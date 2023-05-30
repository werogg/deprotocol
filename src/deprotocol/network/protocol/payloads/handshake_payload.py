from deprotocol.network.protocol.payloads.default_payload import DefaultPayload


class HandshakePayload(DefaultPayload):

    def __init__(self, address, nickname, profile_img, public_key, initiator=False):
        super().__init__()
        self.address = address
        self.nickname = nickname
        self.profile_img = profile_img
        self.public_key = public_key
        self.initiator = initiator
