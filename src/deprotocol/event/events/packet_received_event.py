from deprotocol.event.events.event import Event


class PacketReceivedEvent(Event):
    def __init__(self, packet, node_connection):
        self.packet = packet
        self.node_connection = node_connection
