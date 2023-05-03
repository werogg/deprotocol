# pylint: skip-file

import os
import tarfile

import requests
from tqdm import tqdm

from deprotocol.app.logger import Logger
from deprotocol.settings import BIN_DIR
from deprotocol.settings import DATA_DIR
from deprotocol.settings import TOR_BINARIES_DIR
from deprotocol.settings import TOR_BINARIES_FILENAME
from deprotocol.settings import TOR_BINARIES_URL


class TorUtils:
    @staticmethod
    def download_and_install():
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(BIN_DIR, exist_ok=True)

        if os.path.isfile(TOR_BINARIES_DIR):
            os.remove(TOR_BINARIES_DIR)
            Logger.get_logger().warning(
                'A tor installation was found in your system, if DeProtocol is not working please delete tor.tar.gz'
            )

        response = requests.get(TOR_BINARIES_URL)
        Logger.get_logger().trace(f'requests_get: Requesting tor binaries from [{TOR_BINARIES_URL}]')
        Logger.get_logger().info("Tor Client binaries downloaded")
        with open(TOR_BINARIES_DIR, 'wb') as f:
            f.write(response.content)

        try:
            with tarfile.open(TOR_BINARIES_DIR, 'r:gz') as tar:
                members = tar.getmembers()
                for member in tqdm(members):
                    tar.extract(member, path=BIN_DIR)
            Logger.get_logger().info(f'Tor Client binaries were successfully decompressed on {BIN_DIR}')
        except Exception as exc:
            Logger.get_logger().error(exc)
