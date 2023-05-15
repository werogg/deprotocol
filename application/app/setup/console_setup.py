from application.app.setup.setup import SetupABC
from application.console.simple_console import DeConsole
from application.logger.logger import Logger
from application.settings import USE_CONSOLE


class ConsoleSetup(SetupABC):

    def __init__(self):
        self.shell: DeConsole = None

    async def setup(self):
        if USE_CONSOLE:
            Logger.get_instance().warning("Running DeProtocol in CONSOLE MODE!")
            self.shell = DeConsole()
