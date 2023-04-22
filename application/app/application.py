import platform
from abc import ABC

from application.app.setup.console_setup import ConsoleSetup
from application.app.setup.logger_setup import LoggerSetup
from application.app.setup.p2p_setup import P2PNodeSetup
from application.app.setup.tor_setup import TorSetup
from application.logger.logger import Logger
from application.settings import APP_NAME
from application.settings import NODE_HOST
from application.settings import NODE_PORT
from application.version import APP_VERSION


class DeProtocol(ABC):

    def __init__(self):
        self.setups = {}
        self.on_start()

    def on_start(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.setups = {
            'logger': LoggerSetup(),
            'tor': TorSetup(proxy_host, proxy_port),
            'p2p': P2PNodeSetup(NODE_HOST, NODE_PORT),
        }

        for setup in self.setups.values():
            setup.setup()

        ConsoleSetup(self.setups['p2p'].node, self.setups['tor'].tor_service).setup()

        Logger.get_instance().info(f"Starting {APP_NAME} version {APP_VERSION}, running on {platform.system()}")

    def set_console_props(self):
        node = self.setups['p2p'].node
        tor = self.setups['tor'].tor_service
        # do something with node_connect_command and tor_get_address_command
