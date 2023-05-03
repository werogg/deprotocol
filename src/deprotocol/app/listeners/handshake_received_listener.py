from deprotocol.event.event_listener import Listener
from deprotocol.event.events.handshake_received_event import HandshakeReceivedEvent


class HandshakeReceivedListener(Listener):
    def handle_event(self, event: HandshakeReceivedEvent):
        pass
