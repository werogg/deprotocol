import logging
import threading

from application.app.setup.setup import SetupABC
from application.console.simple_console import read_user_input
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
            shell_thread = threading.Thread(target=read_user_input, args=(self.node, self.tor_service))
            shell_thread.start()
            Logger.get_instance().info("Console started correctly!")
