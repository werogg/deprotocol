from deprotocol.app.application import DeProtocol
from deprotocol.settings import NODE_PORT


class Client:

    def __init__(self):
        self.app = DeProtocol()

    def start(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.app.on_start(proxy_host, proxy_port)

    def connect(self, address, port=NODE_PORT):
        self.app.node.connect_to(address, port)

    def register_listener(self, listener):
        self.app.register_listener(listener)
