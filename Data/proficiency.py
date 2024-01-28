import util
from Base.exit_codes import *
from Data.entity import EntityRPG, EntitiesRPG
from Base.config_handler import ConfigHandlerRPG
from Base.json_handler import JsonHandlerRPG
from Base.logs import logger
from util import str_to_id


class ProficiencyRPG(EntityRPG):
    def __init__(self, prof_id, prof_name):
        super().__init__(prof_id, prof_name, "Proficiency", None)
        logger().log_debug("Created proficiency object with id <$1>", self.get_id())

    def as_dict(self):
        return {"id": self.get_id(), "name": self.get_name()}


class ProficienciesRPG(EntitiesRPG):
    def __init__(self):
        super().__init__()
        self.configs = ConfigHandlerRPG("json.conf")
        self.proficiencies_json = JsonHandlerRPG(self.configs.get_conf("SOURCES_DIR")
                                                , self.configs.get_conf("PROFICIENCY_FILE"))
        self.proficinecies_json_ptr = None
        self.load()

    def load(self):
        logger().log_debug("Loading proficiencies to memory")
        self.proficinecies_json_ptr = self.proficiencies_json.pointer_to_tag(
            self.configs.get_conf("PROFICIENCY_JSON_TAG"))
        for data in self.proficinecies_json_ptr:
            self.data_list.append(ProficiencyRPG(data["id"], data["name"]))
        return EXIT_SUCCESS

    def save(self):
        self.proficinecies_json_ptr.clear()
        for proficiency in self.data_list:
            self.proficinecies_json_ptr.append(proficiency.as_dict())
        self.proficiencies_json.save_json()

    def __proficiency_id_list(self):
        return [prof.get_id() for prof in self.data_list]

    def list_proficiencies(self):
        return [prof.get_name() for prof in self.data_list]

    def proficiency_exists(self, proficiency_id):
        for proficiency in self.data_list:
            if proficiency.get_id() == proficiency_id:
                return True
        return False

    def add_proficiency(self, proficiency_name):
        proficiency_id = str_to_id(proficiency_name)
        if self.proficiency_exists(proficiency_id):
            logger().log_error("Proficiency <$1> already exists.", proficiency_name)
            return EXIT_ALREADY_EXISTS
        self.data_list.append(ProficiencyRPG(proficiency_id, proficiency_name))
        self.__order_list()
        self.save()
        logger().log_info("Proficiency <$1> added.", proficiency_name)
        return EXIT_SUCCESS

    def delete_proficiency(self, proficiency_name):
        proficiency_id = str_to_id(proficiency_name)
        if self.proficiency_exists(proficiency_name):
            for index in range(len(self.data_list)):
                if self.data_list[index].get_id() == proficiency_id:
                    self.data_list.pop(index)
                    break
            self.__order_list()
            self.save()
            logger().log_info("Proficiency <$1> deleted.", proficiency_name)
            return EXIT_SUCCESS
        logger().log_error("Proficiency <$1> doesn't exists.", proficiency_name)
        return EXIT_DOESNT_EXISTS
