import logging
import platform
import threading
from abc import ABC

import socks

from application.console.simple_console import read_user_input
from application.logger.logger import Logger
from application.network.tor_network import TorService
from application.p2p.node import Node
from application.settings import APP_NAME, PROXY_HOST, PROXY_PORT, PROXY_TYPE, NODE_HOST, NODE_PORT, DEBUG, \
    DEFAULT_LOG_LEVEL
from application.tor.tor_client import TorClient
from application.version import APP_VERSION


class DeProtocol(ABC):

    def __init__(self):
        self.node = None
        self.tor_service = None
        self.tor_client = None
        self.logger = None
        self.on_start()

    def on_start(self):
        self.setup_logger()
        Logger.get_instance().info(f"Starting {APP_NAME} version {APP_VERSION}, running on {platform.system()}")

        # Configure socks to use Tor proxy by default
        socks.setdefaultproxy(PROXY_TYPE, PROXY_HOST, PROXY_PORT)
        Logger.get_instance().info(f'Default proxy configuration set: {PROXY_TYPE} - {PROXY_HOST}:{PROXY_PORT}')

        # Call setup methods for different techs
        self.setup()

        Logger.get_instance().info("Running in CONSOLE mode...")

        self.start_console()

    def setup(self):
        self.setup_tor_client()
        self.setup_tor_service()
        self.setup_p2p_node()

    def setup_logger(self):
        log_level = DEFAULT_LOG_LEVEL
        if DEBUG:
            log_level = logging.DEBUG

        # Set up logger
        self.logger = Logger(name=APP_NAME, level=log_level)
        Logger.get_instance().info(f"Logger started correctly! Status: {logging.getLevelName(log_level)}")

    def setup_tor_client(self):
        # Download and install Tor Client
        self.tor_client = TorClient()
        self.tor_client.download_and_install()

    def setup_tor_service(self):
        # Start Tor Service
        self.tor_service = TorService(9051)
        self.tor_service.start()

    def setup_p2p_node(self):
        # Start Node
        self.node = Node(NODE_HOST, NODE_PORT, onion=self.tor_service.get_address())
        self.node.start()

    def start_console(self):
        shell_thread = threading.Thread(target=read_user_input, args=(self.node, self.tor_service))
        shell_thread.start()
