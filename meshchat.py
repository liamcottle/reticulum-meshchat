#!/usr/bin/env python

import argparse
import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from typing import Callable, List

import RNS
import RNS.vendor.umsgpack as msgpack
import LXMF
from LXMF import LXMRouter
from aiohttp import web, WSMessage, WSMsgType, WSCloseCode
import asyncio
import base64
import webbrowser

from peewee import SqliteDatabase
from serial.tools import list_ports

import database
from src.backend.announce_handler import AnnounceHandler
from src.backend.lxmf_message_fields import LxmfImageField, LxmfFileAttachmentsField, LxmfFileAttachment, LxmfAudioField
from src.backend.audio_call_manager import AudioCall, AudioCallManager


# NOTE: this is required to be able to pack our app with cxfreeze as an exe, otherwise it can't access bundled assets
# this returns a file path based on if we are running meshchat.py directly, or if we have packed it as an exe with cxfreeze
# https://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
def get_file_path(filename):
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


class ReticulumMeshChat:

    def __init__(self, identity: RNS.Identity, storage_dir, reticulum_config_dir):

        # when providing a custom storage_dir, files will be saved as
        # <storage_dir>/identities/<identity_hex>/
        # <storage_dir>/identities/<identity_hex>/database.db

        # if storage_dir is not provided, we will use ./storage instead
        # ./storage/identities/<identity_hex>/
        # ./storage/identities/<identity_hex>/database.db

        # ensure a storage path exists for the loaded identity
        self.storage_dir = storage_dir or os.path.join("storage")
        self.storage_path = os.path.join(self.storage_dir, "identities", identity.hash.hex())
        print("Using Storage Path: {}".format(self.storage_path))
        os.makedirs(self.storage_path, exist_ok=True)

        # define path to files based on storage path
        self.database_path = os.path.join(self.storage_path, "database.db")
        lxmf_router_path = os.path.join(self.storage_path, "lxmf_router")

        # check if database already exists, before initialization
        database_already_exists = os.path.exists(self.database_path)

        # init database
        sqlite_database = SqliteDatabase(self.database_path)
        database.database.initialize(sqlite_database)
        self.db = database.database
        self.db.connect()
        self.db.create_tables([
            database.Config,
            database.Announce,
            database.CustomDestinationDisplayName,
            database.LxmfMessage,
            database.LxmfConversationReadState,
        ])

        # init config
        self.config = Config()

        # if database already existed before init, and we don't have a previous version set, we are on version 1
        if database_already_exists and self.config.database_version.get() is None:
            self.config.database_version.set(1)

        # if database didn't already exist, it was just fully migrated when it was created, so set the current version
        if not database_already_exists:
            self.config.database_version.set(database.latest_version)

        # migrate database
        current_database_version = self.config.database_version.get()
        migrated_database_version = database.migrate(current_version=current_database_version)
        self.config.database_version.set(migrated_database_version)

        # vacuum database on start to shrink its file size
        sqlite_database.execute_sql("VACUUM")

        # lxmf messages in outbound or sending state should be marked as failed when app starts as they are no longer being processed
        (database.LxmfMessage.update(state="failed")
         .where(database.LxmfMessage.state == "outbound")
         .orwhere((database.LxmfMessage.state == "sent") & (database.LxmfMessage.method == "opportunistic"))
         .orwhere(database.LxmfMessage.state == "sending").execute())

        # init reticulum
        self.reticulum = RNS.Reticulum(reticulum_config_dir)
        self.identity = identity

        # init lxmf router
        self.message_router = LXMF.LXMRouter(identity=self.identity, storagepath=lxmf_router_path)
        self.message_router.PROCESSING_INTERVAL = 1

        # increase limit for incoming lxmf messages (received over a resource), to allow receiving larger attachments
        # the lxmf router expects delivery_per_transfer_limit to be provided in kilobytes, so we will do that...
        self.message_router.delivery_per_transfer_limit = self.config.lxmf_delivery_transfer_limit_in_bytes.get() / 1000

        # register lxmf identity
        self.local_lxmf_destination = self.message_router.register_delivery_identity(
            identity=self.identity,
            display_name=self.config.display_name.get(),
        )

        # set a callback for when an lxmf message is received
        self.message_router.register_delivery_callback(self.on_lxmf_delivery)

        # update active propagation node
        self.set_active_propagation_node(self.config.lxmf_preferred_propagation_node_destination_hash.get())

        # enable propagation node (we don't call with false if disabled, as no need to announce disabled state every launch)
        if self.config.lxmf_local_propagation_node_enabled.get():
            self.enable_local_propagation_node()

        # handle received announces based on aspect
        RNS.Transport.register_announce_handler(AnnounceHandler("call.audio", self.on_audio_call_announce_received))
        RNS.Transport.register_announce_handler(AnnounceHandler("lxmf.delivery", self.on_lxmf_announce_received))
        RNS.Transport.register_announce_handler(AnnounceHandler("lxmf.propagation", self.on_lxmf_propagation_announce_received))
        RNS.Transport.register_announce_handler(AnnounceHandler("nomadnetwork.node", self.on_nomadnet_node_announce_received))

        # remember websocket clients
        self.websocket_clients: List[web.WebSocketResponse] = []

        # register audio call identity
        self.audio_call_manager = AudioCallManager(identity=self.identity)
        self.audio_call_manager.register_incoming_call_callback(self.on_incoming_audio_call)

        # start background thread for auto announce loop
        thread = threading.Thread(target=asyncio.run, args=(self.announce_loop(),))
        thread.daemon = True
        thread.start()

        # start background thread for auto syncing propagation nodes
        thread = threading.Thread(target=asyncio.run, args=(self.announce_sync_propagation_nodes(),))
        thread.daemon = True
        thread.start()

    # gets app version from package.json
    def get_app_version(self) -> str:
        with open(get_file_path("package.json")) as f:
            package_json = json.load(f)
            return package_json["version"]

    # automatically announces based on user config
    async def announce_loop(self):
        while True:

            should_announce = False

            # check if auto announce is enabled
            if self.config.auto_announce_enabled.get():

                # check if we have announced recently
                last_announced_at = self.config.last_announced_at.get()
                if last_announced_at is not None:

                    # determine when next announce should be sent
                    auto_announce_interval_seconds = self.config.auto_announce_interval_seconds.get()
                    next_announce_at = last_announced_at + auto_announce_interval_seconds

                    # we should announce if current time has passed next announce at timestamp
                    if time.time() > next_announce_at:
                        should_announce = True

                else:
                    # last announced at is null, so we have never announced, lets do it now
                    should_announce = True

            # announce
            if should_announce:
                await self.announce()

            # wait 1 second before next loop
            await asyncio.sleep(1)

    # automatically syncs propagation nodes based on user config
    async def announce_sync_propagation_nodes(self):
        while True:

            should_sync = False

            # check if auto sync is enabled
            auto_sync_interval_seconds = self.config.lxmf_preferred_propagation_node_auto_sync_interval_seconds.get()
            if auto_sync_interval_seconds > 0:

                # check if we have synced recently
                last_synced_at = self.config.lxmf_preferred_propagation_node_last_synced_at.get()
                if last_synced_at is not None:

                    # determine when next sync should happen
                    next_sync_at = last_synced_at + auto_sync_interval_seconds

                    # we should sync if current time has passed next sync at timestamp
                    if time.time() > next_sync_at:
                        should_sync = True

                else:
                    # last synced at is null, so we have never synced, lets do it now
                    should_sync = True

            # sync
            if should_sync:
                await self.sync_propagation_nodes()

            # wait 1 second before next loop
            await asyncio.sleep(1)

    # uses the provided destination hash as the active propagation node
    def set_active_propagation_node(self, destination_hash: str | None):

        # set outbound propagation node
        if destination_hash is not None and destination_hash != "":
            try:
                self.message_router.set_outbound_propagation_node(bytes.fromhex(destination_hash))
            except:
                # failed to set propagation node, clear it to ensure we don't use an old one by mistake
                self.remove_active_propagation_node()
                pass

        # stop using propagation node
        else:
            self.remove_active_propagation_node()

    # stops the in progress propagation node sync
    def stop_propagation_node_sync(self):
        self.message_router.cancel_propagation_node_requests()

    # stops and removes the active propagation node
    def remove_active_propagation_node(self):
        # fixme: it's possible for internal transfer state to get stuck if we change propagation node during a sync
        # this still happens even if we cancel the propagation node requests
        # for now, the user can just manually cancel syncing in the ui if they think it's stuck...
        self.stop_propagation_node_sync()
        self.message_router.outbound_propagation_node = None

    # enables or disables the local lxmf propagation node
    def enable_local_propagation_node(self, enabled: bool = True):
        try:
            if enabled:
                self.message_router.enable_propagation()
            else:
                self.message_router.disable_propagation()
        except:
            print("failed to enable or disable propagation node")
            pass

    # handle receiving a new audio call
    def on_incoming_audio_call(self, audio_call: AudioCall):
        print("on_incoming_audio_call: {}".format(audio_call.link.hash.hex()))
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "incoming_audio_call",
        })))

    # web server has shutdown, likely ctrl+c, but if we don't do the following, the script never exits
    async def shutdown(self, app):

        # force close websocket clients
        for websocket_client in self.websocket_clients:
            await websocket_client.close(code=WSCloseCode.GOING_AWAY)

        # stop reticulum
        RNS.Transport.detach_interfaces()
        self.reticulum.exit_handler()
        RNS.exit()

    def run(self, host, port, launch_browser: bool):

        # create route table
        routes = web.RouteTableDef()

        # serve index.html
        @routes.get("/")
        async def index(request):
            return web.FileResponse(path=get_file_path("public/index.html"), headers={
                # don't allow browser to store page in cache, otherwise new app versions may get stale ui
                "Cache-Control": "no-cache, no-store",
            })

        # serve ping
        @routes.get("/api/v1/status")
        async def index(request):
            return web.json_response({
                "status": "ok",
            })

        # fetch com ports
        @routes.get("/api/v1/comports")
        async def index(request):

            comports = []
            for comport in list_ports.comports():
                comports.append({
                    "device": comport.device,
                    "product": comport.product,
                    "serial_number": comport.serial_number,
                })

            return web.json_response({
                "comports": comports,
            })

        # fetch reticulum interfaces
        @routes.get("/api/v1/reticulum/interfaces")
        async def index(request):

            interfaces = {}
            if "interfaces" in self.reticulum.config:
                interfaces = self.reticulum.config["interfaces"]

            return web.json_response({
                "interfaces": interfaces,
            })

        # enable reticulum interface
        @routes.post("/api/v1/reticulum/interfaces/enable")
        async def index(request):

            # get request data
            data = await request.json()
            interface_name = data.get('name')

            # enable interface
            if "interfaces" in self.reticulum.config:
                interface = self.reticulum.config["interfaces"][interface_name]
                if "enabled" in interface:
                    interface["enabled"] = "true"
                if "interface_enabled" in interface:
                    interface["interface_enabled"] = "true"

            # save config
            self.reticulum.config.write()

            return web.json_response({
                "message": "Interface is now enabled",
            })

        # disable reticulum interface
        @routes.post("/api/v1/reticulum/interfaces/disable")
        async def index(request):

            # get request data
            data = await request.json()
            interface_name = data.get('name')

            # disable interface
            if "interfaces" in self.reticulum.config:
                interface = self.reticulum.config["interfaces"][interface_name]
                if "enabled" in interface:
                    interface["enabled"] = "false"
                if "interface_enabled" in interface:
                    interface["interface_enabled"] = "false"

            # save config
            self.reticulum.config.write()

            return web.json_response({
                "message": "Interface is now disabled",
            })

        # delete reticulum interface
        @routes.post("/api/v1/reticulum/interfaces/delete")
        async def index(request):

            # get request data
            data = await request.json()
            interface_name = data.get('name')

            # delete interface
            if "interfaces" in self.reticulum.config:
                del self.reticulum.config["interfaces"][interface_name]

            # save config
            self.reticulum.config.write()

            return web.json_response({
                "message": "Interface has been deleted",
            })

        # add reticulum interface
        @routes.post("/api/v1/reticulum/interfaces/add")
        async def index(request):

            # get request data
            data = await request.json()
            interface_name = data.get('name')
            interface_type = data.get('type')
            allow_overwriting_interface = data.get('allow_overwriting_interface', False)

            # ensure name is provided
            if interface_name is None or interface_name == "":
                return web.json_response({
                    "message": "Name is required",
                }, status=422)

            # ensure type name provided
            if interface_type is None or interface_type == "":
                return web.json_response({
                    "message": "Type is required",
                }, status=422)

            # get existing interfaces
            interfaces = {}
            if "interfaces" in self.reticulum.config:
                interfaces = self.reticulum.config["interfaces"]

            # ensure name is not for an existing interface, to prevent overwriting
            if allow_overwriting_interface is False and interface_name in interfaces:
                return web.json_response({
                    "message": "Name is already in use by another interface",
                }, status=422)

            # get existing interface details if available
            interface_details = {}
            if interface_name in interfaces:
                interface_details = interfaces[interface_name]

            # update interface details
            interface_details["type"] = interface_type

            # if interface doesn't have enabled or interface_enabled setting already, enable it by default
            if "enabled" not in interface_details and "interface_enabled" not in interface_details:
                interface_details["interface_enabled"] = "true"

            # handle tcp client interface
            if interface_type == "TCPClientInterface":

                interface_target_host = data.get('target_host')
                interface_target_port = data.get('target_port')

                # ensure target host provided
                if interface_target_host is None or interface_target_host == "":
                    return web.json_response({
                        "message": "Target Host is required",
                    }, status=422)

                # ensure target port provided
                if interface_target_port is None or interface_target_port == "":
                    return web.json_response({
                        "message": "Target Port is required",
                    }, status=422)

                interface_details["target_host"] = data.get('target_host')
                interface_details["target_port"] = data.get('target_port')

            # handle tcp server interface
            if interface_type == "TCPServerInterface":

                interface_listen_ip = data.get('listen_ip')
                interface_listen_port = data.get('listen_port')

                # ensure listen ip provided
                if interface_listen_ip is None or interface_listen_ip == "":
                    return web.json_response({
                        "message": "Listen IP is required",
                    }, status=422)

                # ensure listen port provided
                if interface_listen_port is None or interface_listen_port == "":
                    return web.json_response({
                        "message": "Listen Port is required",
                    }, status=422)

                interface_details["listen_ip"] = data.get('listen_ip')
                interface_details["listen_port"] = data.get('listen_port')

            # handle udp interface
            if interface_type == "UDPInterface":

                interface_listen_ip = data.get('listen_ip')
                interface_listen_port = data.get('listen_port')
                interface_forward_ip = data.get('forward_ip')
                interface_forward_port = data.get('forward_port')

                # ensure listen ip provided
                if interface_listen_ip is None or interface_listen_ip == "":
                    return web.json_response({
                        "message": "Listen IP is required",
                    }, status=422)

                # ensure listen port provided
                if interface_listen_port is None or interface_listen_port == "":
                    return web.json_response({
                        "message": "Listen Port is required",
                    }, status=422)

                # ensure forward ip provided
                if interface_forward_ip is None or interface_forward_ip == "":
                    return web.json_response({
                        "message": "Forward IP is required",
                    }, status=422)

                # ensure forward port provided
                if interface_forward_port is None or interface_forward_port == "":
                    return web.json_response({
                        "message": "Forward Port is required",
                    }, status=422)

                interface_details["listen_ip"] = data.get('listen_ip')
                interface_details["listen_port"] = data.get('listen_port')
                interface_details["forward_ip"] = data.get('forward_ip')
                interface_details["forward_port"] = data.get('forward_port')

            # handle rnode interface
            if interface_type == "RNodeInterface":

                interface_port = data.get('port')
                interface_frequency = data.get('frequency')
                interface_bandwidth = data.get('bandwidth')
                interface_txpower = data.get('txpower')
                interface_spreadingfactor = data.get('spreadingfactor')
                interface_codingrate = data.get('codingrate')

                # ensure port provided
                if interface_port is None or interface_port == "":
                    return web.json_response({
                        "message": "Port is required",
                    }, status=422)

                # ensure frequency provided
                if interface_frequency is None or interface_frequency == "":
                    return web.json_response({
                        "message": "Frequency is required",
                    }, status=422)

                # ensure bandwidth provided
                if interface_bandwidth is None or interface_bandwidth == "":
                    return web.json_response({
                        "message": "Bandwidth is required",
                    }, status=422)

                # ensure txpower provided
                if interface_txpower is None or interface_txpower == "":
                    return web.json_response({
                        "message": "TX power is required",
                    }, status=422)

                # ensure spreading factor provided
                if interface_spreadingfactor is None or interface_spreadingfactor == "":
                    return web.json_response({
                        "message": "Spreading Factor is required",
                    }, status=422)

                # ensure coding rate provided
                if interface_codingrate is None or interface_codingrate == "":
                    return web.json_response({
                        "message": "Coding Rate is required",
                    }, status=422)

                interface_details["port"] = interface_port
                interface_details["frequency"] = interface_frequency
                interface_details["bandwidth"] = interface_bandwidth
                interface_details["txpower"] = interface_txpower
                interface_details["spreadingfactor"] = interface_spreadingfactor
                interface_details["codingrate"] = interface_codingrate

            # merge new interface into existing interfaces
            interfaces[interface_name] = interface_details
            self.reticulum.config["interfaces"] = interfaces

            # save config
            self.reticulum.config.write()

            if allow_overwriting_interface:
                return web.json_response({
                    "message": "Interface has been saved",
                })
            else:
                return web.json_response({
                    "message": "Interface has been added",
                })

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

        # get app info
        @routes.get("/api/v1/app/info")
        async def index(request):
            return web.json_response({
                "app_info": {
                    "version": self.get_app_version(),
                    "lxmf_version": LXMF.__version__,
                    "rns_version": RNS.__version__,
                    "storage_path": self.storage_path,
                    "database_path": self.database_path,
                    "database_file_size": os.path.getsize(self.database_path),
                    "reticulum_config_path": self.reticulum.configpath,
                    "is_connected_to_shared_instance": self.reticulum.is_connected_to_shared_instance,
                    "is_transport_enabled": self.reticulum.transport_enabled(),
                },
            })

        # get config
        @routes.get("/api/v1/config")
        async def index(request):
            return web.json_response({
                "config": self.get_config_dict(),
            })

        # update config
        @routes.patch("/api/v1/config")
        async def index(request):

            # get request body as json
            data = await request.json()

            # update config
            await self.update_config(data)

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

        # clear call history
        @routes.post("/api/v1/calls/clear-call-history")
        async def index(request):

            # delete inactive calls, which are classed as call history
            for audio_call in self.audio_call_manager.audio_calls:
                if audio_call.is_active() is False:
                    self.audio_call_manager.delete_audio_call(audio_call)

            return web.json_response({
                "message": "Call history has been cleared",
            })

        # hangup all calls
        @routes.get("/api/v1/calls/hangup-all")
        async def index(request):
            self.audio_call_manager.hangup_all()
            return web.json_response({
                "message": "All calls have been hungup",
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
            timeout_seconds = int(request.query.get("timeout", 15))

            # convert destination hash to bytes
            destination_hash = bytes.fromhex(destination_hash)

            # initiate audio call
            try:

                audio_call = await self.audio_call_manager.initiate(destination_hash, timeout_seconds)
                return web.json_response({
                    "audio_call": self.convert_audio_call_to_dict(audio_call),
                })

            except Exception as e:

                return web.json_response({
                    "message": "Call Failed: {}".format(str(e)),
                }, status=503)

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
                "message": "Call has been hungup",
            })

        # announce
        @routes.get("/api/v1/announce")
        async def index(request):

            await self.announce()

            return web.json_response({
                "message": "announcing",
            })

        # serve announces
        @routes.get("/api/v1/announces")
        async def index(request):

            # get query params
            aspect = request.query.get("aspect", None)
            identity_hash = request.query.get("identity_hash", None)
            limit = request.query.get("limit", None)

            # build announces database query
            query = database.Announce.select()

            # filter by provided aspect
            if aspect is not None:
                query = query.where(database.Announce.aspect == aspect)

            # filter by provided identity hash
            if identity_hash is not None:
                query = query.where(database.Announce.identity_hash == identity_hash)

            # limit results
            if limit is not None:
                query = query.limit(limit)

            # order announces latest to oldest
            query_results = query.order_by(database.Announce.updated_at.desc())

            # process announces
            announces = []
            for announce in query_results:
                announces.append(self.convert_db_announce_to_dict(announce))

            return web.json_response({
                "announces": announces,
            })

        # propagation node status
        @routes.get("/api/v1/lxmf/propagation-node/status")
        async def index(request):
            return web.json_response({
                "propagation_node_status": {
                    "state": self.convert_propagation_node_state_to_string(self.message_router.propagation_transfer_state),
                    "progress": self.message_router.propagation_transfer_progress * 100,  # convert to percentage
                    "messages_received": self.message_router.propagation_transfer_last_result,
                },
            })

        # sync propagation node
        @routes.get("/api/v1/lxmf/propagation-node/sync")
        async def index(request):

            # ensure propagation node is configured before attempting to sync
            if self.message_router.get_outbound_propagation_node() is None:
                return web.json_response({
                    "message": "A propagation node must be configured to sync messages.",
                }, status=400)

            # request messages from propagation node
            await self.sync_propagation_nodes()

            return web.json_response({
                "message": "Sync is starting",
            })

        # stop syncing propagation node
        @routes.get("/api/v1/lxmf/propagation-node/stop-sync")
        async def index(request):

            self.stop_propagation_node_sync()

            return web.json_response({
                "message": "Sync is stopping",
            })

        # serve propagation nodes
        @routes.get("/api/v1/lxmf/propagation-nodes")
        async def index(request):

            # get query params
            limit = request.query.get("limit", None)

            # get lxmf.propagation announces
            query = database.Announce.select().where(database.Announce.aspect == "lxmf.propagation")

            # limit results
            if limit is not None:
                query = query.limit(limit)

            # order announces latest to oldest
            query_results = query.order_by(database.Announce.updated_at.desc())

            # process announces
            lxmf_propagation_nodes = []
            for announce in query_results:

                # find an lxmf.delivery announce for the same identity hash, so we can use that as an "operater by" name
                lxmf_delivery_announce = (database.Announce.select()
                                          .where(database.Announce.aspect == "lxmf.delivery")
                                          .where(database.Announce.identity_hash == announce.identity_hash)
                                          .get_or_none())

                # find a nomadnetwork.node announce for the same identity hash, so we can use that as an "operated by" name
                nomadnetwork_node_announce = (database.Announce.select()
                                          .where(database.Announce.aspect == "nomadnetwork.node")
                                          .where(database.Announce.identity_hash == announce.identity_hash)
                                          .get_or_none())

                # get a display name from other announces belonging to the propagation nodes identity
                operator_display_name = None
                if lxmf_delivery_announce is not None and lxmf_delivery_announce.app_data is not None:
                    operator_display_name = self.parse_lxmf_display_name(lxmf_delivery_announce.app_data, None)
                elif nomadnetwork_node_announce is not None and nomadnetwork_node_announce.app_data is not None:
                    operator_display_name = self.parse_nomadnetwork_node_display_name(nomadnetwork_node_announce.app_data, None)

                # parse app_data so we can see if propagation is enabled or disabled for this node
                is_propagation_enabled = None
                per_transfer_limit = None
                propagation_node_data = self.parse_lxmf_propagation_node_app_data(announce.app_data)
                if propagation_node_data is not None:
                    is_propagation_enabled = propagation_node_data["enabled"]
                    per_transfer_limit = propagation_node_data["per_transfer_limit"]

                lxmf_propagation_nodes.append({
                    "destination_hash": announce.destination_hash,
                    "identity_hash": announce.identity_hash,
                    "operator_display_name": operator_display_name,
                    "is_propagation_enabled": is_propagation_enabled,
                    "per_transfer_limit": per_transfer_limit,
                    "created_at": announce.created_at,
                    "updated_at": announce.updated_at,
                })

            return web.json_response({
                "lxmf_propagation_nodes": lxmf_propagation_nodes,
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

        # get custom destination display name
        @routes.get("/api/v1/destination/{destination_hash}/custom-display-name")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            return web.json_response({
                "custom_display_name": self.get_custom_destination_display_name(destination_hash),
            })

        # set custom destination display name
        @routes.post("/api/v1/destination/{destination_hash}/custom-display-name/update")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # get request data
            data = await request.json()
            display_name = data.get('display_name')

            # update display name if provided
            if len(display_name) > 0:
                self.db_upsert_custom_destination_display_name(destination_hash, display_name)
                return web.json_response({
                    "message": "Custom display name has been updated",
                })

            # otherwise remove display name
            else:
                database.CustomDestinationDisplayName.delete().where(database.CustomDestinationDisplayName.destination_hash == destination_hash).execute()
                return web.json_response({
                    "message": "Custom display name has been removed",
                })

        # get interface stats
        @routes.get("/api/v1/interface-stats")
        async def index(request):

            # get interface stats
            interface_stats = self.reticulum.get_interface_stats()

            # ensure transport_id is hex as json_response can't serialize bytes
            if "transport_id" in interface_stats:
                interface_stats["transport_id"] = interface_stats["transport_id"].hex()

            # ensure ifac_signature is hex as json_response can't serialize bytes
            for interface in interface_stats["interfaces"]:

                # add interface hashes
                interface_instance = self.find_interface_by_name(interface["name"])
                if interface_instance is not None:
                    interface["type"] = type(interface_instance).__name__
                    interface["hash"] = interface_instance.get_hash().hex()
                    interface["interface_name"] = interface_instance.name
                    if hasattr(interface_instance, "parent_interface") and interface_instance.parent_interface is not None:
                        interface["parent_interface_name"] = str(interface_instance.parent_interface)
                        interface["parent_interface_hash"] = interface_instance.parent_interface.get_hash().hex()

                if "ifac_signature" in interface and interface["ifac_signature"]:
                    interface["ifac_signature"] = interface["ifac_signature"].hex()

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

        # send lxmf message
        @routes.post("/api/v1/lxmf-messages/send")
        async def index(request):

            # get request body as json
            data = await request.json()

            # get data from json
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

            # parse audio field
            audio_field = None
            if "audio" in fields:
                audio_mode = data["lxmf_message"]["fields"]["audio"]["audio_mode"]
                audio_bytes = base64.b64decode(data["lxmf_message"]["fields"]["audio"]["audio_bytes"])
                audio_field = LxmfAudioField(audio_mode, audio_bytes)

            # parse file attachments field
            file_attachments_field = None
            if "file_attachments" in fields:

                file_attachments = []
                for file_attachment in data["lxmf_message"]["fields"]["file_attachments"]:
                    file_name = file_attachment["file_name"]
                    file_bytes = base64.b64decode(file_attachment["file_bytes"])
                    file_attachments.append(LxmfFileAttachment(file_name, file_bytes))

                file_attachments_field = LxmfFileAttachmentsField(file_attachments)

            try:

                # send lxmf message to destination
                lxmf_message = await self.send_message(
                    destination_hash=destination_hash,
                    content=content,
                    image_field=image_field,
                    audio_field=audio_field,
                    file_attachments_field=file_attachments_field
                )

                return web.json_response({
                    "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
                })

            except Exception as e:
                return web.json_response({
                    "message": "Sending Failed: {}".format(str(e)),
                }, status=503)

        # delete lxmf message
        @routes.delete("/api/v1/lxmf-messages/{hash}")
        async def index(request):

            # get path params
            hash = request.match_info.get("hash", None)

            # hash is required
            if hash is None:
                return web.json_response({
                    "message": "hash is required",
                }, status=422)

            # delete lxmf messages from db where hash matches
            database.LxmfMessage.delete().where((database.LxmfMessage.hash == hash)).execute()

            return web.json_response({
                "message": "ok",
            })

        # serve lxmf messages for conversation
        @routes.get("/api/v1/lxmf-messages/conversation/{destination_hash}")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")
            order = request.query.get("order", "asc")
            count = request.query.get("count")
            after_id = request.query.get("after_id")

            # get source hash from local lxmf destination
            source_hash = self.local_lxmf_destination.hash.hex()

            # get lxmf messages from db where "source to destination" or "destination to source" and ordered by oldest to newest
            db_lxmf_messages = (database.LxmfMessage.select()
                     .where((database.LxmfMessage.source_hash == source_hash) & (database.LxmfMessage.destination_hash == destination_hash))
                     .orwhere((database.LxmfMessage.destination_hash == source_hash) & (database.LxmfMessage.source_hash == destination_hash))
                     .order_by(database.LxmfMessage.id.asc() if order == "asc" else database.LxmfMessage.id.desc()))

            # limit how many messages to return
            if count is not None:
                db_lxmf_messages = db_lxmf_messages.limit(count)

            # only get records after provided id, based on query order
            if after_id is not None:
                if order == "asc":
                    db_lxmf_messages = db_lxmf_messages.where((database.LxmfMessage.id > after_id))
                else:
                    db_lxmf_messages = db_lxmf_messages.where((database.LxmfMessage.id < after_id))

            # convert to response json
            lxmf_messages = []
            for db_lxmf_message in db_lxmf_messages:
                lxmf_messages.append(self.convert_db_lxmf_message_to_dict(db_lxmf_message))

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

        # get unqiue lxmf conversations
        @routes.get("/api/v1/lxmf/conversations")
        async def index(request):

            # sql query to fetch unique source/destination hash pairs ordered by the most recently updated message
            query = """
            WITH NormalizedMessages AS (
                SELECT
                    CASE WHEN source_hash < destination_hash THEN source_hash ELSE destination_hash END AS normalized_source,
                    CASE WHEN source_hash < destination_hash THEN destination_hash ELSE source_hash END AS normalized_destination,
                    MAX(created_at) AS most_recent_created_at
                FROM lxmf_messages
                GROUP BY normalized_source, normalized_destination
            )
            SELECT
                normalized_source AS source_hash,
                normalized_destination AS destination_hash,
                most_recent_created_at
            FROM NormalizedMessages
            ORDER BY most_recent_created_at DESC;
            """

            # execute sql query
            cursor = database.database.execute_sql(query)

            # parse results to get a list of conversations we have sent or received a message from
            conversations = []
            for row in cursor.fetchall():

                # get data from row
                source_hash = row[0]
                destination_hash = row[1]
                created_at = row[2]

                # determine destination hash of other user
                if source_hash == self.local_lxmf_destination.hexhash:
                    other_user_hash = destination_hash
                else:
                    other_user_hash = source_hash

                # add to conversations
                conversations.append({
                    "display_name": self.get_lxmf_conversation_name(other_user_hash),
                    "custom_display_name": self.get_custom_destination_display_name(other_user_hash),
                    "destination_hash": other_user_hash,
                    "is_unread": self.is_lxmf_conversation_unread(other_user_hash),
                    "failed_messages_count": self.lxmf_conversation_failed_messages_count(other_user_hash),
                    # we say the conversation was updated when the latest message was created
                    # otherwise this will go crazy when sending a message, as the updated_at on the latest message changes very frequently
                    "updated_at": created_at,
                })

            return web.json_response({
                "conversations": conversations,
            })

        # mark lxmf conversation as read
        @routes.get("/api/v1/lxmf/conversations/{destination_hash}/mark-as-read")
        async def index(request):

            # get path params
            destination_hash = request.match_info.get("destination_hash", "")

            # mark lxmf conversation as read
            self.db_mark_lxmf_conversation_as_read(destination_hash)

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
        app = web.Application(client_max_size=1024 * 1024 * 50)  # allow uploading files up to 50mb
        app.add_routes(routes)
        app.add_routes([web.static('/', get_file_path("public/"))])  # serve anything in public folder
        app.on_shutdown.append(self.shutdown)  # need to force close websockets and stop reticulum now
        app.on_startup.append(on_startup)
        web.run_app(app, host=host, port=port)

    # handle announcing
    async def announce(self):

        # update last announced at timestamp
        self.config.last_announced_at.set(int(time.time()))

        # send announce for lxmf (ensuring name is updated before announcing)
        self.local_lxmf_destination.display_name = self.config.display_name.get()
        self.message_router.announce(destination_hash=self.local_lxmf_destination.hash)

        # send announce for local propagation node (if enabled)
        if self.config.lxmf_local_propagation_node_enabled.get():
            self.message_router.announce_propagation_node()

        # send announce for audio call
        self.audio_call_manager.announce(app_data=self.config.display_name.get().encode("utf-8"))

        # tell websocket clients we just announced
        await self.send_announced_to_websocket_clients()

    # handle syncing propagation nodes
    async def sync_propagation_nodes(self):

        # update last synced at timestamp
        self.config.lxmf_preferred_propagation_node_last_synced_at.set(int(time.time()))

        # request messages from propagation node
        self.message_router.request_messages_from_propagation_node(self.identity)

        # send config to websocket clients (used to tell ui last synced at)
        await self.send_config_to_websocket_clients()

    async def update_config(self, data):

        # update display name in config
        if "display_name" in data and data["display_name"] != "":
            self.config.display_name.set(data["display_name"])

        # update auto announce interval
        if "auto_announce_interval_seconds" in data:

            # auto auto announce interval
            auto_announce_interval_seconds = int(data["auto_announce_interval_seconds"])
            self.config.auto_announce_interval_seconds.set(data["auto_announce_interval_seconds"])

            # enable or disable auto announce based on interval
            if auto_announce_interval_seconds > 0:
                self.config.auto_announce_enabled.set(True)
            else:
                self.config.auto_announce_enabled.set(False)

        if "auto_resend_failed_messages_when_announce_received" in data:
            value = bool(data["auto_resend_failed_messages_when_announce_received"])
            self.config.auto_resend_failed_messages_when_announce_received.set(value)

        if "allow_auto_resending_failed_messages_with_attachments" in data:
            value = bool(data["allow_auto_resending_failed_messages_with_attachments"])
            self.config.allow_auto_resending_failed_messages_with_attachments.set(value)

        if "auto_send_failed_messages_to_propagation_node" in data:
            value = bool(data["auto_send_failed_messages_to_propagation_node"])
            self.config.auto_send_failed_messages_to_propagation_node.set(value)

        if "show_suggested_community_interfaces" in data:
            value = bool(data["show_suggested_community_interfaces"])
            self.config.show_suggested_community_interfaces.set(value)

        if "lxmf_preferred_propagation_node_destination_hash" in data:

            # update config value
            value = data["lxmf_preferred_propagation_node_destination_hash"]
            self.config.lxmf_preferred_propagation_node_destination_hash.set(value)

            # update active propagation node
            self.set_active_propagation_node(value)

        # update auto sync interval
        if "lxmf_preferred_propagation_node_auto_sync_interval_seconds" in data:
            value = int(data["lxmf_preferred_propagation_node_auto_sync_interval_seconds"])
            self.config.lxmf_preferred_propagation_node_auto_sync_interval_seconds.set(value)

        if "lxmf_local_propagation_node_enabled" in data:

            # update config value
            value = bool(data["lxmf_local_propagation_node_enabled"])
            self.config.lxmf_local_propagation_node_enabled.set(value)

            # enable or disable local propagation node
            self.enable_local_propagation_node(value)

        # send config to websocket clients
        await self.send_config_to_websocket_clients()

    # handle data received from websocket client
    async def on_websocket_data_received(self, client, data):

        # get type from client data
        _type = data["type"]

        # handle updating config
        if _type == "config.set":

            # get config from websocket
            config = data["config"]

            # update config
            await self.update_config(config)

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
                asyncio.create_task(client.send_str(json.dumps({
                    "type": "nomadnet.file.download",
                    "nomadnet_file_download": {
                        "status": "failure",
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
            downloader = NomadnetFileDownloader(destination_hash, file_path, on_file_download_success, on_file_download_failure, on_file_download_progress)
            await downloader.download()

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
                asyncio.create_task(client.send_str(json.dumps({
                    "type": "nomadnet.page.download",
                    "nomadnet_page_download": {
                        "status": "failure",
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
            downloader = NomadnetPageDownloader(destination_hash, page_path, on_page_download_success, on_page_download_failure, on_page_download_progress)
            await downloader.download()

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

    # broadcasts to all websocket clients that we just announced
    async def send_announced_to_websocket_clients(self):
        await self.websocket_broadcast(json.dumps({
            "type": "announced",
        }))

    # returns a dictionary of config
    def get_config_dict(self):
        return {
            "display_name": self.config.display_name.get(),
            "identity_hash": self.identity.hexhash,
            "lxmf_address_hash": self.local_lxmf_destination.hexhash,
            "audio_call_address_hash": self.audio_call_manager.audio_call_receiver.destination.hexhash,
            "auto_announce_enabled": self.config.auto_announce_enabled.get(),
            "auto_announce_interval_seconds": self.config.auto_announce_interval_seconds.get(),
            "last_announced_at": self.config.last_announced_at.get(),
            "auto_resend_failed_messages_when_announce_received": self.config.auto_resend_failed_messages_when_announce_received.get(),
            "allow_auto_resending_failed_messages_with_attachments": self.config.allow_auto_resending_failed_messages_with_attachments.get(),
            "auto_send_failed_messages_to_propagation_node": self.config.auto_send_failed_messages_to_propagation_node.get(),
            "show_suggested_community_interfaces": self.config.show_suggested_community_interfaces.get(),
            "lxmf_local_propagation_node_enabled": self.config.lxmf_local_propagation_node_enabled.get(),
            "lxmf_local_propagation_node_address_hash": self.message_router.propagation_destination.hexhash,
            "lxmf_preferred_propagation_node_destination_hash": self.config.lxmf_preferred_propagation_node_destination_hash.get(),
            "lxmf_preferred_propagation_node_auto_sync_interval_seconds": self.config.lxmf_preferred_propagation_node_auto_sync_interval_seconds.get(),
            "lxmf_preferred_propagation_node_last_synced_at": self.config.lxmf_preferred_propagation_node_last_synced_at.get(),
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
        remote_destination_hash_hex = None
        if remote_identity is not None:
            remote_destination_hash = RNS.Destination.hash(remote_identity, "call", "audio")
            remote_destination_hash_hex = remote_destination_hash.hex()

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
            "remote_destination_hash": remote_destination_hash_hex,
            "remote_identity_hash": remote_identity_hash,
            "is_active": audio_call.is_active(),
            "is_outbound": audio_call.is_outbound,
            "path": path,
        }

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

            # handle audio field
            if field_type == LXMF.FIELD_AUDIO:
                audio_mode = value[0]
                audio_bytes = base64.b64encode(value[1]).decode("utf-8")
                fields["audio"] = {
                    "audio_mode": audio_mode,
                    "audio_bytes": audio_bytes,
                }

        # convert 0.0-1.0 progress to 0.00-100 percentage
        progress_percentage = round(lxmf_message.progress * 100, 2)

        # get rssi
        rssi = lxmf_message.rssi
        if rssi is None:
            rssi = self.reticulum.get_packet_rssi(lxmf_message.hash)

        # get snr
        snr = lxmf_message.snr
        if snr is None:
            snr = self.reticulum.get_packet_snr(lxmf_message.hash)

        # get quality
        quality = lxmf_message.q
        if quality is None:
            quality = self.reticulum.get_packet_q(lxmf_message.hash)

        return {
            "hash": lxmf_message.hash.hex(),
            "source_hash": lxmf_message.source_hash.hex(),
            "destination_hash": lxmf_message.destination_hash.hex(),
            "is_incoming": lxmf_message.incoming,
            "state": self.convert_lxmf_state_to_string(lxmf_message),
            "progress": progress_percentage,
            "method": self.convert_lxmf_method_to_string(lxmf_message),
            "delivery_attempts": lxmf_message.delivery_attempts,
            "next_delivery_attempt_at": getattr(lxmf_message, "next_delivery_attempt", None),  # attribute may not exist yet
            "title": lxmf_message.title.decode('utf-8'),
            "content": lxmf_message.content.decode('utf-8'),
            "fields": fields,
            "timestamp": lxmf_message.timestamp,
            "rssi": rssi,
            "snr": snr,
            "quality": quality,
        }

    # convert lxmf state to a human friendly string
    def convert_lxmf_state_to_string(self, lxmf_message: LXMF.LXMessage):

        # convert state to string
        lxmf_message_state = "unknown"
        if lxmf_message.state == LXMF.LXMessage.GENERATING:
            lxmf_message_state = "generating"
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

    # convert lxmf method to a human friendly string
    def convert_lxmf_method_to_string(self, lxmf_message: LXMF.LXMessage):

        # convert method to string
        lxmf_message_method = "unknown"
        if lxmf_message.method == LXMF.LXMessage.OPPORTUNISTIC:
            lxmf_message_method = "opportunistic"
        elif lxmf_message.method == LXMF.LXMessage.DIRECT:
            lxmf_message_method = "direct"
        elif lxmf_message.method == LXMF.LXMessage.PROPAGATED:
            lxmf_message_method = "propagated"
        elif lxmf_message.method == LXMF.LXMessage.PAPER:
            lxmf_message_method = "paper"

        return lxmf_message_method

    def convert_propagation_node_state_to_string(self, state):

        # map states to strings
        state_map = {
            LXMRouter.PR_IDLE: "idle",
            LXMRouter.PR_PATH_REQUESTED: "path_requested",
            LXMRouter.PR_LINK_ESTABLISHING: "link_establishing",
            LXMRouter.PR_LINK_ESTABLISHED: "link_established",
            LXMRouter.PR_REQUEST_SENT: "request_sent",
            LXMRouter.PR_RECEIVING: "receiving",
            LXMRouter.PR_RESPONSE_RECEIVED: "response_received",
            LXMRouter.PR_COMPLETE: "complete",
            LXMRouter.PR_NO_PATH: "no_path",
            LXMRouter.PR_LINK_FAILED: "link_failed",
            LXMRouter.PR_TRANSFER_FAILED: "transfer_failed",
            LXMRouter.PR_NO_IDENTITY_RCVD: "no_identity_received",
            LXMRouter.PR_NO_ACCESS: "no_access",
            LXMRouter.PR_FAILED: "failed",
        }

        # return string for state, or fallback to unknown
        if state in state_map:
            return state_map[state]
        else:
            return "unknown"

    # convert database announce to a dictionary
    def convert_db_announce_to_dict(self, announce: database.Announce):

        # parse display name from announce
        display_name = None
        if announce.aspect == "lxmf.delivery":
            display_name = self.parse_lxmf_display_name(announce.app_data)
        elif announce.aspect == "nomadnetwork.node":
            display_name = self.parse_nomadnetwork_node_display_name(announce.app_data)

        return {
            "id": announce.id,
            "destination_hash": announce.destination_hash,
            "aspect": announce.aspect,
            "identity_hash": announce.identity_hash,
            "identity_public_key": announce.identity_public_key,
            "app_data": announce.app_data,
            "display_name": display_name,
            "custom_display_name": self.get_custom_destination_display_name(announce.destination_hash),
            "created_at": announce.created_at,
            "updated_at": announce.updated_at,
        }

    # convert database lxmf message to a dictionary
    def convert_db_lxmf_message_to_dict(self, db_lxmf_message: database.LxmfMessage):

        return {
            "id": db_lxmf_message.id,
            "hash": db_lxmf_message.hash,
            "source_hash": db_lxmf_message.source_hash,
            "destination_hash": db_lxmf_message.destination_hash,
            "is_incoming": db_lxmf_message.is_incoming,
            "state": db_lxmf_message.state,
            "progress": db_lxmf_message.progress,
            "method": db_lxmf_message.method,
            "delivery_attempts": db_lxmf_message.delivery_attempts,
            "next_delivery_attempt_at": db_lxmf_message.next_delivery_attempt_at,
            "title": db_lxmf_message.title,
            "content": db_lxmf_message.content,
            "fields": json.loads(db_lxmf_message.fields),
            "timestamp": db_lxmf_message.timestamp,
            "rssi": db_lxmf_message.rssi,
            "snr": db_lxmf_message.snr,
            "quality": db_lxmf_message.quality,
            "created_at": db_lxmf_message.created_at,
            "updated_at": db_lxmf_message.updated_at,
        }

    # handle an lxmf delivery from reticulum
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_delivery(self, lxmf_message: LXMF.LXMessage):
        try:

            # upsert lxmf message to database
            self.db_upsert_lxmf_message(lxmf_message)

            # find message from database
            db_lxmf_message = database.LxmfMessage.get_or_none(database.LxmfMessage.hash == lxmf_message.hash.hex())
            if db_lxmf_message is None:
                return

            # send received lxmf message data to all websocket clients
            asyncio.run(self.websocket_broadcast(json.dumps({
                "type": "lxmf.delivery",
                "lxmf_message": self.convert_db_lxmf_message_to_dict(db_lxmf_message),
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

        # check if this failed message should fall back to sending via a propagation node
        if lxmf_message.state == LXMF.LXMessage.FAILED and hasattr(lxmf_message, "try_propagation_on_fail") and lxmf_message.try_propagation_on_fail:
            self.send_failed_message_via_propagation_node(lxmf_message)

        # update state
        self.on_lxmf_sending_state_updated(lxmf_message)

    # sends a previously failed message via a propagation node
    def send_failed_message_via_propagation_node(self, lxmf_message: LXMF.LXMessage):

        # reset internal message state
        lxmf_message.packed = None
        lxmf_message.delivery_attempts = 0
        if hasattr(lxmf_message, "next_delivery_attempt"):
            del lxmf_message.next_delivery_attempt

        # this message should now be sent via a propagation node
        lxmf_message.desired_method = LXMF.LXMessage.PROPAGATED
        lxmf_message.try_propagation_on_fail = False

        # resend message
        self.message_router.handle_outbound(lxmf_message)

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
            "method": lxmf_message_dict["method"],
            "delivery_attempts": lxmf_message_dict["delivery_attempts"],
            "next_delivery_attempt_at": lxmf_message_dict["next_delivery_attempt_at"],
            "title": lxmf_message_dict["title"],
            "content": lxmf_message_dict["content"],
            "fields": json.dumps(lxmf_message_dict["fields"]),
            "timestamp": lxmf_message_dict["timestamp"],
            "rssi": lxmf_message_dict["rssi"],
            "snr": lxmf_message_dict["snr"],
            "quality": lxmf_message_dict["quality"],
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.LxmfMessage.insert(data)
        query = query.on_conflict(conflict_target=[database.LxmfMessage.hash], update=data)
        query.execute()

    # upserts the provided announce to the database
    def db_upsert_announce(self, identity: RNS.Identity, destination_hash: bytes, aspect: str, app_data: bytes):

        # prepare data to insert or update
        data = {
            "destination_hash": destination_hash.hex(),
            "aspect": aspect,
            "identity_hash": identity.hash.hex(),
            "identity_public_key": base64.b64encode(identity.get_public_key()).decode("utf-8"),
            "updated_at": datetime.now(timezone.utc),
        }

        # only set app data if provided, as we don't want to wipe existing data when we request keys from the network
        if app_data is not None:
            # save app data as base64 string
            data["app_data"] = base64.b64encode(app_data).decode("utf-8")

        # upsert to database
        query = database.Announce.insert(data)
        query = query.on_conflict(conflict_target=[database.Announce.destination_hash], update=data)
        query.execute()

    # upserts a custom destination display name to the database
    def db_upsert_custom_destination_display_name(self, destination_hash: str, display_name: str):

        # prepare data to insert or update
        data = {
            "destination_hash": destination_hash,
            "display_name": display_name,
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.CustomDestinationDisplayName.insert(data)
        query = query.on_conflict(conflict_target=[database.CustomDestinationDisplayName.destination_hash], update=data)
        query.execute()

    # upserts lxmf conversation read state to the database
    def db_mark_lxmf_conversation_as_read(self, destination_hash: str):

        # prepare data to insert or update
        data = {
            "destination_hash": destination_hash,
            "last_read_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        # upsert to database
        query = database.LxmfConversationReadState.insert(data)
        query = query.on_conflict(conflict_target=[database.LxmfConversationReadState.destination_hash], update=data)
        query.execute()

    # handle sending an lxmf message to reticulum
    async def send_message(self, destination_hash: str, content: str,
                           image_field: LxmfImageField = None,
                           audio_field: LxmfAudioField = None,
                           file_attachments_field: LxmfFileAttachmentsField = None) -> LXMF.LXMessage:

        # convert destination hash to bytes
        destination_hash = bytes.fromhex(destination_hash)

        # determine when to timeout finding path
        timeout_after_seconds = time.time() + 10

        # check if we have a path to the destination
        if not RNS.Transport.has_path(destination_hash):

            # we don't have a path, so we need to request it
            RNS.Transport.request_path(destination_hash)

            # wait until we have a path, or give up after the configured timeout
            while not RNS.Transport.has_path(destination_hash) and time.time() < timeout_after_seconds:
                await asyncio.sleep(0.1)

        # find destination identity from hash
        destination_identity = RNS.Identity.recall(destination_hash)
        if destination_identity is None:

            # we have to bail out of sending, since we don't have the identity/path yet
            raise Exception("Could not find path to destination. Try again later.")

        # create destination for recipients lxmf delivery address
        lxmf_destination = RNS.Destination(destination_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery")

        # send messages over a direct link by default
        desired_delivery_method = LXMF.LXMessage.DIRECT
        if not self.message_router.delivery_link_available(destination_hash) and RNS.Identity.current_ratchet_id(destination_hash) != None:
            # since there's no link established to the destination, it's faster to send opportunistically
            # this is because it takes several packets to establish a link, and then we still have to send the message over it
            # oppotunistic mode will send the message in a single packet (if the message is small enough, otherwise it falls back to a direct link)
            # we will only do this if an encryption ratchet is available, so single packet delivery is more secure
            desired_delivery_method = LXMF.LXMessage.OPPORTUNISTIC

        # create lxmf message
        lxmf_message = LXMF.LXMessage(lxmf_destination, self.local_lxmf_destination, content, desired_method=desired_delivery_method)
        lxmf_message.try_propagation_on_fail = self.config.auto_send_failed_messages_to_propagation_node.get()

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

        # add audio field
        if audio_field is not None:
            lxmf_message.fields[LXMF.FIELD_AUDIO] = [
                audio_field.audio_mode,
                audio_field.audio_bytes,
            ]

        # register delivery callbacks
        lxmf_message.register_delivery_callback(self.on_lxmf_sending_state_updated)
        lxmf_message.register_failed_callback(self.on_lxmf_sending_failed)

        # send lxmf message to be routed to destination
        self.message_router.handle_outbound(lxmf_message)

        # upsert lxmf message to database
        self.db_upsert_lxmf_message(lxmf_message)

        # tell all websocket clients that old failed message was deleted so it can remove from ui
        await self.websocket_broadcast(json.dumps({
            "type": "lxmf_message_created",
            "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
        }))

        # handle lxmf message progress loop without blocking or awaiting
        # otherwise other incoming websocket packets will not be processed until sending is complete
        # which results in the next message not showing up until the first message is finished
        asyncio.create_task(self.handle_lxmf_message_progress(lxmf_message))

        return lxmf_message

    # updates lxmf message in database and broadcasts to websocket until it's delivered, or it fails
    async def handle_lxmf_message_progress(self, lxmf_message):

        # FIXME: there's no register_progress_callback on the lxmf message, so manually send progress until delivered, propagated or failed
        # we also can't use on_lxmf_sending_state_updated method to do this, because of async/await issues...
        should_update_message = True
        while should_update_message:

            # wait 1 second between sending updates
            await asyncio.sleep(1)

            # upsert lxmf message to database (as we want to update the progress in database too)
            self.db_upsert_lxmf_message(lxmf_message)

            # send update to websocket clients
            await self.websocket_broadcast(json.dumps({
                "type": "lxmf_message_state_updated",
                "lxmf_message": self.convert_lxmf_message_to_dict(lxmf_message),
            }))

            # check message state
            has_delivered = lxmf_message.state == LXMF.LXMessage.DELIVERED
            has_propagated = lxmf_message.state == LXMF.LXMessage.SENT and lxmf_message.method == LXMF.LXMessage.PROPAGATED
            has_failed = lxmf_message.state == LXMF.LXMessage.FAILED

            # check if we should stop updating
            if has_delivered or has_propagated or has_failed:
                should_update_message = False

    # handle an announce received from reticulum, for an audio call address
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_audio_call_announce_received(self, aspect, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [call.audio]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, aspect, app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))

    # handle an announce received from reticulum, for an lxmf address
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_announce_received(self, aspect, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [lxmf.delivery]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, aspect, app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))

        # resend all failed messages that were intended for this destination
        if self.config.auto_resend_failed_messages_when_announce_received.get():
            asyncio.run(self.resend_failed_messages_for_destination(destination_hash.hex()))

    # handle an announce received from reticulum, for an lxmf propagation node address
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_lxmf_propagation_announce_received(self, aspect, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [lxmf.propagation]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, aspect, app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))

    # resends all messages that previously failed to send to the provided destination hash
    async def resend_failed_messages_for_destination(self, destination_hash: str):

        # get messages that failed to send to this destination
        failed_messages = (database.LxmfMessage.select()
                           .where(database.LxmfMessage.state == "failed")
                           .where(database.LxmfMessage.destination_hash == destination_hash)
                           .order_by(database.LxmfMessage.id.asc()))

        # resend failed messages
        for failed_message in failed_messages:
            try:

                # parse fields as json
                fields = json.loads(failed_message.fields)

                # parse image field
                image_field = None
                if "image" in fields:
                    image_field = LxmfImageField(fields["image"]["image_type"], base64.b64decode(fields["image"]["image_bytes"]))

                # parse audio field
                audio_field = None
                if "audio" in fields:
                    audio_field = LxmfAudioField(fields["audio"]["audio_mode"], base64.b64decode(fields["audio"]["audio_bytes"]))

                # parse file attachments field
                file_attachments_field = None
                if "file_attachments" in fields:
                    file_attachments = []
                    for file_attachment in fields["file_attachments"]:
                        file_attachments.append(LxmfFileAttachment(file_attachment["file_name"], base64.b64decode(file_attachment["file_bytes"])))
                    file_attachments_field = LxmfFileAttachmentsField(file_attachments)

                # don't resend message with attachments if not allowed
                if not self.config.allow_auto_resending_failed_messages_with_attachments.get():
                    if image_field is not None or audio_field is not None or file_attachments_field is not None:
                        print("Not resending failed message with attachments, as setting is disabled")
                        continue

                # send new message with failed message content
                await self.send_message(
                    failed_message.destination_hash,
                    failed_message.content,
                    image_field,
                    audio_field,
                    file_attachments_field,
                )

                # remove original failed message from database
                database.LxmfMessage.delete().where((database.LxmfMessage.hash == failed_message.hash)).execute()

                # tell all websocket clients that old failed message was deleted so it can remove from ui
                await self.websocket_broadcast(json.dumps({
                    "type": "lxmf_message_deleted",
                    "hash": failed_message.hash,
                }))

            except Exception as e:
                print("Error resending failed message: " + str(e))
                pass


    # handle an announce received from reticulum, for a nomadnet node
    # NOTE: cant be async, as Reticulum doesn't await it
    def on_nomadnet_node_announce_received(self, aspect, destination_hash, announced_identity, app_data):

        # log received announce
        print("Received an announce from " + RNS.prettyhexrep(destination_hash) + " for [nomadnetwork.node]")

        # upsert announce to database
        self.db_upsert_announce(announced_identity, destination_hash, aspect, app_data)

        # find announce from database
        announce = database.Announce.get_or_none(database.Announce.destination_hash == destination_hash.hex())
        if announce is None:
            return

        # send database announce to all websocket clients
        asyncio.run(self.websocket_broadcast(json.dumps({
            "type": "announce",
            "announce": self.convert_db_announce_to_dict(announce),
        })))

    # gets the custom display name a user has set for the provided destination hash
    def get_custom_destination_display_name(self, destination_hash: str):

        # get display name from database
        db_destination_display_name = database.CustomDestinationDisplayName.get_or_none(database.CustomDestinationDisplayName.destination_hash == destination_hash)
        if db_destination_display_name is not None:
            return db_destination_display_name.display_name

        return None

    # get name to show for an lxmf conversation
    # currently, this will use the app data from the most recent announce
    # TODO: we should fetch this from our contacts database, when it gets implemented, and if not found, fallback to app data
    def get_lxmf_conversation_name(self, destination_hash):

        # get lxmf.delivery announce from database for the provided destination hash
        lxmf_announce = (database.Announce.select()
                         .where(database.Announce.aspect == "lxmf.delivery")
                         .where(database.Announce.destination_hash == destination_hash)
                         .get_or_none())

        # if app data is available in database, it should be base64 encoded text that was announced
        # we will return the parsed lxmf display name as the conversation name
        if lxmf_announce is not None and lxmf_announce.app_data is not None:
            return self.parse_lxmf_display_name(app_data_base64=lxmf_announce.app_data)

        # announce did not have app data, so provide a fallback name
        return "Anonymous Peer"

    # reads the lxmf display name from the provided base64 app data
    def parse_lxmf_display_name(self, app_data_base64: str, default_value: str | None = "Anonymous Peer"):
        try:
            app_data_bytes = base64.b64decode(app_data_base64)
            return LXMF.display_name_from_app_data(app_data_bytes)
        except:
            return default_value

    # reads the nomadnetwork node display name from the provided base64 app data
    def parse_nomadnetwork_node_display_name(self, app_data_base64: str, default_value: str | None = "Anonymous Node"):
        try:
            app_data_bytes = base64.b64decode(app_data_base64)
            return app_data_bytes.decode("utf-8")
        except:
            return default_value

    # parses lxmf propagation node app data
    def parse_lxmf_propagation_node_app_data(self, app_data_base64: str):
        try:
            app_data_bytes = base64.b64decode(app_data_base64)
            data = msgpack.unpackb(app_data_bytes)
            return {
                "enabled": bool(data[0]),
                "timebase": int(data[1]),
                "per_transfer_limit": int(data[2]),
            }
        except:
            return None

    # returns true if the conversation has messages newer than the last read at timestamp
    def is_lxmf_conversation_unread(self, destination_hash):

        # get lxmf conversation read state from database for the provided destination hash
        lxmf_conversation_read_state = (database.LxmfConversationReadState.select()
                         .where(database.LxmfConversationReadState.destination_hash == destination_hash)
                         .get_or_none())

        # get most recent incoming message from destination hash
        latest_incoming_lxmf_message = (database.LxmfMessage.select()
                        .where(database.LxmfMessage.source_hash == destination_hash)
                        .order_by(database.LxmfMessage.created_at.desc())
                        .get_or_none())

        # there's no incoming message, so it can't be unread
        if latest_incoming_lxmf_message is None:
            return False

        # user has never read this conversation, so it's unread
        if lxmf_conversation_read_state is None:
            return True

        # conversation is unread if last read at is before the latest incoming message creation date
        conversation_last_read_at = datetime.strptime(lxmf_conversation_read_state.last_read_at, "%Y-%m-%d %H:%M:%S.%f%z")
        conversation_latest_message_at = datetime.strptime(latest_incoming_lxmf_message.created_at, "%Y-%m-%d %H:%M:%S.%f%z")
        return conversation_last_read_at < conversation_latest_message_at

    # returns number of messages that failed to send in a conversation
    def lxmf_conversation_failed_messages_count(self, destination_hash: str):
        return (database.LxmfMessage.select()
                .where(database.LxmfMessage.state == "failed")
                .where(database.LxmfMessage.destination_hash == destination_hash)
                .count())

    # find an interface by name
    def find_interface_by_name(self, name: str):
        for interface in RNS.Transport.interfaces:
            interface_name = str(interface)
            if name == interface_name:
                return interface

        return None

# class to manage config stored in database
class Config:

    @staticmethod
    def get(key: str, default_value=None) -> str | None:

        # get config value from database
        config_item = database.Config.get_or_none(database.Config.key == key)

        # return value if available
        if config_item is not None:
            return config_item.value

        # fallback to returning default value
        return default_value

    @staticmethod
    def set(key: str, value: str | None):

        # if none, delete the config entry
        if value is None:
            database.Config.delete().where(database.Config.key == key).execute()
            return

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

        def __init__(self, key: str, default_value: str | None = None):
            self.key = key
            self.default_value = default_value

        def get(self, default_value: str = None) -> str | None:
            _default_value = default_value or self.default_value
            return Config.get(self.key, default_value=_default_value)

        def set(self, value: str | None):
            Config.set(self.key, value)

    # handle config values that should be bools
    class BoolConfig:

        def __init__(self, key: str, default_value: bool = False):
            self.key = key
            self.default_value = default_value

        def get(self) -> bool:

            # get string value, or return default
            config_value = Config.get(self.key, default_value=None)
            if config_value is None:
                return self.default_value

            return config_value == "true"

        def set(self, value: bool):

            # determine string value for bool
            if value is True:
                config_value = "true"
            else:
                config_value = "false"

            Config.set(self.key, config_value)

    # handle config values that should be integers
    class IntConfig:

        def __init__(self, key: str, default_value: int | None = 0):
            self.key = key
            self.default_value = default_value

        def get(self) -> int | None:

            # get string value, or return default
            config_value = Config.get(self.key, default_value=None)
            if config_value is None:
                return self.default_value

            return int(config_value)

        def set(self, value: int):
            Config.set(self.key, str(value))

    # all possible config items
    database_version = IntConfig("database_version", None)
    display_name = StringConfig("display_name", "Anonymous Peer")
    auto_announce_enabled = BoolConfig("auto_announce_enabled", False)
    auto_announce_interval_seconds = IntConfig("auto_announce_interval_seconds", 0)
    last_announced_at = IntConfig("last_announced_at", None)
    auto_resend_failed_messages_when_announce_received = BoolConfig("auto_resend_failed_messages_when_announce_received", True)
    allow_auto_resending_failed_messages_with_attachments = BoolConfig("allow_auto_resending_failed_messages_with_attachments", False)
    auto_send_failed_messages_to_propagation_node = BoolConfig("auto_send_failed_messages_to_propagation_node", False)
    show_suggested_community_interfaces = BoolConfig("show_suggested_community_interfaces", True)
    lxmf_delivery_transfer_limit_in_bytes = IntConfig("lxmf_delivery_transfer_limit_in_bytes", 1000 * 1000 * 10)  # 10MB
    lxmf_preferred_propagation_node_destination_hash = StringConfig("lxmf_preferred_propagation_node_destination_hash", None)
    lxmf_preferred_propagation_node_auto_sync_interval_seconds = IntConfig("lxmf_preferred_propagation_node_auto_sync_interval_seconds", 0)
    lxmf_preferred_propagation_node_last_synced_at = IntConfig("lxmf_preferred_propagation_node_last_synced_at", None)
    lxmf_local_propagation_node_enabled = BoolConfig("lxmf_local_propagation_node_enabled", False)


class NomadnetDownloader:

    def __init__(self, destination_hash: bytes, path: str, on_download_success: Callable[[bytes], None], on_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None):
        self.app_name = "nomadnetwork"
        self.aspects = "node"
        self.destination_hash = destination_hash
        self.path = path
        self.timeout = timeout
        self.on_download_success = on_download_success
        self.on_download_failure = on_download_failure
        self.on_progress_update = on_progress_update

    # setup link to destination and request download
    async def download(self, path_lookup_timeout: int = 15, link_establishment_timeout: int = 15):

        # determine when to timeout
        timeout_after_seconds = time.time() + path_lookup_timeout

        # check if we have a path to the destination
        if not RNS.Transport.has_path(self.destination_hash):

            # we don't have a path, so we need to request it
            RNS.Transport.request_path(self.destination_hash)

            # wait until we have a path, or give up after the configured timeout
            while not RNS.Transport.has_path(self.destination_hash) and time.time() < timeout_after_seconds:
                await asyncio.sleep(0.1)

        # if we still don't have a path, we can't establish a link, so bail out
        if not RNS.Transport.has_path(self.destination_hash):
            self.on_download_failure("Could not find path to destination.")
            return

        # create destination to nomadnet node
        identity = RNS.Identity.recall(self.destination_hash)
        destination = RNS.Destination(
            identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            self.app_name,
            self.aspects,
        )

        # create link to destination
        link = RNS.Link(destination, established_callback=self.link_established)

        # determine when to timeout
        timeout_after_seconds = time.time() + link_establishment_timeout

        # wait until we have established a link, or give up after the configured timeout
        while link.status is not RNS.Link.ACTIVE and time.time() < timeout_after_seconds:
            await asyncio.sleep(0.1)

        # if we still haven't established a link, bail out
        if link.status is not RNS.Link.ACTIVE:
            self.on_download_failure("Could not establish link to destination.")

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

    def __init__(self, destination_hash: bytes, page_path: str, on_page_download_success: Callable[[str], None], on_page_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None):
        self.on_page_download_success = on_page_download_success
        self.on_page_download_failure = on_page_download_failure
        super().__init__(destination_hash, page_path, self.on_download_success, self.on_download_failure, on_progress_update, timeout)

    # page download was successful, decode the response and send to provided callback
    def on_download_success(self, response_bytes):
        micron_markup_response = response_bytes.decode("utf-8")
        self.on_page_download_success(micron_markup_response)

    # page download failed, send error to provided callback
    def on_download_failure(self, failure_reason):
        self.on_page_download_failure(failure_reason)


class NomadnetFileDownloader(NomadnetDownloader):

    def __init__(self, destination_hash: bytes, page_path: str, on_file_download_success: Callable[[str, bytes], None], on_file_download_failure: Callable[[str], None], on_progress_update: Callable[[float], None], timeout: int|None = None):
        self.on_file_download_success = on_file_download_success
        self.on_file_download_failure = on_file_download_failure
        super().__init__(destination_hash, page_path, self.on_download_success, self.on_download_failure, on_progress_update, timeout)

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
    parser = argparse.ArgumentParser(description="ReticulumMeshChat")
    parser.add_argument("--host", nargs='?', default="127.0.0.1", type=str, help="The address the web server should listen on.")
    parser.add_argument("--port", nargs='?', default="8000", type=int, help="The port the web server should listen on.")
    parser.add_argument("--headless", action='store_true', help="Web browser will not automatically launch when this flag is passed.")
    parser.add_argument("--identity-file", type=str, help="Path to a Reticulum Identity file to use as your LXMF address.")
    parser.add_argument("--identity-base64", type=str, help="A base64 encoded Reticulum Identity to use as your LXMF address.")
    parser.add_argument("--generate-identity-file", type=str, help="Generates and saves a new Reticulum Identity to the provided file path and then exits.")
    parser.add_argument("--generate-identity-base64", action='store_true', help="Outputs a randomly generated Reticulum Identity as base64 and then exits.")
    parser.add_argument("--reticulum-config-dir", type=str, help="Path to a Reticulum config directory for the RNS stack to use (e.g: ~/.reticulum)")
    parser.add_argument("--storage-dir", type=str, help="Path to a directory for storing databases and config files (default: ./storage)")
    parser.add_argument("--test-exception-message", type=str, help="Throws an exception. Used for testing the electron error dialog")
    parser.add_argument('args', nargs=argparse.REMAINDER)  # allow unknown command line args
    args = parser.parse_args()

    # check if we want to test exception messages
    if args.test_exception_message is not None:
        raise Exception(args.test_exception_message)

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
        print("Reticulum Identity <{}> has been loaded from file {}.".format(identity.hash.hex(), args.identity_file))
    elif args.identity_base64 is not None:
        identity = RNS.Identity(create_keys=False)
        identity.load_private_key(base64.b64decode(args.identity_base64))
        print("Reticulum Identity <{}> has been loaded from base64.".format(identity.hash.hex()))
    else:

        # ensure provided storage dir exists, or the default storage dir exists
        base_storage_dir = args.storage_dir or os.path.join("storage")
        os.makedirs(base_storage_dir, exist_ok=True)

        # configure path to default identity file
        default_identity_file = os.path.join(base_storage_dir, "identity")

        # if default identity file does not exist, generate a new identity and save it
        if not os.path.exists(default_identity_file):
            identity = RNS.Identity(create_keys=True)
            with open(default_identity_file, "wb") as file:
                file.write(identity.get_private_key())
            print("Reticulum Identity <{}> has been randomly generated and saved to {}.".format(identity.hash.hex(), default_identity_file))

        # default identity file exists, load it
        identity = RNS.Identity(create_keys=False)
        identity.load(default_identity_file)
        print("Reticulum Identity <{}> has been loaded from file {}.".format(identity.hash.hex(), default_identity_file))

    # init app
    reticulum_meshchat = ReticulumMeshChat(identity, args.storage_dir, args.reticulum_config_dir)
    reticulum_meshchat.run(args.host, args.port, launch_browser=args.headless is False)


if __name__ == "__main__":
    main()
