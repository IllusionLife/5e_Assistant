from abc import ABC, abstractmethod


class Entity5E(ABC):
    def __init__(self, entity_name, entity_type, entity_size):
        self.eName = entity_name
        self.eType = entity_type
        self.eSize = entity_size

    @abstractmethod
    def get_name(self):
        return self.eName

    @abstractmethod
    def get_type(self):
        return self.eType

    @abstractmethod
    def get_size(self):
        return self.eSize
