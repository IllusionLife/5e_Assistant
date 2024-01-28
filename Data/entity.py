from abc import ABC, abstractmethod


class EntityRPG(ABC):
    def __init__(self, entity_id, entity_name, entity_type, entity_size):
        self.id = entity_id
        self.name = entity_name
        self.type = entity_type
        self.size = entity_size

    def set_id(self, entity_id):
        self.id = entity_id

    def get_id(self):
        return self.id

    def set_name(self, entity_name):
        self.name = entity_name

    def get_name(self):
        return self.name

    def set_type(self, entity_type):
        self.type = entity_type

    def get_type(self):
        return self.type

    def set_size(self, entity_size):
        self.size = entity_size

    def get_size(self):
        return self.size

    @abstractmethod
    def as_dict(self):
        pass


class EntitiesRPG(ABC):
    def __init__(self):
        self.data_list = list()

    def __order_list(self):
        self.data_list.sort(key=lambda x: x.get_id())

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass
