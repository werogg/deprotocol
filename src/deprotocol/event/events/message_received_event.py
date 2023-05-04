import json

from deprotocol.event.events.packet_received_event import PacketReceivedEvent


class MessageReceivedEvent(PacketReceivedEvent):
    def __init__(self, packet, node_connection):
        super().__init__(packet, node_connection)
        payload = json.loads(packet.payload)
        self.time = payload['time']
        self.message = payload['message']
