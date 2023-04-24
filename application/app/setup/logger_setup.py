import logging

from application.app.setup.setup import SetupABC
from application.logger.logger import Logger
from application.settings import APP_NAME, PROXY_HOST, PROXY_PORT, PROXY_TYPE, NODE_HOST, NODE_PORT, DEBUG, \
    LOG_LEVEL


class LoggerSetup(SetupABC):

    def __init__(self):
        self.logger = None

    def setup(self):
        log_level = LOG_LEVEL
        Logger.get_logger().info(f"Logger started correctly! Status: {logging.getLevelName(log_level)}")
