import json
import time

from deprotocol.network.protocol.payloads.payload import Payload


class MessagePayload(Payload):

    def __init__(self, message):
        super().__init__()
        self.time = time.time()
        self.message = message

    def serialize(self):
        payload = {
            'time': self.time,
            'message': self.message,
        }
        return json.dumps(payload)
