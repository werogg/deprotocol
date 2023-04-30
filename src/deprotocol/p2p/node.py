import threading

from deprotocol.p2p.network_manager import NetworkManager


class Node:
    def __init__(self, deprotocol, host='', port=65432, onion_address=''):
        super().__init__()
        self.deprotocol = deprotocol
        self.terminate_flag = threading.Event()
        self.host = host
        self.port = port
        self.onion_address = onion_address
        self.network_manager = NetworkManager(deprotocol, host, port, onion_address)
        deprotocol.node = self

    def start(self):
        self.network_manager.start()

    def connect_to(self, host, port):
        self.network_manager.connect_to(host, port)

    def disconnect_from(self, node):
        self.network_manager.disconnect_from(node)

    def send_message(self, message, node):
        self.network_manager.send_message(message, node)


