from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.logger.logger import Logger


class DeProtocolReadyListener(Listener):
    def handle_event(self, event: DeProtocolReadyEvent):
        Logger.get_logger().info("DeProtocol is ready!")
