import logging
import platform

import socks

APP_NAME = 'DeProtocol'
USE_CONSOLE = True
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9050
PROXY_TYPE = socks.PROXY_TYPE_SOCKS5

NODE_HOST = '127.0.0.1'
NODE_PORT = 65432

DEBUG = True

if TRACE := True:
    LOG_LEVEL = TRACE
else:
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

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
        'url': 'https://dist.torproject.org/torbrowser/12.0.5/tor-expert-bundle-12.0.5-osx-x86_64.tar.gz',
        'path': 'Contents/Resources/TorBrowser/Tor/tor',
    }
}

if system_os not in TOR_BINARIES:
    raise ValueError(f'Unsupported operating system: {system_os}')

TOR_BINARIES_URL = TOR_BINARIES[system_os]['url']
TOR_BINARIES_PATH = TOR_BINARIES[system_os]['path']
TOR_BINARIES_FILENAME = 'tor.tar.gz'
