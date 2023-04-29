from deprotocol.logger.logger import Logger


class MessageHandler:
    def __init__(self, node):
        self.node = node

    def on_message(self, data, sender, private):
        Logger.get_logger().info(f"Incomig Message: {data}")

    def handle_message(self, data, node):
        pass