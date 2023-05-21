import json

from deprotocol.network.protocol.payloads.payload import Payload


class HandshakePayload(Payload):

    def __init__(self, address, nickname, profile_img, public_key, initiator=False):
        super().__init__()
        self.address = address
        self.nickname = nickname
        self.profile_img = profile_img
        self.public_key = public_key
        self.initiator = initiator

    def serialize(self):
        payload = {
            'address': self.address,
            'nickname': self.nickname,
            'profile_img': self.profile_img,
            'public_key': self.public_key,
            'initiator': self.initiator
        }
        return json.dumps(payload)
