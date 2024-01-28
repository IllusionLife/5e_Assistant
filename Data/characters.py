from Data.entity import EntityRPG


class CharacterSheet(EntityRPG):
    def __init__(self, entity_name, entity_type, entity_size):
        super().__init__(entity_name, entity_type, entity_size)


def create_character():
    print("Success!")
