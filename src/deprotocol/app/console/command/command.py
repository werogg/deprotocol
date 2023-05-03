from abc import ABC
from abc import abstractmethod


class Command(ABC):
    @abstractmethod
    def handle_command(self, args=''):
        pass