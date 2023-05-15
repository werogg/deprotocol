# pylint: skip-file

import os
import tarfile
import asyncio
import aiohttp
import aiofiles

from tqdm import tqdm
import stem.control

from application.logger.logger import Logger
from application.settings import TOR_BINARIES_FILENAME
from application.settings import TOR_BINARIES_URL
from application.settings import CONTROL_PORT


class TorUtils:

    async def install(self):
        if os.path.isfile(TOR_BINARIES_FILENAME):
            os.remove(TOR_BINARIES_FILENAME)
            Logger.get_instance().warning(
                'A tor installation was found in your system, if DeProtocol is not working please delete tor.tar.gz'
            )
            return
        async with aiohttp.ClientSession() as session:
            response = await session.get(TOR_BINARIES_URL)
            result = await response.content.read()
            Logger.get_instance().info("Tor Client binaries downloaded")
            async with aiofiles.open('tor.tar.gz', 'wb') as f:
                await f.write(result)
        self.write()

    def write(self):
        try:
            with tarfile.open('tor.tar.gz', 'r:gz') as tar:
                members = tar.getmembers()
                for member in tqdm(members):
                    tar.extract(member, path='bin')
            Logger.get_instance().info('Tor Client binaries were successfully decompressed')
        except Exception as exc:
            Logger.get_instance().error(exc)

    @staticmethod
    async def establish_tor_connection(return_=False):
        try:
            tor_controller = stem.control.Controller.from_port(port=CONTROL_PORT)
            await tor_controller.authenticate()
            await tor_controller.new_circuit()
            await asyncio.sleep(0.2)
            if return_:
                return tor_controller
        except TypeError as exs:
            Logger.get_instance().error(
                """

                You are using an outdated version of stem that does not support the current functionality of the protocol. 
                Since pip does not detect the latest version of stem, install the current version in the following way:
                1. pip uninstall stem
                2. pip install git+https://github.com/torproject/stem.git
                3. restart app
                """)
            raise exs
