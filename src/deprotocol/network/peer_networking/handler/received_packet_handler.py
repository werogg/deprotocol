from deprotocol.event.events.packet_received_event import PacketReceivedEvent
from deprotocol.network.peer_networking.handler.handshake_packet_handler import HandshakePacketHandler
from deprotocol.network.peer_networking.handler.keepalive_packet_handler import KeepAlivePacketHandler
from deprotocol.network.protocol.type import PacketType


class ReceivedPacketHandler:
    def __init__(self, node_connection):
        self.node_connection = node_connection
        self.packet_type_handlers = {
            PacketType.HANDSHAKE: HandshakePacketHandler(node_connection),
            PacketType.KEEP_ALIVE: KeepAlivePacketHandler(node_connection),
        }

    def handle_received_packet(self, received_packet):
        event = PacketReceivedEvent(received_packet)
        self.node_connection.deprotocol.listeners.fire(event)

        if handler := self.packet_type_handlers.get(received_packet.TYPE):
            handler.handle_packet_type(received_packet)
