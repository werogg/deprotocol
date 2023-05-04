import time

from deprotocol.event.events.keepalive_received_event import KeepAliveReceivedEvent
from deprotocol.network.peer_networking.handler.packet_type_handler import PacketTypeHandler


class KeepAlivePacketHandler(PacketTypeHandler):
    def __init__(self, node_connection):
        self.node_connection = node_connection

    def handle_packet_type(self, received_packet):
        self.node_connection.pinger.last_ping = time.time()

        event = KeepAliveReceivedEvent(received_packet, self.node_connection)
        self.node_connection.deprotocol.listeners.fire(event)
