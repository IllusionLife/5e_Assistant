import util
from Base.exit_codes import *
from Data.entity import EntityRPG, EntitiesRPG
from Base.config_handler import ConfigHandlerRPG
from Base.json_handler import JsonHandlerRPG
from Base.logs import logger
from util import str_to_id, clear_dict


class TraitRPG(EntityRPG):
    def __init__(self, trait_id, trait_name, trait_type):
        super().__init__(trait_id, trait_name, "Trait", None)
        self.trait_type = trait_type
        logger().log_debug("Created trait object with id <$1>", self.get_id())

    def as_dict(self):
        result = clear_dict(self.__dict__)
        result.pop("type")
        return result


class TraitsRPG(EntitiesRPG):
    def __init__(self):
        super().__init__()
        self.configs = ConfigHandlerRPG("json.conf")
        self.traits_json = JsonHandlerRPG(self.configs.get_conf("SOURCES_DIR")
                                         , self.configs.get_conf("TRAITS_FILE"))
        self.traits_json_ptr = None
        self.__load()

    def __load(self):
        logger().log_debug("Loading traits to memory")
        self.traits_json_ptr = self.traits_json_ptr.pointer_to_tag(self.configs.get_conf("TRAITS_JSON_TAG"))
        for data in self.traits_json_ptr:
            self.data_list.append(TraitRPG(data["id"], data["name"], data["trait_type"]))
        return EXIT_SUCCESS

    def __save(self):
        self.traits_json_ptr.clear()
        for trait in self.data_list:
            self.traits_json_ptr.append(trait.as_dict())
        self.traits_json.save_json()

    def __trait_id_list(self):
        return [trait.get_id() for trait in self.data_list]

    def list_traits(self):
        return [trait.get_name() for trait in self.data_list]

    def trait_exists(self, trait_name):
        trait_id = str_to_id(trait_name)
        for trait in self.data_list:
            if trait.get_id() == trait_id:
                return True
        return False

    def add_trait(self, trait_name, trait_type):
        trait_id = str_to_id(trait_name)
        if self.trait_exists(trait_name):
            logger().log_error("Trait <$1> already exists.", trait_name)
            return EXIT_ALREADY_EXISTS
        self.data_list.append(TraitRPG(trait_id, trait_name, trait_type))
        self.__order_list()
        self.__save()
        logger().log_info("Trait <$1> added.", trait_name)
        return EXIT_SUCCESS

    def delete_trait(self, trait_name):
        trait_id = str_to_id(trait_name)
        if self.trait_exists(trait_name):
            for index in range(len(self.data_list)):
                if self.data_list[index].get_id() == trait_id:
                    self.data_list.pop(index)
                    break
            self.__order_list()
            self.__save()
            logger().log_info("Trait <$1> deleted.", trait_name)
            return EXIT_SUCCESS
        logger().log_error("Trait <$1> doesn't exists.", trait_name)
        return EXIT_DOESNT_EXISTS
