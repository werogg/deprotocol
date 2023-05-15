# pylint: skip-file

import os.path
import socket
import asyncio

import stem.util
import stem.control
import stem.process

from application.logger.logger import Logger
from application.settings import TOR_BINARIES_PATH
from application.settings import NODE_PORT
from application.settings import NODE_HOST
from application.settings import PROXY_PORT
from application.utils.tor_utils import TorUtils


class TorService:

    def __init__(self, port: int):
        self.port = port
        self.tor_process = None
        self.tor_controller = None
        self.hidden_service = None

    def set_tor_config(self) -> None:
        try:
            self.tor_process = stem.process.launch_tor_with_config(
                config={
                    'SocksPort': f'{PROXY_PORT}',  # 9050
                    'SocksPolicy': 'accept *',
                    'ControlPort': f"{self.port}",  # 9051
                    'DataDirectory': os.path.join(os.getcwd(), 'tor_data'),
                    'HiddenServiceDir': os.path.join(os.getcwd(), 'tor_hidden_service'),
                    'HiddenServicePort': f'80 {NODE_HOST}:{NODE_PORT}',  # localhost : 65432/65433
                },
                tor_cmd=os.path.join(os.getcwd(), TOR_BINARIES_PATH),
                init_msg_handler=self._print_bootstrap_lines,
                take_ownership=True
            )
        except Exception as e:
            Logger.get_instance().error(e)

    async def get_info_by_traffic(self) -> None:
        bytes_read = await self.tor_controller.get_info("traffic/read")
        bytes_written = await self.tor_controller.get_info("traffic/written")
        Logger.get_instance().info(f'Tor relay has read {bytes_read} bytes and written {bytes_written}.')

    async def create_hidden_service(self) -> None:
        self.hidden_service = await self.tor_controller.create_ephemeral_hidden_service(
            {'80': f'{NODE_HOST}:{NODE_PORT}'}, await_publication=True
        )
        Logger.get_instance().info(f"Hidden service created with address: {self.hidden_service.service_id}.onion")

    async def start(self) -> None:
        self.set_tor_config()
        await self.create_tor_session()

    async def create_tor_session(self) -> None:
        self.tor_controller = await TorUtils.establish_tor_connection(return_=True)
        await self.get_info_by_traffic()
        await self.create_hidden_service()

    async def stop(self) -> None:
        if self.tor_controller:
            await self.tor_controller.close()
            Logger.get_instance().info("Tor Service was closed successfully")
        if self.tor_process:
            self.tor_process.kill()
            Logger.get_instance().warning("Tor Service process was killed!")

    def _print_bootstrap_lines(self, line: str) -> None:
        if "Bootstrapped" in line:
            Logger.get_instance().info(line)

    def get_address(self) -> str:
        return self.hidden_service.service_id
