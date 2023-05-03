import json

from deprotocol.network.protocol.payloads.payload import Payload


class HandshakePayload(Payload):

    def __init__(self, address, nickname, profile_img, public_key):
        super().__init__()
        self.address = address
        self.nickname = nickname
        self.profile_img = profile_img
        self.public_key = public_key

    def serialize(self):
        payload = {
            'address': self.address,
            'nickname': self.nickname,
            'profile_img': self.profile_img,
            'public_key': self.public_key
        }
        return json.dumps(payload)
