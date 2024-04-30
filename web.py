#!/usr/bin/env python

import argparse
import http
import json
import mimetypes
import os

import RNS
import LXMF
import asyncio
import websockets
import base64


class ReticulumWebChat:

    def __init__(self, webchat_config_file, identity: RNS.Identity):

        # default values before loading config
        self.display_name = "Anonymous Peer"

        # load config
        self.config_file = webchat_config_file or "storage/config.json"
        self.load_config()

        # init reticulum
        self.reticulum = RNS.Reticulum(None)
        self.identity = identity

        # init lxmf router
        self.message_router = LXMF.LXMRouter(identity=self.identity, storagepath="storage/lxmf")

        # register lxmf identity
        self.local_lxmf_destination = self.message_router.register_delivery_identity(self.identity)

        # set a callback for when an lxmf message is received
        self.message_router.register_delivery_callback(self.on_lxmf_delivery)

        # set a callback for when an lxmf announce is received
        RNS.Transport.register_announce_handler(LXMFAnnounceHandler(self.on_lxmf_announce_received))

        # remember websocket clients
        self.websocket_clients = []

    def load_config(self):

        # default config
        config = {

        }

        # attempt to load config and override default values
        try:
            with open(self.config_file, 'r') as f:
                custom_config = json.load(f)
                config |= custom_config

        # config is broken, fallback to defaults
        except:
            print("failed to load config, defaults will be used")

        # update display name from config
        if "display_name" in config:
            self.display_name = config["display_name"]

        # return loaded config
        return config

    def save_config(self):

        # build config
        config = {
            "display_name": self.display_name,
        }

        # attempt to save config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)

        # config is broken, fallback to defaults
        except:
            print("failed to save config")

    async def run(self, host, port):

        # start websocket server
        async with websockets.serve(self.on_websocket_client_connected, host, port, process_request=self.process_request):
            print("ReticulumWebChat server running at http://{}:{}".format(host, port))
            await asyncio.Future()  # run forever

    # handle serving custom http paths
    async def process_request(self, path, request_headers):

        # serve index.html
        if path == "/":
            with open("public/index.html") as f:
                file_content = f.read()
                return http.HTTPStatus.OK, [
                    ('Content-Type', 'text/html')
                ], file_content.encode("utf-8")

        # serve anything in public folder
        public_file_path = os.path.join("public", path.lstrip("/"))
        if os.path.isfile(public_file_path):
            mime_type, _ = mimetypes.guess_type(public_file_path)
            with open(public_file_path, "rb") as f:
                file_content = f.read()
                return http.HTTPStatus.OK, [
                    ('Content-Type', mime_type)
                ], file_content
        
        # by default, websocket is always served, but we only want it to be available at /ws
        # so we will return 404 for everything other than /ws
        if path != "/ws":
            return http.HTTPStatus.NOT_FOUND, [
                ('Content-Type', 'text/html')
            ], b"Not Found"

    # handle new client connecting to websocket
    async def on_websocket_client_connected(self, client):

        # add client to connected clients list
        self.websocket_clients.append(client)

        # send config to all clients
        await self.send_config_to_websocket_clients()

        # handle client messages until disconnected
        while True:
            try:
                message = await client.recv()
                data = json.loads(message)
                await self.on_websocket_data_received(client, data)
            except (websockets.ConnectionClosed, websockets.ConnectionClosedOK, websockets.ConnectionClosedError):
                # client disconnected, we can stop looping
                break
            except Exception as e:
                # ignore errors while handling message
                print("failed to process client message")
                print(e)

        # loop finished, client is no longer connected
        self.websocket_clients.remove(client)

    # handle data received from websocket client
    async def on_websocket_data_received(self, client, data):

        # get type from client data
        _type = data["type"]

        # handle updating config
        if _type == "config.set":

            # send lxmf message to destination
            config = data["config"]

            # update display name in state
            if "display_name" in config and config["display_name"] != "":
                self.display_name = config["display_name"]
                print("updated display name to: " + self.display_name)

            # save config
            self.save_config()

            # send config to websocket clients
            await self.send_config_to_websocket_clients()

        # handle sending an lxmf message
        elif _type == "lxmf.delivery":

            # send lxmf message to destination
            destination_hash = data["destination_hash"]
            message = data["message"]
            await self.send_message(destination_hash, message)

            # # TODO: send response to client when marked as delivered?
            # await client.send(json.dumps({
            #     "type": "lxmf.sent",
            # }))

        # handle sending an announce
        elif _type == "announce":

            # send announce for lxmf
            self.local_lxmf_destination.announce(app_data=self.display_name.encode("utf-8"))

        # unhandled type
        else:
            print("unhandled client message type: " + _type)

    # broadcast provided data to all connected websocket clients
    async def websocket_broadcast(self, data):
        for websocket_client in self.websocket_clients:
            await websocket_client.send(data)

    # broadcasts config to all websocket clients
    async def send_config_to_websocket_clients(self):
        await self.websocket_broadcast(json.dumps({
            "type": "config",
            "config": {
                "display_name": self.display_name,
                "identity_hash": self.identity.hexhash,
                "lxmf_address_hash": self.local_lxmf_destination.hexhash,
            },
        }))

    # convert an lxmf message to a dictionary, for sending over websocket
    def convert_lxmf_message_to_dict(self, lxmf_message: LXMF.LXMessage):

        # handle fields
        fields = {}
        message_fields = lxmf_message.get_fields()
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

        return {
            "hash": lxmf_message.hash.hex(),
            "source_hash": lxmf_message.source_hash.hex(),
            "destination_hash": lxmf_message.destination_hash.hex(),
            "state": self.convert_lxmf_state_to_string(lxmf_message),
            "progress": lxmf_message.progress,
            "content": lxmf_message.content.decode('utf-8'),
            "fields": fields,
        }

    # convert lxmf state to a human friendly string
    def convert_lxmf_state_to_string(self, lxmf_message: LXMF.LXMessage):

        # convert state to string
        lxmf_message_state = "unknown"
        if lxmf_message.state == LXMF.LXMessage.DRAFT:
            lxmf_message_state = "draft"
        elif lxmf_message.state == LXMF.LXMessage.OUTBOUND:
            lxmf_message_state = "outbound"
        elif lxmf_message.state == LXMF.LXMessage.SENDING:
            lxmf_message_state = "sending"
        elif lxmf_message.state == LXMF.LXMessage.SENT:
            lxmf_message_state = "sent"
        elif lxmf_message.state == LXMF.LXMessage.DELIVERED:
            lxmf_message_state = "delivered"
        elif lxmf_message.state == LXMF.LXMessage.FAILED:
            lxmf_message_state = "failed"
        
        return lxmf_message_state

    # handle an lxmf delivery from reticulum
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_delivery(self, message):
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
            asyncio.run(self.websocket_broadcast(json.dumps({
                "type": "lxmf.delivery",
                "lxmf_message": self.convert_lxmf_message_to_dict(message),
            })))

        except Exception as e:
            # do nothing on error
            print("lxmf_delivery error: {}".format(e))

    # handle delivery status update for an outbound lxmf message
    def on_lxmf_sending_state_updated(self, lxmf_message):
    
        # send lxmf message state to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "lxmf_message_state_updated",
            "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
        })))

    # handle delivery failed for an outbound lxmf message
    def on_lxmf_sending_failed(self, lxmf_message):
        # just pass this on, we don't need to do anything special
        self.on_lxmf_sending_state_updated(lxmf_message)

    # handle sending an lxmf message to reticulum
    async def send_message(self, destination_hash, message_content):

        try:

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # FIXME: can this be removed, and just rely on the router to check paths?
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
            lxmf_message = LXMF.LXMessage(lxmf_destination, self.local_lxmf_destination, message_content, desired_method=LXMF.LXMessage.DIRECT)
            lxmf_message.try_propagation_on_fail = True
            lxmf_message.register_delivery_callback(self.on_lxmf_sending_state_updated)
            lxmf_message.register_failed_callback(self.on_lxmf_sending_failed)

            # send lxmf message to be routed to destination
            self.message_router.handle_outbound(lxmf_message)
            
            # send outbound lxmf message to websocket (after passing to router so hash is available)
            await self.websocket_broadcast(json.dumps({
                "type": "lxmf_outbound_message_created",
                "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
            }))

        except:
            # FIXME send error to websocket?
            print("failed to send lxmf message")

    # handle an announce received from reticulum, for an lxmf address
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_announce_received(self, destination_hash, announced_identity, app_data):

        # log received announce
        RNS.log("Received an announce from " + RNS.prettyhexrep(destination_hash))

        # parse app data
        parsed_app_data = None
        if app_data is not None:
            parsed_app_data = app_data.decode("utf-8")

        # send received lxmf announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "destination_hash": destination_hash.hex(),
            "app_data": parsed_app_data,
        })))


# an announce handler for lxmf.delivery aspect that just forwards to a provided callback
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

async def main():

    # parse command line args
    parser = argparse.ArgumentParser(description="ReticulumWebChat")
    parser.add_argument("--host", nargs='?', default="0.0.0.0", type=str, help="The address the web server should listen on.")
    parser.add_argument("--port", nargs='?', default="8000", type=int, help="The port the web server should listen on.")
    parser.add_argument("--identity-file", type=str, help="Path to a Reticulum Identity file to use as your LXMF address.")
    parser.add_argument("--identity-base64", type=str, help="A base64 encoded Reticulum Identity to use as your LXMF address.")
    parser.add_argument("--webchat-config-file", type=str, help="Path to a ReticulumWebChat config file for saving user preferences.")
    args = parser.parse_args()

    # use provided identity, or fallback to a random one
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

    # init app
    reticulum_webchat = ReticulumWebChat(args.webchat_config_file, identity)
    await reticulum_webchat.run(args.host, args.port)
    
    
if __name__ == "__main__":
    asyncio.run(main())
