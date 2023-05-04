from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandAddress(Command):
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        Logger.get_logger().info(f'You address: {self.deprotocol.node.onion_address}')