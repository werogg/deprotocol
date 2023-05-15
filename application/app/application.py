import asyncio
import platform
from abc import ABC


from application.app.setup.console_setup import ConsoleSetup
from application.app.setup.logger_setup import LoggerSetup
from application.app.setup.p2p_setup import P2PNodeSetup
from application.app.setup.tor_setup import TorSetup
from application.logger.logger import Logger
from application.settings import APP_NAME
from application.settings import PROXY_HOST
from application.settings import PROXY_PORT
from application.settings import NODE_HOST
from application.settings import NODE_PORT
from application.version import APP_VERSION
from application.p2p.node import Node
from application.app.de_app import DeApp


class DeProtocol(ABC):

    def __init__(self):
        self.setups = {}

    async def on_start(self, proxy_host: str = PROXY_HOST, proxy_port: int = PROXY_PORT) -> None:
        self.setups = {
            'logger': LoggerSetup(),
            'tor': TorSetup(proxy_host, proxy_port),
            'p2p': P2PNodeSetup(NODE_HOST, NODE_PORT),
            'shell': ConsoleSetup()
        }

        for setup in self.setups.values():
            await setup.setup()

        app = DeApp(self.setups['p2p'].node, self.setups['tor'].tor_service, self.setups['shell'].shell)
        Logger.get_instance().info(f"Starting {APP_NAME} version {APP_VERSION}, running on {platform.system()}")
        await app.start()

    def on_stop(self) -> None:
        pass
