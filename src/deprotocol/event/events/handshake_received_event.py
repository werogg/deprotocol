import json

from deprotocol.event.events.packet_received_event import PacketReceivedEvent


class HandshakeReceivedEvent(PacketReceivedEvent):
    def __init__(self, packet):
        super().__init__(packet)
        payload = json.loads(packet.payload)
        self.connected_address = payload['address']
        self.nickname = payload['nickname']
        self.profile_img = payload['profile_img']
        self.connected_public_key = payload['public_key']