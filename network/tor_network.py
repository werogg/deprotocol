import os.path
import stem.process
import stem.control

from logger.logger import Logger


class TorService:
    def __init__(self, port):
        self.port = port
        self.tor_process = None
        self.tor_controller = None
        self.hidden_service = None

    def start(self):
        self.tor_process = stem.process.launch_tor_with_config(
            config={
                'SocksPort': '0',
                'ControlPort': str(self.port),
                'DataDirectory': os.path.join(os.getcwd(), 'tor_data'),
                'HiddenServiceDir': os.path.join(os.getcwd(), 'tor_hidden_service'),
                'HiddenServicePort': '80 127.0.0.1:8080'
            },
            tor_cmd=os.path.join(os.getcwd(), 'bin', 'tor', 'tor.exe'),
            init_msg_handler=self._print_bootstrap_lines,
            take_ownership=True
        )

        self.tor_controller = stem.control.Controller.from_port(port=self.port)
        self.tor_controller.authenticate()

        self.hidden_service = self.tor_controller.create_ephemeral_hidden_service(
            {'80': '127.0.0.1:8080'}, await_publication=True
        )
        Logger.get_instance().info(f"Hidden service created with address: {self.hidden_service.service_id}")

    def stop(self):
        if self.tor_controller:
            self.tor_controller.close()
        if self.tor_process:
            self.tor_process.kill()

    def _print_bootstrap_lines(self, line):
        if "Bootstrapped" in line:
            print(line)
