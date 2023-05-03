import threading

from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.handler.connection_handler import ConnectionHandler
from deprotocol.settings import NODE_PORT


class NetworkManager(threading.Thread):
    def __init__(self, deprotocol, host='', port=65432, onion_address=''):
        super().__init__()
        self.deprotocol = deprotocol
        self.terminate_flag = threading.Event()
        self.host = host
        self.port = port
        self.onion_address = onion_address
        self.node_connections = []
        self.banned_address = []
        self.connection_handler = ConnectionHandler(deprotocol, self)

    def start(self):
        self.connection_handler.start()
        super().start()

    def stop(self):
        self.connection_handler.stop()
        self.terminate_flag.set()

    def connect_to(self, address, port=NODE_PORT):
        if self.is_valid_address(address):
            node_connection = self.connection_handler.connect_to(address, port)
            self.node_connections.append(node_connection)

    def disconnect_from(self, node):
        pass

    def node_connected(self, node):
        Logger.get_logger().info(f"Connected to node: {node.connected_host}")
        if node.connected_host not in self.node_connections:
            self.node_connections.append(node.connected_host)

    def is_valid_address(self, address):
        if address is self.host or address in self.banned_address:
            return False

        for node in self.node_connections:
            if node.connected_host == self.host:
                Logger.get_logger().info("Already connected with this node.")
                return False

        return True
