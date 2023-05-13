import socks

from application.app.setup.setup import SetupABC
from application.logger.logger import Logger
from application.network.tor_network import TorService
from application.settings import PROXY_TYPE
from application.utils.tor_utils import TorUtils


class TorSetup(SetupABC):
    def __init__(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.tor_service = None
        self.tor_client = None
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    async def setup(self):
        # Configure socks to use Tor proxy by default
        socks.setdefaultproxy(PROXY_TYPE, self.proxy_host, self.proxy_port)
        Logger.get_instance().info(
            f'Default proxy configuration set: {PROXY_TYPE} - {self.proxy_host}:{self.proxy_port}')

        # Download and install Tor Client
        self.tor_client = TorUtils()
        await self.tor_client.install()

        # Start Tor Service
        self.tor_service = TorService(9051)
        await self.tor_service.start()
        Logger.get_instance().info("Tor Service started correctly!")
