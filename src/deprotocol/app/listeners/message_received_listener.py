from deprotocol.event.event_listener import Listener
from deprotocol.event.events.message_received_event import MessageReceivedEvent


class MessageReceivedListener(Listener):
    def handle_event(self, event: MessageReceivedEvent):
        pass
