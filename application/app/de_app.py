# from application.console.simple_console import DeConsole
from application.network.tor_network import TorService
from application.p2p.node import Node


class DeApp:
    def __init__(self, node: Node, tor_service: TorService, shell):
        self.node = node
        self.tor_service = tor_service
        self.shell = shell

    async def start(self) -> None:
        init_shell_vars = [self, self.tor_service, self.node]
        await self.shell.start(*init_shell_vars)

