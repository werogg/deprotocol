from deprotocol.app.console.command.command import Command
from deprotocol.app.logger import Logger


class CommandMessage(Command):

    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        try:
            node = next(
                node for node in self.deprotocol.node.network_manager.node_connections if str(node.id) == args[0])
            node.send_message(args[1:])
            Logger.get_logger().info("Sending message...")
        except StopIteration:
            # Handle the case when no matching node is found
            Logger.get_logger().info("No matching node found.")
        except Exception as e:
            # Handle any other exception that may occur
            Logger.get_logger().error("An error occurred:", e)
