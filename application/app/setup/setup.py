from abc import ABC
from abc import abstractmethod


class SetupABC(ABC):
    @abstractmethod
    def setup(self):
        pass
