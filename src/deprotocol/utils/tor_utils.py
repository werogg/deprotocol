# pylint: skip-file

import os
import tarfile

import requests
from tqdm import tqdm

from deprotocol.app.logger import Logger
from deprotocol.settings import DATA_DIR
from deprotocol.settings import TOR_BINARIES_FILENAME
from deprotocol.settings import TOR_BINARIES_URL


class TorUtils:
    @staticmethod
    def download_and_install():
        os.makedirs(DATA_DIR, exist_ok=True)
        tor_dir = os.path.join(DATA_DIR, TOR_BINARIES_FILENAME)

        if os.path.isfile(tor_dir):
            os.remove(tor_dir)
            Logger.get_logger().warning(
                'A tor installation was found in your system, if DeProtocol is not working please delete tor.tar.gz'
            )

        response = requests.get(TOR_BINARIES_URL)
        Logger.get_logger().trace(f'requests_get: Requesting tor binaries from [{TOR_BINARIES_URL}]')
        Logger.get_logger().info("Tor Client binaries downloaded")
        with open(tor_dir, 'wb') as f:
            f.write(response.content)

        try:
            with tarfile.open(tor_dir, 'r:gz') as tar:
                members = tar.getmembers()
                for member in tqdm(members):
                    tar.extract(member, path=DATA_DIR)
            Logger.get_logger().info('Tor Client binaries were successfully decompressed')
        except Exception as exc:
            Logger.get_logger().error(exc)
