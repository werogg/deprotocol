import json

from deprotocol.event.events.packet_received_event import PacketReceivedEvent


class MessageReceivedEvent(PacketReceivedEvent):
    def __init__(self, packet):
        super().__init__(packet)
        payload = json.loads(packet.payload)
        self.time = payload['time']
        self.message = payload['message']
