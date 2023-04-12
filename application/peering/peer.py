# pylint: skip-file

from pythonp2p import Node

from application.logger.logger import Logger


class PeerNode(Node):

    def __init__(self, host='127.0.0.1', port=65433):
        super().__init__(host, port)
        self.start()

    def broadcast(self, data):
        self.send_message(data)

    def connect(self, ip):
        self.connect_to(ip)

    def on_message(self, data, sender, private):
        Logger.get_instance().info(data)
