from deprotocol.app.setup.setup import SetupABC
from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.node import Node


class P2PNodeSetup(SetupABC):
    def __init__(self, deprotocol, node_host, node_port):
        self.deprotocol = deprotocol
        self.node = None
        self.node_host = node_host
        self.node_port = node_port

    def setup(self):
        # Start Node
        self.node = Node(self.deprotocol, self.node_host, self.node_port)
        self.node.start()
        Logger.get_logger().info(f"Node started correctly! Host:Port -> {self.node_host}:{self.node_port}")
