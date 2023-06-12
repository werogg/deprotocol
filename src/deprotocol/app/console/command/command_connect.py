from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandConnect(Command):
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        if args == '' or not args:
            Logger.get_logger().info("Please specify an address to connect!")
            return
        self.deprotocol.node.connect_to(args[0])
