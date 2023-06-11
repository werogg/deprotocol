import threading

from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.handler.connection_handler import ConnectionHandler
from deprotocol.settings import HIDDEN_SERVICE_VIRTUAL_PORT


class NetworkManager(threading.Thread):
    def __init__(self, deprotocol, host='', port=65432):
        super().__init__()
        self.deprotocol = deprotocol
        self.terminate_flag = threading.Event()
        self.host = host
        self.port = port
        self.node_connections = []
        self.banned_address = []
        self.connection_handler = ConnectionHandler(deprotocol, self)

    def start(self):
        self.connection_handler.start()
        super().start()

    def stop(self):
        self.connection_handler.stop()
        self.terminate_flag.set()

    def connect_to(self, address, port=HIDDEN_SERVICE_VIRTUAL_PORT):
        if self.is_valid_address(address):
            node_connection = self.connection_handler.connect_to(address, port, True)
            self.node_connections.append(node_connection)

    def disconnect_from(self, node):
        pass

    def node_connected(self, node):
        Logger.get_logger().info(f"Connected to node: {node.connected_host}")
        if node.connected_host not in self.node_connections:
            self.node_connections.append(node.connected_host)

    def is_valid_address(self, address):
        if address == self.deprotocol.node.onion_address:
            Logger.get_logger().info("You can't connect to yourself.")
            return False
        elif address in self.banned_address:
            Logger.get_logger().info("This address is banned.")
            return False

        for node in self.node_connections:
            if node.connected_address == address:
                Logger.get_logger().info("Already connected with this node.")
                return False

        return True
