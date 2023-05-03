from deprotocol.app.console.command.command import Command


class CommandConnect(Command):
    def __init__(self, deprotocol):
        self.deprotocol = deprotocol

    def handle_command(self, args=''):
        self.deprotocol.node.connect_to(args[0])
