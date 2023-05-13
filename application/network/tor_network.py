# pylint: skip-file

import os.path
import socket
import asyncio


import stem.util
import stem.control
import stem.process


from application.logger.logger import Logger
from application.settings import TOR_BINARIES_PATH


class TorService:

    def __init__(self, port):
        self.port = port
        self.tor_process = None
        self.tor_controller = None
        self.hidden_service = None

    def set_tor_config(self):
            try:
                self.tor_process = stem.process.launch_tor_with_config(
                    config={
                        'SocksPort': '9050',
                        'SocksPolicy': 'accept *',
                        'ControlPort': str(self.port),
                        'DataDirectory': os.path.join(os.getcwd(), 'tor_data'),
                        'HiddenServiceDir': os.path.join(os.getcwd(), 'tor_hidden_service'),
                        'HiddenServicePort': '80 127.0.0.1:65432'
                    },
                    tor_cmd=os.path.join(os.getcwd(), TOR_BINARIES_PATH),
                    init_msg_handler=self._print_bootstrap_lines,
                    take_ownership=True
                )
            except Exception as e:
                Logger.get_instance().error(e)

    async def get_info_by_traffic(self):
        bytes_read = await self.tor_controller.get_info("traffic/read")
        bytes_written = await self.tor_controller.get_info("traffic/written")
        Logger.get_instance().info(f'Tor relay has read {bytes_read} bytes and written {bytes_written}.')

    async def create_hidden_service(self):
        self.hidden_service = await self.tor_controller.create_ephemeral_hidden_service(
            {'80': '127.0.0.1:65432'}, await_publication=True
        )
        Logger.get_instance().info(f"Hidden service created with address: {self.hidden_service.service_id}.onion")

    async def start(self):
        self.set_tor_config()
        await self.create_tor_session()

    async def create_tor_session(self):
        self.tor_controller = stem.control.Controller.from_port(port=self.port)
        await self.tor_controller.authenticate()
        await self.tor_controller.new_circuit()
        await self.get_info_by_traffic()
        await self.create_hidden_service()
        Logger.get_instance().info(self.tor_controller.is_alive())

    async def stop(self):
        if self.tor_controller:
            await self.tor_controller.close()
            Logger.get_instance().info("Tor Service was closed successfully")
        if self.tor_process:
            self.tor_process.kill()
            Logger.get_instance().warning("Tor Service process was killed!")

    def _print_bootstrap_lines(self, line):
        if "Bootstrapped" in line:
            Logger.get_instance().info(line)

    # unused
    def connect(self, addr, port):
        circuit = self.tor_controller.new_circuit()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)

        # Connect the socket to the hidden service via the Tor circuit
        s.connect((addr, port))
        s = self.tor_controller.attach_stream(circuit, s)

        s.send("test")
        response = s.recv(1024)
        print(response)

    def get_address(self):
        return self.hidden_service.service_id
