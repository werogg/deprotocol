import json
from abc import ABC
from abc import abstractmethod


class Payload(ABC):
    def __init__(self):
        self.payload = {}

    @abstractmethod
    def get_payload(self):
        pass

    def serialize(self):
        return json.dumps(self.get_payload())
