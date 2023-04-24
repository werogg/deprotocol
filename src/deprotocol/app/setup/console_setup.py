from deprotocol.app.setup.setup import SetupABC
from deprotocol.console.simple_console import DeConsole
from deprotocol.logger.logger import Logger
from deprotocol.settings import USE_CONSOLE


class ConsoleSetup(SetupABC):

    def __init__(self, node, tor_service):
        self.shell = None
        self.node = node
        self.tor_service = tor_service

    def setup(self):
        if USE_CONSOLE:
            Logger.get_logger().warning("Running DeProtocol in CONSOLE MODE!")
            self.shell = DeConsole(self.node, self.tor_service)
            self.shell.start()
            Logger.get_logger().info("Console started correctly!")
