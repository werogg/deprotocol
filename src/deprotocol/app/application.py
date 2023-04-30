import platform
from abc import ABC

from deprotocol.app.console.command.command_handler import CommandHandler
from deprotocol.app.console.command.command_help import CommandHelp
from deprotocol.app.listeners.packet_received_listener import PacketReceivedListener
from deprotocol.event.event_listener import Listeners
from deprotocol.version import APP_VERSION

from deprotocol.settings import APP_NAME

from deprotocol.app.setup.console_setup import ConsoleSetup
from deprotocol.app.setup.logger_setup import LoggerSetup
from deprotocol.app.setup.p2p_setup import P2PNodeSetup
from deprotocol.app.setup.tor_setup import TorSetup
from deprotocol.app.logger import Logger
from deprotocol.settings import NODE_HOST
from deprotocol.settings import NODE_PORT


class DeProtocol(ABC):

    def __init__(self):
        self.setups = {}
        self.listeners = Listeners()
        self.command_handler = CommandHandler(self)
        self.node = None

    def on_start(self, proxy_host='127.0.0.1', proxy_port=9050):
        self.register_default_events()
        self.register_default_commands()

        self.setups = {
            'console': ConsoleSetup(self),
            'logger': LoggerSetup(),
            'tor': TorSetup(self, proxy_host, proxy_port),
            'peer_networking': P2PNodeSetup(self, NODE_HOST, NODE_PORT)
        }

        for setup in self.setups.values():
            setup.setup()

        Logger.get_logger().info(f"Starting {APP_NAME} version {APP_VERSION}, running on {platform.system()}")

    def on_stop(self):
        pass

    def register_default_events(self):
        self.register_listener(PacketReceivedListener())

    def register_default_commands(self):
        self.register_command('help', CommandHelp)

    def register_listener(self, listener):
        self.listeners.register_listener(listener)

    def register_command(self, command_name, command):
        self.command_handler.register_command(command_name, command)
