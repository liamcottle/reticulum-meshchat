import asyncio
import threading
import time

import RNS
import websockets
from RNS.Interfaces.Interface import Interface
from websockets import ServerConnection

from src.backend.interfaces.WebsocketClientInterface import WebsocketClientInterface


class WebsocketServerInterface(Interface):

    # TODO: required?
    DEFAULT_IFAC_SIZE = 16

    def __str__(self):
        return f"WebsocketServerInterface[{self.name}/{self.listen_ip}:{self.listen_port}]"

    def __init__(self, owner, configuration):

        super().__init__()

        self.owner = owner

        self.IN = True
        self.OUT = False
        self.HW_MTU = 262144 # 256KiB
        self.bitrate = 1_000_000_000 # 1Gbps
        self.mode = RNS.Interfaces.Interface.Interface.MODE_FULL
        self.spawned_interfaces = []

        # parse config
        ifconf = Interface.get_config_obj(configuration)
        self.name = ifconf.get("name")
        self.listen_ip = ifconf.get("listen_ip", None)
        self.listen_port = ifconf.get("listen_port", None)

        # ensure listen ip is provided
        if self.listen_ip is None:
            raise SystemError(f"listen_ip is required for interface '{self.name}'")

        # ensure listen port is provided
        if self.listen_port is None:
            raise SystemError(f"listen_port is required for interface '{self.name}'")

        # convert listen port to int
        self.listen_port = int(self.listen_port)

        # run websocket server
        thread = threading.Thread(target=asyncio.run, args=(self.serve(),))
        thread.daemon = True
        thread.start()

    # todo docs
    def received_announce(self, from_spawned=False):
        if from_spawned:
            self.ia_freq_deque.append(time.time())

    # todo docs
    def sent_announce(self, from_spawned=False):
        if from_spawned:
            self.oa_freq_deque.append(time.time())

    # called when a full packet has been received from a websocket client
    def process_incoming(self, data):

        print(f"{self} process_incoming: {data.hex()}")

        # Update our received bytes counter
        self.rxb += len(data)

        # And send the data packet to the Transport instance for processing.
        self.owner.inbound(data, self)

    # do nothing as the spawned child interface will take care of rx/tx
    def process_outgoing(self, data):
        pass

    async def serve(self):

        # handle new websocket client connections
        async def on_websocket_client_connected(websocket: ServerConnection):

            # create new child interface
            RNS.log("Accepting incoming WebSocket connection", RNS.LOG_VERBOSE)
            spawned_interface = WebsocketClientInterface(self.owner, {
                "name": f"Client on {self.name}",
                "target_host": websocket.remote_address[0],
                "target_port": str(websocket.remote_address[1]),
            }, websocket=websocket)

            # configure child interface
            spawned_interface.IN = self.IN
            spawned_interface.OUT = self.OUT
            spawned_interface.HW_MTU = self.HW_MTU
            spawned_interface.bitrate = self.bitrate
            spawned_interface.mode = self.mode
            spawned_interface.parent_interface = self
            spawned_interface.online = True

            # todo ifac?
            # todo announce rates?

            # activate child interface
            RNS.log(f"Spawned new WebsocketClientInterface: {spawned_interface}", RNS.LOG_VERBOSE)
            RNS.Transport.interfaces.append(spawned_interface)

            # associate child interface with this interface
            while spawned_interface in self.spawned_interfaces:
                self.spawned_interfaces.remove(spawned_interface)
            self.spawned_interfaces.append(spawned_interface)

            # run read loop
            await spawned_interface.read_loop()

        # run websocket server
        try:
            async with websockets.serve(on_websocket_client_connected, self.listen_ip, self.listen_port, compression=None) as server:
                self.online = True
                await server.serve_forever()
        except Exception as e:
            RNS.log(f"{self} failed with error: {e}", RNS.LOG_ERROR)

        # websocket server is no longer running, let's restart it
        # todo implement retry delay
        self.online = False
        await self.serve()


# set interface class RNS should use when importing this external interface
interface_class = WebsocketServerInterface
