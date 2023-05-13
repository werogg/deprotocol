# pylint: skip-file

import os
import tarfile
import asyncio
import aiohttp
import aiofiles

from tqdm import tqdm

from application.logger.logger import Logger
from application.settings import TOR_BINARIES_FILENAME
from application.settings import TOR_BINARIES_URL


class TorUtils():

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
