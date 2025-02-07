import threading
import time

import RNS
from RNS.Interfaces.Interface import Interface
from websockets.sync.client import connect
from websockets.sync.connection import Connection


class WebsocketClientInterface(Interface):

    # TODO: required?
    DEFAULT_IFAC_SIZE = 16

    RECONNECT_DELAY_SECONDS = 5

    def __str__(self):
        return f"WebsocketClientInterface[{self.name}/{self.target_host}:{self.target_port}]"

    def __init__(self, owner, configuration, websocket: Connection = None):

        super().__init__()

        self.owner = owner
        self.parent_interface = None

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
        self.target_type = ifconf.get("target_type", "ws")

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
            thread = threading.Thread(target=self.connect)
            thread.daemon = True
            thread.start()

    # called when a full packet has been received over the websocket
    def process_incoming(self, data):

        # do nothing if offline or detached
        if not self.online or self.detached:
            return

        # update received bytes counter
        self.rxb += len(data)

        # update received bytes counter for parent interface
        if self.parent_interface is not None:
            self.parent_interface.rxb += len(data)

        # send received data to transport instance
        self.owner.inbound(data, self)

    # the running reticulum transport instance will call this method whenever the interface must transmit a packet
    def process_outgoing(self, data):

        # do nothing if offline or detached
        if not self.online or self.detached:
            return

        # send to websocket server
        try:
            self.websocket.send(data)
        except Exception as e:
            RNS.log(f"Exception occurred while transmitting via {str(self)}", RNS.LOG_ERROR)
            RNS.log(f"The contained exception was: {str(e)}", RNS.LOG_ERROR)
            return

        # update sent bytes counter
        self.txb += len(data)

        # update received bytes counter for parent interface
        if self.parent_interface is not None:
            self.parent_interface.txb += len(data)

    # connect to the configured websocket server
    def connect(self):

        # do nothing if interface is detached
        if self.detached:
            return

        # connect to websocket server
        try:
            RNS.log(f"Establishing Websocket connection for {str(self)}...", RNS.LOG_DEBUG)
            self.websocket = connect(f"{self.target_type}://{self.target_host}:{self.target_port}", max_size=None, compression=None)
            self.read_loop()
        except Exception as e:
            RNS.log(f"{self} failed with error: {e}", RNS.LOG_ERROR)

        # auto reconnect after delay
        RNS.log(f"Websocket disconnected for {str(self)}...", RNS.LOG_DEBUG)
        time.sleep(self.RECONNECT_DELAY_SECONDS)
        self.connect()

    def read_loop(self):

        self.online = True

        try:
            for message in self.websocket:
                self.process_incoming(message)
        except Exception as e:
            RNS.log(f"{self} read loop error: {e}", RNS.LOG_ERROR)

        self.online = False

    def detach(self):

        # mark as offline
        self.online = False

        # close websocket
        if self.websocket is not None:
            self.websocket.close()

        # mark as detached
        self.detached = True

# set interface class RNS should use when importing this external interface
interface_class = WebsocketClientInterface
