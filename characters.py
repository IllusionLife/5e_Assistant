from entity import Entity5E

class CharacterSheet(Entity5E):
    def __init__(self, entity_name, entity_type, entity_size):
        super().__init__(entity_name, entity_type, entity_size)


def create_character():
    print("Success!")