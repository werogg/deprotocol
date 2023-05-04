from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandHelp(Command):
    def handle_command(self, args=''):
        Logger.get_logger().info("\nAvailable commands:\n"
                                 "- connect <onion.address> - connect to a peer using their onion address\n"
                                 "- connections - list all current connections\n"
                                 "- quit - disconnect from all peers and quit DeProtocol\n"
                                 "- message <connection> <message> - send a message to a specific connection")
