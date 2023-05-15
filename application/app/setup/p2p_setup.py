from application.app.setup.setup import SetupABC
from application.logger.logger import Logger
from application.p2p.node import Node


class P2PNodeSetup(SetupABC):
    def __init__(self, node_host: str, node_port: int):
        self.node = None
        self.node_host = node_host
        self.node_port = node_port

    async def setup(self) -> None:
        self.node = Node(self.node_host, self.node_port)
        await self.node.start()
        Logger.get_instance().info(f"Node started correctly! Host:Port -> {self.node_host}:{self.node_port}")
