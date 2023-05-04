from deprotocol.app.logger import Logger
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.message_received_event import MessageReceivedEvent


class MessageReceivedListener(Listener):
    def handle_event(self, event: MessageReceivedEvent):
        Logger.get_logger().info('Message received by ')
        pass
