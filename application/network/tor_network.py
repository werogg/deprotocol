# pylint: skip-file

import os.path
import socket

import stem.control
import stem.process

from application.logger.logger import Logger


class TorService:
    def __init__(self, port):
        self.port = port
        self.tor_process = None
        self.tor_controller = None
        self.hidden_service = None

    def start(self):
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
                tor_cmd=os.path.join(os.getcwd(), 'bin', 'tor', 'tor.exe'),
                init_msg_handler=self._print_bootstrap_lines,
                take_ownership=True
            )
        except Exception as e:
            Logger.get_instance().error(e)

        self.tor_controller = stem.control.Controller.from_port(port=self.port)
        self.tor_controller.authenticate()
        self.tor_controller.new_circuit()

        bytes_read = self.tor_controller.get_info("traffic/read")
        bytes_written = self.tor_controller.get_info("traffic/written")

        Logger.get_instance().info(f'Tor relay has read {bytes_read} bytes and written {bytes_written}.')

        self.hidden_service = self.tor_controller.create_ephemeral_hidden_service(
            {'80': '127.0.0.1:65432'}, await_publication=True
        )
        Logger.get_instance().info(f"Hidden service created with address: {self.hidden_service.service_id}")

    def stop(self):
        if self.tor_controller:
            self.tor_controller.close()
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
