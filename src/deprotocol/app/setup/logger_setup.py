import logging

from deprotocol.app.setup.setup import SetupABC
from deprotocol.logger.logger import Logger
from deprotocol.settings import LOG_LEVEL


class LoggerSetup(SetupABC):

    def __init__(self):
        self.logger = None

    def setup(self):
        log_level = LOG_LEVEL
        Logger.get_logger().info(f"Logger started correctly! Status: {logging.getLevelName(log_level)}")
