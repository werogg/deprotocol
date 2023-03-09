from logger.logger import Logger
from network.tor_network import TorService
from tor.tor_client import TorClient

if __name__ == '__main__':
    logger = Logger('DeChat')
    tor_client = TorClient()
    tor_client.download_and_install()
    tor_service = TorService(9051)
    tor_service.start()
    input("Press Enter to stop Tor...")
    tor_service.stop()
