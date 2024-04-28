#!/usr/bin/env python

import json

import RNS
import LXMF
import asyncio
import websockets
import base64

# init reticulum
reticulum = RNS.Reticulum(None)

# create a new identity and log as base64
identity = RNS.Identity()
print(base64.b64encode(identity.get_private_key()))

# init lxmf router
message_router = LXMF.LXMRouter(identity=identity, storagepath="storage/lxmf")

# register lxmf identity
local_lxmf_destination = message_router.register_delivery_identity(identity, display_name="ReticulumWebChat")

# global reference to all connected websocket clients
websocket_clients = []


async def main():

    # set a callback for when an lxmf message is received
    message_router.register_delivery_callback(lxmf_delivery)

    # start websocket server
    async with websockets.serve(on_websocket_client_connected, "", 8000):
        await asyncio.Future()  # run forever


# handle websocket messages
async def on_websocket_client_connected(client):

    # add client to connected clients list
    websocket_clients.append(client)

    # handle client messages until disconnected
    while True:
        try:
            message = await client.recv()
            data = json.loads(message)
            await on_data(client, data)
        except websockets.ConnectionClosedOK:
            # client disconnected, we can stop looping
            break
        except Exception as e:
            # ignore errors while handling message
            print("failed to process client message")
            print(e)

    # loop finished, client is no longer connected
    websocket_clients.remove(client)


async def on_data(client, data):

    # get type from client data
    _type = data["type"]

    # handle sending an lxmf message
    if _type == "lxmf.delivery":

        # send lxmf message to destination
        destination_hash = data["destination_hash"]
        message = data["message"]
        send_message(destination_hash, message)

        # # TODO: send response to client when marked as delivered?
        # await client.send(json.dumps({
        #     "type": "lxmf.sent",
        # }))

    # handle sending an announce
    elif _type == "announce":

        # send announce for lxmf
        local_lxmf_destination.announce()

    # unhandled type
    else:
        print("unhandled client message type: " + _type)


def websocket_broadcast(data):
    # broadcast provided data to all connected websocket clients
    for websocket_client in websocket_clients:
        asyncio.run(websocket_client.send(data))


def lxmf_delivery(message):
    try:

        # get message data
        message_content = message.content.decode('utf-8')
        source_hash_text = RNS.hexrep(message.source_hash, delimit=False)

        fields = []
        message_fields = message.get_fields()
        for field_type in message_fields:

            value = message_fields[field_type]

            # handle file attachments field
            if field_type == LXMF.FIELD_FILE_ATTACHMENTS:

                # process file attachments
                file_attachments = []
                for file_attachment in value:
                    file_name = file_attachment[0]
                    file_bytes = base64.b64encode(file_attachment[1]).decode("utf-8")
                    file_attachments.append({
                        "file_name": file_name,
                        "file_bytes": file_bytes,
                    })

                # add to fields
                fields.append({
                    "type": "file_attachments",
                    "file_attachments": file_attachments,
                })

            # handle image field
            if field_type == LXMF.FIELD_IMAGE:
                image_type = value[0]
                image_bytes = base64.b64encode(value[1]).decode("utf-8")
                fields.append({
                    "type": "image",
                    "image_type": image_type,
                    "image_bytes": image_bytes,
                })

            # handle commands field
            if field_type == LXMF.FIELD_COMMANDS:

                # process commands
                commands = []
                for command in value:
                    command_string = command[0]
                    commands.append({
                        "command_string": command_string,
                    })

                # add to fields
                fields.append({
                    "type": "commands",
                    "commands": commands,
                })

        # send received lxmf message data to all websocket clients
        websocket_broadcast(json.dumps({
            "type": "lxmf.delivery",
            "source_hash": source_hash_text,
            "message": {
                "content": message_content,
                "fields": fields,
            },
        }))

    except Exception as e:
        # do nothing on error
        print("lxmf_delivery error: {}".format(e))


def send_message(destination_hash, message_content):

    try:

        # convert destination hash to bytes
        destination_hash = bytes.fromhex(destination_hash)

        # find destination identity from hash
        destination_identity = RNS.Identity.recall(destination_hash)
        if destination_identity is None:

            # we don't know the path/identity for this destination hash, we will request it
            RNS.Transport.request_path(destination_hash)

            # we have to bail out of sending, since we don't have the path yet
            return

        # create destination for recipients lxmf delivery address
        lxmf_destination = RNS.Destination(destination_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery")

        # create lxmf message
        lxm = LXMF.LXMessage(lxmf_destination, local_lxmf_destination, message_content, desired_method=LXMF.LXMessage.DIRECT)
        lxm.try_propagation_on_fail = True

        # send lxmf message to be routed to destination
        message_router.handle_outbound(lxm)

    except:
        # FIXME send error to websocket?
        print("failed to send lxmf message")


if __name__ == "__main__":
    asyncio.run(main())
