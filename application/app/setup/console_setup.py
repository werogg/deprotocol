from application.app.setup.setup import SetupABC
from application.console.simple_console import DeConsole
from application.logger.logger import Logger
from application.settings import USE_CONSOLE


class ConsoleSetup(SetupABC):

    def __init__(self, node, tor_service):
        self.shell = None
        self.node = node
        self.tor_service = tor_service

    def setup(self):
        if USE_CONSOLE:
            Logger.get_instance().warning("Running DeProtocol in CONSOLE MODE!")
            self.shell = DeConsole(self.node, self.tor_service)
            self.shell.start()
            Logger.get_instance().info("Console started correctly!")
