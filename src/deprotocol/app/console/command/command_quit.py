from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandQuit(Command):
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        Logger.get_logger().info("Stopping the protocol...")
        self.deprotocol.on_stop()
