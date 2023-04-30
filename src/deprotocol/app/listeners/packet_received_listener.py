from deprotocol.app.logger import Logger
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.packet_received_event import PacketReceivedEvent


class PacketReceivedListener(Listener):
    def handle_event(self, event: PacketReceivedEvent):
        Logger.get_logger().info(event.packet)
