from application.api.handlers.message_handler import MessageHandler
from application.app.application import DeProtocol
from application.p2p.deprecated_node import PORT


class Client:

    def __init__(self):
        self.app = DeProtocol()
        self.message_handler = MessageHandler()

    def start(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.app.on_start(proxy_host, proxy_port)

    def get_onion_address(self):
        return self.app.node.connected_host

    def get_port(self):
        return self.app.node.connected_port

    def connect(self, host, port=PORT):
        self.app.node.connect_to(host, port)

    def get_peers(self):
        return self.app.node.peers

    def send_message(self, peer, message):
        self.app.node.send_message(peer, message)
