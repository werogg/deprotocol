from deprotocol.event.events.packet_received_event import PacketReceivedEvent


class KeepAliveReceivedEvent(PacketReceivedEvent):
    def __init__(self, packet, node_connection):
        super().__init__(packet, node_connection)
