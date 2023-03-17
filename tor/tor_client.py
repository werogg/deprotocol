import os
import requests
import subprocess
import tarfile
from tqdm import tqdm

from logger.logger import Logger


class TorClient:
    def __init__(self):
        self.tor_binary_url = 'https://dist.torproject.org/torbrowser/12.5a3/tor-expert-bundle-12.5a3-windows-x86_64.tar.gz'
        self.response = None
        self.process = None

    def download_and_install(self):
        if os.path.isfile('tor.tar.gz'):
            return
        response = requests.get(self.tor_binary_url)
        with open('tor.tar.gz', 'wb') as f:
            f.write(response.content)
        with tarfile.open('tor.tar.gz', 'r:gz') as tar:
            members = tar.getmembers()
            for member in tqdm(members):
                tar.extract(member, path='bin')
        Logger.get_instance().info('Tor binaries were successfully decompressed')

    def run(self):
        tor_binary_path = os.path.join(os.getcwd(), 'bin', 'tor', 'tor.exe')
        self.process = subprocess.Popen([tor_binary_path])

    def stop(self):
        self.process.kill()
