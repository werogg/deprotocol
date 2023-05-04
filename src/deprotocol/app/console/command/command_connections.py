from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandConnections(Command):
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        for i, node in enumerate(self.deprotocol.node.network_manager.node_connections):
            Logger.get_logger().info(f"[{i}] {node}")
