import logging

from application.app.setup.setup import SetupABC
from application.logger.logger import Logger
from application.settings import APP_NAME, DEFAULT_LOG_LEVEL


class LoggerSetup(SetupABC):

    def __init__(self):
        self.logger: Logger = None

    async def setup(self) -> None:
        log_level = DEFAULT_LOG_LEVEL

        self.logger = Logger(name=APP_NAME, level=log_level)
        Logger.get_instance().info(f"Logger started correctly! Status: {logging.getLevelName(log_level)}")
