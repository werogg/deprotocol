from deprotocol.event.event_listener import Listener
from deprotocol.event.events.keepalive_received_event import KeepAliveReceivedEvent


class KeepAliveReceivedListener(Listener):
    def handle_event(self, event: KeepAliveReceivedEvent):
        pass
