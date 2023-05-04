from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent


class DeProtocolReadyListener(Listener):
    def handle_event(self, event: DeProtocolReadyEvent):
        pass
