from deprotocol.network.protocol.payloads.default_payload import DefaultPayload


class MessagePayload(DefaultPayload):

    def __init__(self, message, signature):
        super().__init__()
        self.message = message
        self.signature = signature
