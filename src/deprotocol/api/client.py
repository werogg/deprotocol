from deprotocol.app.application import DeProtocol
from deprotocol.settings import NODE_PORT


class Client:

    def __init__(self, testing=False):
        self.app = DeProtocol(testing)

    def start(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.app.on_start(proxy_host, proxy_port)

    def stop(self):
        self.app.on_stop()

    def connect(self, address, port=NODE_PORT):
        self.app.node.connect_to(address, port)

    def send_message(self, node_id, message):
        node = next(node for node in self.app.node.network_manager.node_connections if node.id is node_id)
        node.send_message(message)

    def get_connected_nodes(self):
        return self.app.node.get_connected_nodes()

    def register_listener(self, listener):
        self.app.register_listener(listener)

    def get_address(self):
        return self.app.node.onion_address
