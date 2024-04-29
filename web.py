#!/usr/bin/env python

import argparse
import json

import RNS
import LXMF
import asyncio
import websockets
import base64

from sanic import Sanic, Request, Websocket, file

# global references
app_name = "ReticulumWebChat"
reticulum: RNS.Reticulum | None = None
identity: RNS.Identity | None = None
message_router: LXMF.LXMRouter | None = None
local_lxmf_destination: RNS.Destination | None = None
websocket_clients = []

# create sanic app
app = Sanic(app_name)


def main():

    # parse command line args
    parser = argparse.ArgumentParser(description="ReticulumWebChat")
    parser.add_argument("--host", nargs='?', default="0.0.0.0", type=str, help="The address the web server should listen on.")
    parser.add_argument("--port", nargs='?', default="8000", type=int, help="The port the web server should listen on.")
    parser.add_argument("--identity-file", type=str, help="Path to a Reticulum Identity file to use as your LXMF address.")
    parser.add_argument("--identity-base64", type=str, help="A base64 encoded Reticulum Identity to use as your LXMF address.")
    args = parser.parse_args()

    # use provided identity, or fallback to a random one
    global identity
    if args.identity_file is not None:
        identity = RNS.Identity(create_keys=False)
        identity.load(args.identity_file)
        print("Reticulum Identity has been loaded from file.")
        print(identity)
    elif args.identity_base64 is not None:
        identity = RNS.Identity(create_keys=False)
        identity.load_private_key(base64.b64decode(args.identity_base64))
        print("Reticulum Identity has been loaded from base64.")
        print(identity)
    else:
        identity = RNS.Identity(create_keys=True)
        print("Reticulum Identity has been randomly generated.")
        print(identity)

    # run sanic app
    app.run(
        host=args.host,
        port=args.port,
    )


def start_reticulum():

    # init reticulum
    global reticulum
    reticulum = RNS.Reticulum(None)
    
    # init lxmf router
    global message_router
    message_router = LXMF.LXMRouter(identity=identity, storagepath="storage/lxmf")
    
    # register lxmf identity
    global local_lxmf_destination
    local_lxmf_destination = message_router.register_delivery_identity(identity, display_name="ReticulumWebChat")

    # set a callback for when an lxmf message is received
    message_router.register_delivery_callback(lxmf_delivery)
    
    # set a callback for when an lxmf announce is received
    RNS.Transport.register_announce_handler(LXMFAnnounceHandler(on_lxmf_announce_received))


@app.after_server_start
async def after_server_start(*_):
    start_reticulum()


@app.get("/")
async def hello_world(request):
    return await file("index.html")


# handle websocket messages
@app.websocket("/ws")
async def on_websocket_client_connected(request: Request, client: Websocket):

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

        fields = {}
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
                fields["file_attachments"] = file_attachments

            # handle image field
            if field_type == LXMF.FIELD_IMAGE:
                image_type = value[0]
                image_bytes = base64.b64encode(value[1]).decode("utf-8")
                fields["image"] = {
                    "image_type": image_type,
                    "image_bytes": image_bytes,
                }

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


def on_lxmf_announce_received(destination_hash, announced_identity, app_data):

    # log received announce
    RNS.log("Received an announce from " + RNS.prettyhexrep(destination_hash))

    # parse app data
    parsed_app_data = None
    if app_data is not None:
        parsed_app_data = app_data.decode("utf-8")

    # send received lxmf announce to all websocket clients
    websocket_broadcast(json.dumps({
        "type": "announce",
        "destination_hash": destination_hash.hex(),
        "app_data": parsed_app_data,
    }))


class LXMFAnnounceHandler:

    def __init__(self, received_announce_callback):
        self.aspect_filter = "lxmf.delivery"
        self.received_announce_callback = received_announce_callback

    # we will just pass the received announce back to the provided callback
    def received_announce(self, destination_hash, announced_identity, app_data):
        try:
            # handle received announce
            self.received_announce_callback(destination_hash, announced_identity, app_data)
        except:
            # ignore failure to handle received announce
            pass



if __name__ == "__main__":
    main()
