import platform
import signal
from abc import ABC

from deprotocol.app.console.command.command_connect import CommandConnect
from deprotocol.app.console.command.command_handler import CommandHandler
from deprotocol.app.console.command.command_help import CommandHelp
from deprotocol.app.console.command.command_message import CommandMessage
from deprotocol.app.console.command.command_quit import CommandQuit
from deprotocol.app.listeners.handshake_received_listener import HandshakeReceivedListener
from deprotocol.app.listeners.keepalive_received_listener import KeepAliveReceivedListener
from deprotocol.app.listeners.message_received_listener import MessageReceivedListener
from deprotocol.app.listeners.packet_received_listener import PacketReceivedListener
from deprotocol.app.user import User
from deprotocol.event.event_listener import Listeners
from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.type import PacketType
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

    def __init__(self, testing=False):
        self.setups = {}
        self.listeners = Listeners()
        self.command_handler = CommandHandler(self)
        self.node = None
        self.user = User()
        self.testing = testing

    def on_stop(self):
        if self.node:
            self.node.stop()
        if self.setups['tor']:
            self.setups['tor'].stop()
        if self.setups['console'].shell:
            self.setups['console'].shell.stop()
        Logger.get_logger().info("Successfully stopped! Bye...")

    def on_start(self, proxy_host='127.0.0.1', proxy_port=9050):
        signal.signal(signal.SIGINT, self.on_stop)
        signal.signal(signal.SIGTERM, self.on_stop)
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

        self.node.onion_address = self.setups['tor'].tor_service.get_address()

        Logger.get_logger().info(f"Starting {APP_NAME} version {APP_VERSION}, running on {platform.system()}")

    def set_nickname(self, nickname):
        self.user.nickname = nickname

    def set_profile_img(self, profile_img):
        self.user.profile_img = profile_img

    def register_default_events(self):
        self.register_listener(PacketReceivedListener())
        self.register_listener(MessageReceivedListener())
        self.register_listener(KeepAliveReceivedListener())
        self.register_listener(HandshakeReceivedListener())

    def register_default_commands(self):
        self.register_command('help', CommandHelp)
        self.register_command('connect', CommandConnect(self))
        self.register_command('quit', CommandQuit(self))
        self.register_command('message', CommandMessage(self))

    def register_listener(self, listener):
        self.listeners.register_listener(listener)

    def register_command(self, command_name, command):
        self.command_handler.register_command(command_name, command)
