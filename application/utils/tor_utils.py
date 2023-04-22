# pylint: skip-file

import os
import platform
import subprocess
import tarfile

import requests
from tqdm import tqdm

from application.logger.logger import Logger
from application.settings import TOR_BINARIES_FILENAME
from application.settings import TOR_BINARIES_URL


class TorUtils:
    @staticmethod
    def download_and_install():
        if os.path.isfile(TOR_BINARIES_FILENAME):
            os.remove(TOR_BINARIES_FILENAME)
            Logger.get_instance().warning(
                'A tor installation was found in your system, if DeProtocol is not working please delete tor.tar.gz'
            )
            return
        response = requests.get(TOR_BINARIES_URL)
        Logger.get_instance().info("Tor Client binaries downloaded")
        with open('tor.tar.gz', 'wb') as f:
            f.write(response.content)

        try:
            with tarfile.open('tor.tar.gz', 'r:gz') as tar:
                members = tar.getmembers()
                for member in tqdm(members):
                    tar.extract(member, path='bin')
            Logger.get_instance().info('Tor Client binaries were successfully decompressed')
        except Exception as exc:
            Logger.get_instance().error(exc)
