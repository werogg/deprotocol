import time

from deprotocol.network.protocol.payloads.payload import Payload


class DefaultPayload(Payload):
    def __init__(self):
        super().__init__()
        self.time = time.time()

    def get_payload(self):
        return {
            attr_name: attr_value
            for attr_name, attr_value in self.__dict__.items()
            if not attr_name.startswith('_') and not callable(attr_value)
        }
