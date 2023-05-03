from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandMessage(Command):

    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        node = next(node for node in self.deprotocol.node.network_manager.node_connections if str(node.id) == args[0])
        node.send_message(args[1:])
        Logger.get_logger().info("Sending message...")
