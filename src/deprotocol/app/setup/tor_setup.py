import socks

from deprotocol.app.setup.setup import SetupABC
from deprotocol.app.logger import Logger
from deprotocol.network.tor_network import TorService
from deprotocol.settings import PROXY_TYPE
from deprotocol.utils.tor_utils import TorUtils


class TorSetup(SetupABC):
    def __init__(self, deprotocol, proxy_host='127.0.0.1', proxy_port=9050):
        self.deprotocol = deprotocol
        self.tor_service = None
        self.tor_client = None
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    def setup(self):
        # Configure socks to use Tor proxy by default
        socks.setdefaultproxy(PROXY_TYPE, self.proxy_host, self.proxy_port)
        Logger.get_logger().debug(
            f'Default proxy configuration set: {PROXY_TYPE} - {self.proxy_host}:{self.proxy_port}')

        # Download and install Tor Client
        self.tor_client = TorUtils()
        self.tor_client.download_and_install()

        # Start Tor Service
        self.tor_service = TorService(9051)
        self.tor_service.start()
        Logger.get_logger().info("Tor Service started correctly!")

    def stop(self):
        self.tor_service.stop()
