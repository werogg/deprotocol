import logging
import platform
import socks

from application.utils.utils import get_free_port


APP_NAME = 'DeProtocol'
DEFAULT_LOG_LEVEL = logging.DEBUG
DEBUG = True
USE_CONSOLE = True
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9050
PROXY_TYPE = socks.PROXY_TYPE_SOCKS5

CONTROL_PORT = 9051

NODE_HOST = '127.0.0.1'
NODE_PORT = get_free_port(65432)

system_os = platform.system()

TOR_BINARIES = {
    'Windows': {
        'url': 'https://dist.torproject.org/torbrowser/12.0.5/tor-expert-bundle-12.0.5-windows-x86_64.tar.gz',
        'path': 'bin/tor/tor.exe',
    },
    'Linux': {
        'url': 'https://dist.torproject.org/torbrowser/12.0.5/tor-expert-bundle-12.0.5-linux-x86_64.tar.gz',
        'path': 'bin/tor/tor',
    },
    'Darwin': {
        'url': 'https://dist.torproject.org/torbrowser/12.0.5/tor-expert-bundle-12.0.5-macos-x86_64.tar.gz',
        'path': 'bin/tor/tor',
    }
}

if system_os not in TOR_BINARIES:
    raise ValueError(f'Unsupported operating system: {system_os}')

TOR_BINARIES_URL = TOR_BINARIES[system_os]['url']
TOR_BINARIES_PATH = TOR_BINARIES[system_os]['path']
TOR_BINARIES_FILENAME = 'tor.tar.gz'
