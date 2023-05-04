from deprotocol.app.console.custom_console import ConsoleUI
from deprotocol.app.logger import Logger
from deprotocol.app.setup.setup import SetupABC
from deprotocol.settings import USE_CONSOLE


class ConsoleSetup(SetupABC):

    def __init__(self, deprotocol):
        self.shell = None
        self.deprotocol = deprotocol

    def setup(self):
        if USE_CONSOLE and not self.deprotocol.testing:
            Logger.get_logger().warning("Running DeProtocol in CONSOLE MODE!")
            self.shell = ConsoleUI(self.deprotocol)
            self.shell.start()
            Logger.get_logger().info("Console started correctly!")
