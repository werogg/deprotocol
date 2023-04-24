from deprotocol.app.setup.setup import SetupABC
from deprotocol.logger.logger import Logger
from deprotocol.p2p.node import Node


class P2PNodeSetup(SetupABC):
    def __init__(self, node_host, node_port):
        self.node = None
        self.node_host = node_host
        self.node_port = node_port

    def setup(self):
        # Start Node
        self.node = Node(self.node_host, self.node_port)
        self.node.start()
        Logger.get_logger().info(f"Node started correctly! Host:Port -> {self.node_host}:{self.node_port}")