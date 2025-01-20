import asyncio
import threading

import RNS
import websockets
from RNS.Interfaces.Interface import Interface
from websockets.asyncio.connection import Connection

from src.backend.async_utils import AsyncUtils


class WebsocketClientInterface(Interface):

    # TODO: required?
    DEFAULT_IFAC_SIZE = 16

    def __str__(self):
        return f"WebsocketClientInterface[{self.name}/{self.target_host}:{self.target_port}]"

    def __init__(self, owner, configuration, websocket: Connection = None):

        super().__init__()

        self.owner = owner

        self.IN = True
        self.OUT = False
        self.HW_MTU = 262144 # 256KiB
        self.bitrate = 1_000_000_000 # 1Gbps
        self.mode = RNS.Interfaces.Interface.Interface.MODE_FULL

        # parse config
        ifconf = Interface.get_config_obj(configuration)
        self.name = ifconf.get("name")
        self.target_host = ifconf.get("target_host", None)
        self.target_port = ifconf.get("target_port", None)

        # ensure target host is provided
        if self.target_host is None:
            raise SystemError(f"target_host is required for interface '{self.name}'")

        # ensure target port is provided
        if self.target_port is None:
            raise SystemError(f"target_port is required for interface '{self.name}'")

        # convert target port to int
        self.target_port = int(self.target_port)

        # connect to websocket server if an existing connection was not provided
        self.websocket = websocket
        if self.websocket is None:
            thread = threading.Thread(target=asyncio.run, args=(self.connect(),))
            thread.daemon = True
            thread.start()

    # called when a full packet has been received over the websocket
    def process_incoming(self, data):

        print(f"{self} process_incoming: {data.hex()}")

        # update received bytes counter
        self.rxb += len(data)

        # send received data to transport instance
        self.owner.inbound(data, self)

    # the running reticulum transport instance will call this method whenever the interface must transmit a packet
    def process_outgoing(self, data):

        # do nothing if not online
        if not self.online:
            return

        # send to websocket server
        print(f"{self} process_outgoing: {data.hex()}")
        AsyncUtils.run_async(self.websocket.send(data))

        # update sent bytes counter
        self.txb += len(data)

    # connect to the configured websocket server
    async def connect(self):

        try:
            # todo: ws:// and wss:// support in config file?
            async with websockets.connect(f"ws://{self.target_host}:{self.target_port}", max_size=None, compression=None) as websocket:
                self.websocket = websocket
                await self.read_loop()
        except Exception as e:
            RNS.log(f"{self} failed with error: {e}", RNS.LOG_ERROR)

        # todo implement reconnect delay
        await self.connect()

    async def read_loop(self):

        self.online = True

        try:
            async for message in self.websocket:
                self.process_incoming(message)
        except Exception as e:
            RNS.log(f"{self} read loop error: {e}", RNS.LOG_ERROR)

        self.online = False


# set interface class RNS should use when importing this external interface
interface_class = WebsocketClientInterface
