from abc import ABC
from abc import abstractmethod


class Payload(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def serialize(self):
        pass
