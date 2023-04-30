from deprotocol.app.logger import Logger


class CommandHandler:
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol
        self.commands = {}

    def register_command(self, command_name, command):
        self.commands[command_name] = command

    def handle_command(self, command_string):
        if command_string == '':
            return

        Logger.get_logger().info(f"Console executed command: {command_string}")

        command_args = command_string.split()
        command_name = command_args[0]

        if command_name in self.commands:
            command = self.commands[command_name]
            output = command.handle_command(command_args[1:])
        else:
            Logger.get_logger().info("Unknown command!")
