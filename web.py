#!/usr/bin/env python

import argparse
import json
import os
import time
from datetime import datetime, timezone
from typing import Callable, List

import RNS
import LXMF
from aiohttp import web, WSMessage, WSMsgType, WSCloseCode
import asyncio
import base64
import webbrowser

from peewee import SqliteDatabase

import database
from lxmf_message_fields import LxmfImageField, LxmfFileAttachmentsField, LxmfFileAttachment
from src.audio_call_manager import AudioCall, AudioCallManager


class ReticulumWebChat:

    def __init__(self, identity: RNS.Identity, storage_dir, reticulum_config_dir):

        # when providing a custom storage_dir, files will be saved as
        # <storage_dir>/identities/<identity_hex>/
        # <storage_dir>/identities/<identity_hex>/database.db

        # if storage_dir is not provided, we will use ./storage instead
        # ./storage/identities/<identity_hex>/
        # ./storage/identities/<identity_hex>/database.db

        # ensure a storage path exists for the loaded identity
        base_storage_dir = storage_dir or os.path.join("storage")
        storage_path = os.path.join(base_storage_dir, "identities", identity.hash.hex())
        print("Using Storage Path: {}".format(storage_path))
        os.makedirs(storage_path, exist_ok=True)

        # define path to files based on storage path
        database_path = os.path.join(storage_path, "database.db")
        lxmf_router_path = os.path.join(storage_path, "lxmf_router")

        # init database
        sqlite_database = SqliteDatabase(database_path)
        database.database.initialize(sqlite_database)
        self.db = database.database
        self.db.connect()
        self.db.create_tables([
            database.Config,
            database.Announce,
            database.LxmfMessage,
        ])

        # vacuum database on start to shrink its file size
        sqlite_database.execute_sql("VACUUM")

        # lxmf messages in outbound or sending state should be marked as failed when app starts as they are no longer being processed
        (database.LxmfMessage.update(state="failed")
         .where(database.LxmfMessage.state == "outbound")
         .orwhere(database.LxmfMessage.state == "sending").execute())

        # init config
        self.config = Config()

        # init reticulum
        self.reticulum = RNS.Reticulum(reticulum_config_dir)
        self.identity = identity

        # init lxmf router
        self.message_router = LXMF.LXMRouter(identity=self.identity, storagepath=lxmf_router_path)

        # register lxmf identity
        self.local_lxmf_destination = self.message_router.register_delivery_identity(self.identity)

        # set a callback for when an lxmf message is received
        self.message_router.register_delivery_callback(self.on_lxmf_delivery)

        # set a callback for when an lxmf announce is received
        RNS.Transport.register_announce_handler(LXMFAnnounceHandler(self.on_lxmf_announce_received))
        RNS.Transport.register_announce_handler(NomadnetworkNodeAnnounceHandler(self.on_nomadnet_node_announce_received))

        # remember websocket clients
        self.websocket_clients: List[web.WebSocketResponse] = []

        # register audio call identity
        self.audio_call_manager = AudioCallManager(identity=self.identity)
        self.audio_call_manager.register_incoming_call_callback(self.on_incoming_audio_call)

    # handle receiving a new audio call
    def on_incoming_audio_call(self, audio_call: AudioCall):
        print("on_incoming_audio_call: {}".format(audio_call.link.hash.hex()))

    # web server has shutdown, likely ctrl+c, but if we don't do the following, the script never exits
    async def shutdown(self, app):

        # force close websocket clients
        for websocket_client in self.websocket_clients:
            print("force closing websocket for shutdown")
            await websocket_client.close(code=WSCloseCode.GOING_AWAY)
            print("force closed websocket")

        # stop reticulum
        print("stopping reticulum")
        RNS.Transport.detach_interfaces()
        self.reticulum.exit_handler()
        RNS.exit()

    def run(self, host, port, launch_browser: bool):

        # create route table
        routes = web.RouteTableDef()

        # serve index.html
        @routes.get("/")
        async def index(request):
            return web.FileResponse(path="public/index.html")

        # handle websocket clients
        @routes.get("/ws")
        async def ws(request):

            # prepare websocket response
            websocket_response = web.WebSocketResponse(
                # set max message size accepted by server to 50 megabytes
                max_msg_size=50 * 1024 * 1024,
            )
            await websocket_response.prepare(request)

            # add client to connected clients list
            self.websocket_clients.append(websocket_response)

            # send config to all clients
            await self.send_config_to_websocket_clients()

            # handle websocket messages until disconnected
            async for msg in websocket_response:
                msg: WSMessage = msg
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self.on_websocket_data_received(websocket_response, data)
                    except Exception as e:
                        # ignore errors while handling message
                        print("failed to process client message")
                        print(e)
                elif msg.type == WSMsgType.ERROR:
                    # ignore errors while handling message
                    print('ws connection error %s' % websocket_response.exception())

            # websocket closed
            self.websocket_clients.remove(websocket_response)

            return websocket_response

        # handle websocket clients for initiating a call
        # todo: remove
        @routes.get("/call/initiate/{destination_hash}")
        async def ws(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # prepare websocket response
            websocket_response = web.WebSocketResponse()
            await websocket_response.prepare(request)

            # wait until we have a path to the destination
            if not RNS.Transport.has_path(destination_hash):
                print("waiting for path to server")
                RNS.Transport.request_path(destination_hash)
                while not RNS.Transport.has_path(destination_hash):
                    await asyncio.sleep(0.1)

            # connect to server
            print("establishing link with server")
            server_identity = RNS.Identity.recall(destination_hash)
            server_destination = RNS.Destination(
                server_identity,
                RNS.Destination.OUT,
                RNS.Destination.SINGLE,
                "call",
                "audio"
            )

            # todo implement
            def link_established(link):
                print("link established")

            # todo implement
            def link_closed(link):
                if link.teardown_reason == RNS.Link.TIMEOUT:
                    print("The link timed out, exiting now")
                elif link.teardown_reason == RNS.Link.DESTINATION_CLOSED:
                    print("The link was closed by the server, exiting now")
                else:
                    print("Link closed")

            # todo implement
            def client_packet_received(message, packet):

                # send audio received from call receiver to call initiator websocket
                asyncio.run(websocket_response.send_bytes(message))

            # create link
            link = RNS.Link(server_destination)

            # register link state callbacks
            link.set_packet_callback(client_packet_received)
            link.set_link_established_callback(link_established)
            link.set_link_closed_callback(link_closed)

            # handle websocket messages until disconnected
            async for msg in websocket_response:
                msg: WSMessage = msg
                if msg.type == WSMsgType.BINARY:
                    try:

                        # drop audio packet if it is too big to send
                        if len(msg.data) > RNS.Link.MDU:
                            print("dropping packet " + str(len(msg.data)) + " bytes exceeds the link packet MDU of " + str(RNS.Link.MDU) + " bytes")
                            continue

                        # send codec2 audio received from call initiator on websocket, to call receiver over reticulum link
                        print("sending bytes to call receiver: {}".format(len(msg.data)))
                        RNS.Packet(link, msg.data).send()

                    except Exception as e:
                        # ignore errors while handling message
                        print("failed to process client message")
                        print(e)
                elif msg.type == WSMsgType.ERROR:
                    # ignore errors while handling message
                    print('ws connection error %s' % websocket_response.exception())

            return websocket_response

        # get config
        @routes.get("/api/v1/config")
        async def index(request):
            return web.json_response({
                "config": self.get_config_dict(),
            })

        # get calls
        @routes.get("/api/v1/calls")
        async def index(request):

            # get audio calls
            audio_calls = []
            for audio_call in self.audio_call_manager.audio_calls:
                audio_calls.append(self.convert_audio_call_to_dict(audio_call))

            return web.json_response({
                "audio_calls": audio_calls,
            })

        # get call
        @routes.get("/api/v1/calls/{audio_call_link_hash}")
        async def index(request):

            # get path params
            audio_call_link_hash = request.match_info.get("audio_call_link_hash", "")

            # convert hash to bytes
            audio_call_link_hash = bytes.fromhex(audio_call_link_hash)

            # find audio call
            audio_call = self.audio_call_manager.find_audio_call_by_link_hash(audio_call_link_hash)
            if audio_call is None:
                return web.json_response({
                    "message": "audio call not found",
                }, status=404)

            return web.json_response({
                "audio_call": self.convert_audio_call_to_dict(audio_call),
            })

        # delete call
        @routes.delete("/api/v1/calls/{audio_call_link_hash}")
        async def index(request):

            # get path params
            audio_call_link_hash = request.match_info.get("audio_call_link_hash", "")

            # convert hash to bytes
            audio_call_link_hash = bytes.fromhex(audio_call_link_hash)

            # delete audio call
            self.audio_call_manager.delete_audio_call_by_link_hash(audio_call_link_hash)

            return web.json_response({
                "message": "audio call deleted",
            })

        # initiate a call to the provided destination
        @routes.get("/api/v1/calls/initiate/{destination_hash}")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # initiate audio call
            link_hash = await self.audio_call_manager.initiate(destination_hash)

            return web.json_response({
                "hash": link_hash.hex(),
            })

        # handle websocket client for sending and receiving audio packets in a call
        @routes.get("/api/v1/calls/{audio_call_link_hash}/audio")
        async def ws(request):

            # get path params
            audio_call_link_hash = request.match_info.get("audio_call_link_hash", "")

            # convert hash to bytes
            audio_call_link_hash = bytes.fromhex(audio_call_link_hash)

            # find audio call, this will be null until the link is established
            audio_call = self.audio_call_manager.find_audio_call_by_link_hash(audio_call_link_hash)
            if audio_call is None:
                # fixme: web browser expects websocket, so this won't be useful
                return web.json_response({
                    "message": "audio call not found",
                }, status=404)

            # send audio received from call initiator to call receiver websocket
            def on_audio_packet(data):
                if websocket_response.closed is False:
                    try:
                        asyncio.run(websocket_response.send_bytes(data))
                    except:
                        # ignore errors sending audio packets to websocket
                        pass

            # close websocket when call is hungup
            def on_hangup():
                if websocket_response.closed is False:
                    try:
                        asyncio.run(websocket_response.close(code=WSCloseCode.GOING_AWAY))
                    except:
                        # ignore errors closing websocket
                        pass

            # register audio packet listener
            audio_call.register_audio_packet_listener(on_audio_packet)
            audio_call.register_hangup_listener(on_hangup)

            # prepare websocket response
            websocket_response = web.WebSocketResponse()
            await websocket_response.prepare(request)

            # handle websocket messages until disconnected
            # FIXME: we should send a type with the message, so we can send other data as well
            async for msg in websocket_response:
                msg: WSMessage = msg
                if msg.type == WSMsgType.BINARY:
                    try:
                        audio_call.send_audio_packet(msg.data)
                    except Exception as e:
                        # ignore errors while handling message
                        print("failed to process client message")
                        print(e)
                elif msg.type == WSMsgType.ERROR:
                    # ignore errors while handling message
                    print('ws connection error %s' % websocket_response.exception())

            # unregister audio packet handler now that the websocket has been closed
            audio_call.register_audio_packet_listener(on_audio_packet)

            return websocket_response

        # hangup calls
        @routes.get("/api/v1/calls/{audio_call_link_hash}/hangup")
        async def index(request):

            # get path params
            audio_call_link_hash = request.match_info.get("audio_call_link_hash", "")

            # convert hash to bytes
            audio_call_link_hash = bytes.fromhex(audio_call_link_hash)

            # find audio call
            audio_call = self.audio_call_manager.find_audio_call_by_link_hash(audio_call_link_hash)
            if audio_call is None:
                return web.json_response({
                    "message": "audio call not found",
                }, status=404)

            # hangup the call
            audio_call.hangup()

            return web.json_response({
                "message": "call has been hungup",
            })

        # serve announces
        @routes.get("/api/v1/announces")
        async def index(request):

            # get query params
            aspect = request.query.get("aspect", None)

            # build announces database query
            query = database.Announce.select()

            # filter by provided aspect
            if aspect is not None:
                query = query.where(database.Announce.aspect == aspect)

            # get announces from database
            query_results = query.order_by(database.Announce.id.asc())

            # process announces
            announces = []
            for announce in query_results:
                announces.append(self.convert_db_announce_to_dict(announce))

            return web.json_response({
                "announces": announces,
            })

        # get path to destination
        @routes.get("/api/v1/destination/{destination_hash}/path")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # check if user wants to request the path from the network right now
            request_query_param = request.query.get("request", "false")
            should_request_now = request_query_param == "true" or request_query_param == "1"
            if should_request_now:

                # determine how long we should wait for a path response
                timeout_seconds = int(request.query.get("timeout", 15))
                timeout_after_seconds = time.time() + timeout_seconds

                # request path if we don't have it
                if not RNS.Transport.has_path(destination_hash):
                    RNS.Transport.request_path(destination_hash)

                # wait until we have a path, or give up after the configured timeout
                while not RNS.Transport.has_path(destination_hash) and time.time() < timeout_after_seconds:
                    await asyncio.sleep(0.1)

            # ensure path is known
            if not RNS.Transport.has_path(destination_hash):
                return web.json_response({
                    "path": None,
                })

            # determine next hop and hop count
            hops = RNS.Transport.hops_to(destination_hash)
            next_hop_bytes = self.reticulum.get_next_hop(destination_hash)

            # ensure next hop provided
            if next_hop_bytes is None:
                return web.json_response({
                    "path": None,
                })

            next_hop = next_hop_bytes.hex()
            next_hop_interface = self.reticulum.get_next_hop_if_name(destination_hash)

            return web.json_response({
                "path": {
                    "hops": hops,
                    "next_hop": next_hop,
                    "next_hop_interface": next_hop_interface,
                },
            })

        # get interface stats
        @routes.get("/api/v1/interface-stats")
        async def index(request):

            # get interface stats
            interface_stats = self.reticulum.get_interface_stats()

            # ensure transport_id is hex as json_response can't serialize bytes
            if "transport_id" in interface_stats:
                interface_stats["transport_id"] = interface_stats["transport_id"].hex()

            return web.json_response({
                "interface_stats": interface_stats,
            })

        # get path table
        @routes.get("/api/v1/path-table")
        async def index(request):

            # get path table, making sure hash and via are in hex as json_response can't serialize bytes
            path_table = []
            for path in self.reticulum.get_path_table():
                path["hash"] = path["hash"].hex()
                path["via"] = path["via"].hex()
                path_table.append(path)

            return web.json_response({
                "path_table": path_table,
            })

        # delete lxmf message
        @routes.delete("/api/v1/lxmf-messages/{id}")
        async def index(request):

            # get path params
            id = request.match_info.get("id", None)

            # source_hash is required
            if id is None:
                return web.json_response({
                    "message": "id is required",
                }, status=422)

            # delete lxmf messages from db where id matches
            database.LxmfMessage.delete_by_id(id)

            return web.json_response({
                "message": "ok",
            })

        # serve lxmf messages for conversation
        @routes.get("/api/v1/lxmf-messages/conversation/{destination_hash}")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # get source hash from local lxmf destination
            source_hash = self.local_lxmf_destination.hash.hex()

            # get lxmf messages from db where "source to destination" or "destination to source" and ordered by oldest to newest
            db_lxmf_messages = (database.LxmfMessage.select()
                                .where((database.LxmfMessage.source_hash == source_hash) & (database.LxmfMessage.destination_hash == destination_hash))
                                .orwhere((database.LxmfMessage.destination_hash == source_hash) & (database.LxmfMessage.source_hash == destination_hash))
                                .order_by(database.LxmfMessage.id.asc())
                                )

            # convert to response json
            lxmf_messages = []
            for db_lxmf_message in db_lxmf_messages:
                lxmf_messages.append({
                    "id": db_lxmf_message.id,
                    "hash": db_lxmf_message.hash,
                    "source_hash": db_lxmf_message.source_hash,
                    "destination_hash": db_lxmf_message.destination_hash,
                    "is_incoming": db_lxmf_message.is_incoming,
                    "state": db_lxmf_message.state,
                    "progress": db_lxmf_message.progress,
                    "title": db_lxmf_message.title,
                    "content": db_lxmf_message.content,
                    "fields": json.loads(db_lxmf_message.fields),
                    "timestamp": db_lxmf_message.timestamp,
                    "created_at": db_lxmf_message.created_at,
                    "updated_at": db_lxmf_message.updated_at,
                })

            return web.json_response({
                "lxmf_messages": lxmf_messages,
            })

        # delete lxmf messages for conversation
        @routes.delete("/api/v1/lxmf-messages/conversation/{destination_hash}")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # get source hash from local lxmf destination
            source_hash = self.local_lxmf_destination.hash.hex()

            # delete lxmf messages from db where "source to destination" or "destination to source"
            (database.LxmfMessage.delete()
             .where((database.LxmfMessage.source_hash == source_hash) & (database.LxmfMessage.destination_hash == destination_hash))
             .orwhere((database.LxmfMessage.destination_hash == source_hash) & (database.LxmfMessage.source_hash == destination_hash))
             .execute())

            return web.json_response({
                "message": "ok",
            })

        # called when web app has started
        async def on_startup(app):

            # auto launch web browser
            if launch_browser:
                try:
                    webbrowser.open("http://127.0.0.1:{}".format(port))
                except:
                    print("failed to launch web browser")

        # create and run web app
        app = web.Application()
        app.add_routes(routes)
        app.add_routes([web.static('/', "public")])  # serve anything in public folder
        app.on_shutdown.append(self.shutdown)  # need to force close websockets and stop reticulum now
        app.on_startup.append(on_startup)
        web.run_app(app, host=host, port=port)

    # handle data received from websocket client
    async def on_websocket_data_received(self, client, data):

        # get type from client data
        _type = data["type"]

        # handle updating config
        if _type == "config.set":

            # send lxmf message to destination
            config = data["config"]

            # update display name in config
            if "display_name" in config and config["display_name"] != "":
                self.config.display_name.set(config["display_name"])

            # send config to websocket clients
            await self.send_config_to_websocket_clients()

        # handle sending an lxmf message
        elif _type == "lxmf.delivery":

            # get data from websocket client
            destination_hash = data["lxmf_message"]["destination_hash"]
            content = data["lxmf_message"]["content"]
            fields = {}
            if "fields" in data["lxmf_message"]:
                fields = data["lxmf_message"]["fields"]

            # parse image field
            image_field = None
            if "image" in fields:
                image_type = data["lxmf_message"]["fields"]["image"]["image_type"]
                image_bytes = base64.b64decode(data["lxmf_message"]["fields"]["image"]["image_bytes"])
                image_field = LxmfImageField(image_type, image_bytes)

            # parse file attachments field
            file_attachments_field = None
            if "file_attachments" in fields:

                file_attachments = []
                for file_attachment in data["lxmf_message"]["fields"]["file_attachments"]:
                    file_name = file_attachment["file_name"]
                    file_bytes = base64.b64decode(file_attachment["file_bytes"])
                    file_attachments.append(LxmfFileAttachment(file_name, file_bytes))

                file_attachments_field = LxmfFileAttachmentsField(file_attachments)

            # send lxmf message to destination
            await self.send_message(destination_hash, content, image_field=image_field, file_attachments_field=file_attachments_field)

            # # TODO: send response to client when marked as delivered?
            # await client.send(json.dumps({
            #     "type": "lxmf.sent",
            # }))

        # handle sending an announce
        elif _type == "announce":

            # send announce for lxmf
            self.local_lxmf_destination.announce(app_data=self.config.display_name.get().encode("utf-8"))

            # send announce for audio call
            self.audio_call_manager.announce(app_data=self.config.display_name.get().encode("utf-8"))

        # handle downloading a file from a nomadnet node
        elif _type == "nomadnet.file.download":

            # get data from websocket client
            destination_hash = data["nomadnet_file_download"]["destination_hash"]
            file_path = data["nomadnet_file_download"]["file_path"]

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # handle successful file download
            def on_file_download_success(file_name, file_bytes):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.file.download",
                    "nomadnet_file_download": {
                        "status": "success",
                        "destination_hash": destination_hash.hex(),
                        "file_path": file_path,
                        "file_name": file_name,
                        "file_bytes": base64.b64encode(file_bytes).decode("utf-8"),
                    },
                })))

            # handle file download failure
            def on_file_download_failure(failure_reason):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.file.download",
                    "nomadnet_file_download": {
                        "status": "error",
                        "failure_reason": failure_reason,
                        "destination_hash": destination_hash.hex(),
                        "file_path": file_path,
                    },
                })))

            # handle file download progress
            def on_file_download_progress(progress):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.file.download",
                    "nomadnet_file_download": {
                        "status": "progress",
                        "progress": progress,
                        "destination_hash": destination_hash.hex(),
                        "file_path": file_path,
                    },
                })))

            # todo: handle file download progress

            # download the file
            NomadnetFileDownloader(destination_hash, file_path, on_file_download_success, on_file_download_failure, on_file_download_progress)

        # handle downloading a page from a nomadnet node
        elif _type == "nomadnet.page.download":

            # get data from websocket client
            destination_hash = data["nomadnet_page_download"]["destination_hash"]
            page_path = data["nomadnet_page_download"]["page_path"]

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # handle successful page download
            def on_page_download_success(page_content):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.page.download",
                    "nomadnet_page_download": {
                        "status": "success",
                        "destination_hash": destination_hash.hex(),
                        "page_path": page_path,
                        "page_content": page_content,
                    },
                })))

            # handle page download failure
            def on_page_download_failure(failure_reason):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.page.download",
                    "nomadnet_page_download": {
                        "status": "error",
                        "failure_reason": failure_reason,
                        "destination_hash": destination_hash.hex(),
                        "page_path": page_path,
                    },
                })))

            # handle page download progress
            def on_page_download_progress(progress):
                asyncio.run(client.send_str(json.dumps({
                    "type": "nomadnet.page.download",
                    "nomadnet_page_download": {
                        "status": "progress",
                        "progress": progress,
                        "destination_hash": destination_hash.hex(),
                        "page_path": page_path,
                    },
                })))

            # todo: handle page download progress

            # download the page
            NomadnetPageDownloader(destination_hash, page_path, on_page_download_success, on_page_download_failure, on_page_download_progress)

        # unhandled type
        else:
            print("unhandled client message type: " + _type)

    # broadcast provided data to all connected websocket clients
    async def websocket_broadcast(self, data):
        for websocket_client in self.websocket_clients:
            try:
                await websocket_client.send_str(data)
            except:
                # do nothing if failed to broadcast to a specific websocket client
                pass

    # broadcasts config to all websocket clients
    async def send_config_to_websocket_clients(self):
        await self.websocket_broadcast(json.dumps({
            "type": "config",
            "config": self.get_config_dict(),
        }))

    # returns a dictionary of config
    def get_config_dict(self):
        return {
            "display_name": self.config.display_name.get(),
            "identity_hash": self.identity.hexhash,
            "lxmf_address_hash": self.local_lxmf_destination.hexhash,
            "audio_call_address_hash": self.audio_call_manager.audio_call_receiver.destination.hexhash,
        }

    # convert audio call to dict
    def convert_audio_call_to_dict(self, audio_call: AudioCall):

        # get remote identity hash
        remote_identity_hash = None
        remote_identity = audio_call.get_remote_identity()
        if remote_identity is not None:
            remote_identity_hash = remote_identity.hash.hex()

        # get remote destination hash
        # we need to know the remote identity to determine their destination hash
        remote_destination_hash = None
        if remote_identity is not None:
            remote_destination_hash = RNS.Destination.hash(remote_identity, "call", "audio")

        # determine path to remote destination
        path = None
        if remote_destination_hash is not None:

            # determine next hop and hop count
            hops = RNS.Transport.hops_to(remote_destination_hash)
            next_hop_bytes = self.reticulum.get_next_hop(remote_destination_hash)

            # ensure next hop provided
            if next_hop_bytes is not None:
                next_hop = next_hop_bytes.hex()
                next_hop_interface = self.reticulum.get_next_hop_if_name(remote_destination_hash)
                path = {
                    "hops": hops,
                    "next_hop": next_hop,
                    "next_hop_interface": next_hop_interface,
                }

        return {
            "hash": audio_call.link.hash.hex(),
            "remote_destination_hash": remote_destination_hash.hex(),
            "remote_identity_hash": remote_identity_hash,
            "is_active": audio_call.is_active(),
            "is_outbound": audio_call.is_outbound,
            "path": path,
        }

    # convert app data to string, or return none unable to do so
    def convert_app_data_to_string(self, app_data):

        # attempt to convert to utf-8 string
        if app_data is not None:
            try:
                return app_data.decode("utf-8")
            except:
                # ignore failure to convert to string
                pass

        # unable to convert to string
        return None

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

        # convert 0.0-1.0 progress to 0.00-100 percentage
        progress_percentage = round(lxmf_message.progress * 100, 2)

        return {
            "hash": lxmf_message.hash.hex(),
            "source_hash": lxmf_message.source_hash.hex(),
            "destination_hash": lxmf_message.destination_hash.hex(),
            "is_incoming": lxmf_message.incoming,
            "state": self.convert_lxmf_state_to_string(lxmf_message),
            "progress": progress_percentage,
            "title": lxmf_message.title.decode('utf-8'),
            "content": lxmf_message.content.decode('utf-8'),
            "fields": fields,
            "timestamp": lxmf_message.timestamp,
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

    # convert database announce to a dictionary
    def convert_db_announce_to_dict(self, announce: database.Announce):
        return {
            "id": announce.id,
            "destination_hash": announce.destination_hash,
            "aspect": announce.aspect,
            "identity_hash": announce.identity_hash,
            "identity_public_key": announce.identity_public_key,
            "app_data": announce.app_data,
            "created_at": announce.created_at,
            "updated_at": announce.updated_at,
        }

    # handle an lxmf delivery from reticulum
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_delivery(self, lxmf_message):
        try:

            # upsert lxmf message to database
            self.db_upsert_lxmf_message(lxmf_message)

            # send received lxmf message data to all websocket clients
            asyncio.run(self.websocket_broadcast(json.dumps({
                "type": "lxmf.delivery",
                "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
            })))

        except Exception as e:
            # do nothing on error
            print("lxmf_delivery error: {}".format(e))

    # handle delivery status update for an outbound lxmf message
    def on_lxmf_sending_state_updated(self, lxmf_message):

        # upsert lxmf message to database
        self.db_upsert_lxmf_message(lxmf_message)

        # send lxmf message state to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "lxmf_message_state_updated",
            "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
        })))

    # handle delivery failed for an outbound lxmf message
    def on_lxmf_sending_failed(self, lxmf_message):
        # just pass this on, we don't need to do anything special
        self.on_lxmf_sending_state_updated(lxmf_message)

    # upserts the provided lxmf message to the database
    def db_upsert_lxmf_message(self, lxmf_message: LXMF.LXMessage):

        # convert lxmf message to dict
        lxmf_message_dict = self.convert_lxmf_message_to_dict(lxmf_message)

        # prepare data to insert or update
        data = {
            "hash": lxmf_message_dict["hash"],
            "source_hash": lxmf_message_dict["source_hash"],
            "destination_hash": lxmf_message_dict["destination_hash"],
            "is_incoming": lxmf_message_dict["is_incoming"],
            "state": lxmf_message_dict["state"],
            "progress": lxmf_message_dict["progress"],
            "title": lxmf_message_dict["title"],
            "content": lxmf_message_dict["content"],
            "fields": json.dumps(lxmf_message_dict["fields"]),
            "timestamp": lxmf_message_dict["timestamp"],
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.LxmfMessage.insert(data)
        query = query.on_conflict(conflict_target=[database.LxmfMessage.hash], update=data)
        query.execute()

    # upserts the provided announce to the database
    def db_upsert_announce(self, identity: RNS.Identity, destination_hash: bytes, aspect: str, app_data: bytes):

        # parse app data
        parsed_app_data = None
        if app_data is not None:
            parsed_app_data = base64.b64encode(app_data).decode("utf-8")

        # prepare data to insert or update
        data = {
            "destination_hash": destination_hash.hex(),
            "aspect": aspect,
            "identity_hash": identity.hash.hex(),
            "identity_public_key": base64.b64encode(identity.get_public_key()).decode("utf-8"),
            "app_data": parsed_app_data,
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.Announce.insert(data)
        query = query.on_conflict(conflict_target=[database.Announce.destination_hash], update=data)
        query.execute()

    # handle sending an lxmf message to reticulum
    async def send_message(self, destination_hash, content: str,
                           image_field: LxmfImageField = None,
                           file_attachments_field: LxmfFileAttachmentsField = None):

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
                # FIXME: we just ate the message, and didn't tell the user it failed...
                return

            # create destination for recipients lxmf delivery address
            lxmf_destination = RNS.Destination(destination_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery")

            # create lxmf message
            lxmf_message = LXMF.LXMessage(lxmf_destination, self.local_lxmf_destination, content, desired_method=LXMF.LXMessage.DIRECT)
            lxmf_message.try_propagation_on_fail = True

            lxmf_message.fields = {}

            # add file attachments field
            if file_attachments_field is not None:

                # create array of [[file_name, file_bytes], [file_name, file_bytes], ...]
                file_attachments = []
                for file_attachment in file_attachments_field.file_attachments:
                    file_attachments.append([file_attachment.file_name, file_attachment.file_bytes])

                # set field attachments field
                lxmf_message.fields[LXMF.FIELD_FILE_ATTACHMENTS] = file_attachments

            # add image field
            if image_field is not None:
                lxmf_message.fields[LXMF.FIELD_IMAGE] = [
                    image_field.image_type,
                    image_field.image_bytes,
                ]

            # register delivery callbacks
            lxmf_message.register_delivery_callback(self.on_lxmf_sending_state_updated)
            lxmf_message.register_failed_callback(self.on_lxmf_sending_failed)

            # send lxmf message to be routed to destination
            self.message_router.handle_outbound(lxmf_message)

            # upsert lxmf message to database
            self.db_upsert_lxmf_message(lxmf_message)

            # send outbound lxmf message to websocket (after passing to router so hash is available)
            await self.websocket_broadcast(json.dumps({
                "type": "lxmf_outbound_message_created",
                "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
            }))

            # handle lxmf message progress loop without blocking or awaiting
            # otherwise other incoming websocket packets will not be processed until sending is complete
            # which results in the next message not showing up until the first message is finished
            asyncio.create_task(self.handle_lxmf_message_progress(lxmf_message))

        except:
            # FIXME send error to websocket?
            print("failed to send lxmf message")

    # updates lxmf message in database and broadcasts to websocket until it's delivered, or it fails
    async def handle_lxmf_message_progress(self, lxmf_message):

        # FIXME: there's no register_progress_callback on the lxmf message, so manually send progress until delivered or failed
        # we also can't use on_lxmf_sending_state_updated method to do this, because of async/await issues...
        while lxmf_message.state != LXMF.LXMessage.DELIVERED and lxmf_message.state != LXMF.LXMessage.FAILED:

            # wait 1 second between sending updates
            await asyncio.sleep(1)

            # upsert lxmf message to database (as we want to update the progress in database too)
            self.db_upsert_lxmf_message(lxmf_message)

            # send update to websocket clients
            await self.websocket_broadcast(json.dumps({
                "type": "lxmf_message_state_updated",
                "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
            }))


    # handle an announce received from reticulum, for an lxmf address
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_announce_received(self, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [lxmf.delivery]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, "lxmf.delivery", app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))

    # handle an announce received from reticulum, for a nomadnet node
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_nomadnet_node_announce_received(self, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [nomadnetwork.node]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, "nomadnetwork.node", app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))


# class to manage config stored in database
class Config:

    @staticmethod
    def get(key: str, default_value=None):

        # get config value from database
        config_item = database.Config.get_or_none(database.Config.key == key)

        # return value if available
        if config_item is not None:
            return config_item.value

        # fallback to returning default value
        return default_value

    @staticmethod
    def set(key: str, value: str):

        # prepare data to insert or update
        data = {
            "key": key,
            "value": value,
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.Config.insert(data)
        query = query.on_conflict(conflict_target=[database.Config.key], update=data)
        query.execute()

    # handle config values that should be strings
    class StringConfig:

        def __init__(self, key: str, default_value: str = None):
            self.key = key
            self.default_value = default_value

        def get(self, default_value: str = None):
            _default_value = default_value or self.default_value
            return Config.get(self.key, default_value=_default_value)

        def set(self, value: str):
            return Config.set(self.key, value)

    # all possible config items
    display_name = StringConfig("display_name", "Anonymous Peer")


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


# an announce handler for nomadnetwork.node aspect that just forwards to a provided callback
class NomadnetworkNodeAnnounceHandler:

    def __init__(self, received_announce_callback):
        self.aspect_filter = "nomadnetwork.node"
        self.received_announce_callback = received_announce_callback

    # we will just pass the received announce back to the provided callback
    def received_announce(self, destination_hash, announced_identity, app_data):
        try:
            # handle received announce
            self.received_announce_callback(destination_hash, announced_identity, app_data)
        except:
            # ignore failure to handle received announce
            pass


class NomadnetDownloader:

    def __init__(self, destination_hash: bytes, path: str, on_download_success: Callable[[bytes], None], on_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None, auto_download=True):
        self.app_name = "nomadnetwork"
        self.aspects = "node"
        self.destination_hash = destination_hash
        self.path = path
        self.timeout = timeout
        self.on_download_success = on_download_success
        self.on_download_failure = on_download_failure
        self.on_progress_update = on_progress_update
        if auto_download:
            self.download()

    # setup link to destination and request download
    def download(self):

        # request path to destination
        RNS.Transport.request_path(self.destination_hash)

        # find existing identity
        identity = RNS.Identity.recall(self.destination_hash)
        if identity is None:
            self.on_download_failure("identity not found")
            return

        # create destination to nomadnet node
        destination = RNS.Destination(
            identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            self.app_name,
            self.aspects,
        )

        # create link to destination
        RNS.Link(destination, established_callback=self.link_established)

    # link to destination was established, we should now request the download
    def link_established(self, link):

        # request download over link
        link.request(
            self.path,
            data=None,
            response_callback=self.on_response,
            failed_callback=self.on_failed,
            progress_callback=self.on_progress,
            timeout=self.timeout,
        )

    # handle successful download
    def on_response(self, request_receipt):
        self.on_download_success(request_receipt.response)

    # handle failure
    def on_failed(self, request_receipt=None):
        self.on_download_failure("request_failed")

    # handle download progress
    def on_progress(self, request_receipt):
        self.on_progress_update(request_receipt.progress)


class NomadnetPageDownloader(NomadnetDownloader):

    def __init__(self, destination_hash: bytes, page_path: str, on_page_download_success: Callable[[str], None], on_page_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None, auto_download=True):
        self.on_page_download_success = on_page_download_success
        self.on_page_download_failure = on_page_download_failure
        super().__init__(destination_hash, page_path, self.on_download_success, self.on_download_failure, on_progress_update, timeout, auto_download)

    # page download was successful, decode the response and send to provided callback
    def on_download_success(self, response_bytes):
        micron_markup_response = response_bytes.decode("utf-8")
        self.on_page_download_success(micron_markup_response)

    # page download failed, send error to provided callback
    def on_download_failure(self, failure_reason):
        self.on_page_download_failure(failure_reason)


class NomadnetFileDownloader(NomadnetDownloader):

    def __init__(self, destination_hash: bytes, page_path: str, on_file_download_success: Callable[[str, bytes], None], on_file_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None, auto_download=True):
        self.on_file_download_success = on_file_download_success
        self.on_file_download_failure = on_file_download_failure
        super().__init__(destination_hash, page_path, self.on_download_success, self.on_download_failure, on_progress_update, timeout, auto_download)

    # file download was successful, decode the response and send to provided callback
    def on_download_success(self, response):
        file_name: str = response[0]
        file_data: bytes = response[1]
        self.on_file_download_success(file_name, file_data)

    # page download failed, send error to provided callback
    def on_download_failure(self, failure_reason):
        self.on_file_download_failure(failure_reason)


def main():

    # parse command line args
    parser = argparse.ArgumentParser(description="ReticulumWebChat")
    parser.add_argument("--host", nargs='?', default="0.0.0.0", type=str, help="The address the web server should listen on.")
    parser.add_argument("--port", nargs='?', default="8000", type=int, help="The port the web server should listen on.")
    parser.add_argument("--headless", action='store_true', help="Web browser will not automatically launch when this flag is passed.")
    parser.add_argument("--identity-file", type=str, help="Path to a Reticulum Identity file to use as your LXMF address.")
    parser.add_argument("--identity-base64", type=str, help="A base64 encoded Reticulum Identity to use as your LXMF address.")
    parser.add_argument("--generate-identity-file", type=str, help="Generates and saves a new Reticulum Identity to the provided file path and then exits.")
    parser.add_argument("--generate-identity-base64", action='store_true', help="Outputs a randomly generated Reticulum Identity as base64 and then exits.")
    parser.add_argument("--reticulum-config-dir", type=str, help="Path to a Reticulum config directory for the RNS stack to use (e.g: ~/.reticulum)")
    parser.add_argument("--storage-dir", type=str, help="Path to a directory for storing databases and config files (default: ./storage)")
    args = parser.parse_args()

    # util to generate reticulum identity and save to file without using rnid
    if args.generate_identity_file is not None:

        # do not overwrite existing files, otherwise user could lose existing keys
        if os.path.exists(args.generate_identity_file):
            print("DANGER: the provided identity file path already exists, not overwriting!")
            return

        # generate a new identity and save to provided file path
        identity = RNS.Identity(create_keys=True)
        with open(args.generate_identity_file, "wb") as file:
            file.write(identity.get_private_key())

        print("A new Reticulum Identity has been saved to: {}".format(args.generate_identity_file))
        return

    # util to generate reticulum identity as base64 without using rnid
    if args.generate_identity_base64 is True:
        identity = RNS.Identity(create_keys=True)
        print(base64.b64encode(identity.get_private_key()).decode("utf-8"))
        return

    # use provided identity, or fallback to a random one
    if args.identity_file is not None:
        identity = RNS.Identity(create_keys=False)
        identity.load(args.identity_file)
        print("Reticulum Identity <{}> has been loaded from file.".format(identity.hash.hex()))
    elif args.identity_base64 is not None:
        identity = RNS.Identity(create_keys=False)
        identity.load_private_key(base64.b64decode(args.identity_base64))
        print("Reticulum Identity <{}> has been loaded from base64.".format(identity.hash.hex()))
    else:
        identity = RNS.Identity(create_keys=True)
        print("Reticulum Identity <{}> has been randomly generated.".format(identity.hash.hex()))

    # init app
    reticulum_webchat = ReticulumWebChat(identity, args.storage_dir, args.reticulum_config_dir)
    reticulum_webchat.run(args.host, args.port, launch_browser=args.headless is False)
    
    
if __name__ == "__main__":
    main()
