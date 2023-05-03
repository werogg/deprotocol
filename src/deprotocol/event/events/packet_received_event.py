from deprotocol.event.events.event import Event


class PacketReceivedEvent(Event):
    def __init__(self, packet):
        self.packet = packet
