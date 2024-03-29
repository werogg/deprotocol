import threading

from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.network.peer_networking.network_manager import NetworkManager
from deprotocol.settings import HIDDEN_SERVICE_VIRTUAL_PORT
from deprotocol.settings import NODE_PORT


class Node:
    def __init__(self, deprotocol, host='', port=65432, onion_address=''):
        super().__init__()
        self.deprotocol = deprotocol
        self.terminate_flag = threading.Event()
        self.host = host
        self.port = port
        self.onion_address = onion_address
        self.network_manager = NetworkManager(deprotocol, host, port)
        deprotocol.node = self

    def start(self):
        self.network_manager.start()

    def stop(self):
        self.network_manager.stop()

    def connect_to(self, host, port=HIDDEN_SERVICE_VIRTUAL_PORT):
        self.network_manager.connect_to(host, port)

    def disconnect_from(self, node):
        self.network_manager.disconnect_from(node)

    def get_connected_nodes(self):
        return self.network_manager.node_connections


