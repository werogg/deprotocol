from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandHelp(Command):
    def handle_command(self, args=''):
        Logger.get_logger().info("You can use x x and x")
