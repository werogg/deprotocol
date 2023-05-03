from abc import ABC
from abc import abstractmethod


class PacketTypeHandler(ABC):
    @abstractmethod
    def handle_packet_type(self, received_packet):
        pass