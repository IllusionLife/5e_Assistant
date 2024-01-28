import util
from Base.exit_codes import *
from Base.config_handler import ConfigHandlerRPG
from Base.json_handler import JsonHandlerRPG
from Base.logs import logger
from Data.entity import EntityRPG
from util import str_to_id, clear_dict


class RaceRPG(EntityRPG):
    def __init__(self, **kwargs):
        race_data = kwargs.get("data", None)
        if kwargs.get("id", None) is not None and race_data is None:
            race_data = RacesRPG().get_race_data(kwargs.get("id")).get_score_modifier()

        super().__init__(race_data["id"], race_data["name"], "Race", race_data["size"])
        self.speed = race_data.get("speed", None)
        self.asm = race_data.get("asm", None)
        self.appearance = race_data.get("appearance", None)
        self.age_span = race_data.get("age_span", None)
        self.traits = race_data.get("traits", None)
        self.languages = race_data.get("languages", None)
        self.subrace_of = race_data.get("subrace_of", None)

        logger().log_debug("Created proficiency object with id <$1>", self.get_id())

    def as_dict(self):
        result = clear_dict(self.__dict__)
        result.pop("type")
        return result

    def get_speed(self):
        return self.speed

    def get_parent_race(self):
        return self.subrace_of

    def get_score_modifier(self):
        return self.asm

    def is_subrace(self):
        if self.subrace_of is not None:
            return True
        return False

    def get_ability_modifiers(self):
        total_asm = self.asm
        if self.is_subrace():
            parent_race_asm = RacesRPG().get_race_data(self.get_parent_race()).get_score_modifier()
            if parent_race_asm:
                for attribute, bonus in parent_race_asm.items():
                    if attribute in total_asm:
                        total_asm[attribute] += bonus
                    else:
                        total_asm[attribute] = bonus
        return total_asm


class RacesRPG:
    def __init__(self):
        self.configs = ConfigHandlerRPG("json.conf")
        self.races_json = JsonHandlerRPG(self.configs.get_conf("SOURCES_DIR")
                                        , self.configs.get_conf("RACES_FILE"))
        self.races_json_ptr = None
        self.races = list()
        self.load_races()
        self.__save()

    def __race_id_list(self):
        return [race.get_id() for race in self.races]

    def __order_list(self):
        self.races.sort(key=lambda x: x.get_id())

    def __save(self):
        self.races_json_ptr.clear()
        for race in self.races:
            self.races_json_ptr.append(race.as_dict())
        self.races_json.save_json()

    def list_races(self):
        return [race.get_name() for race in self.races]

    def race_exists(self, race_id):
        for race in self.races:
            if race.get_id() == race_id:
                return True
        return False

    def load_races(self):
        logger().log_debug("Loading races to memory")
        self.races_json_ptr = self.races_json.pointer_to_tag(self.configs.get_conf("RACES_JSON_TAG"))
        for race_data in self.races_json_ptr:
            self.races.append(RaceRPG(data=race_data))
        return EXIT_SUCCESS

    def add_races(self, race_data):
        if self.race_exists(race_data["id"]):
            logger().log_error("Race with ID <$1> already exists.", race_data["id"])
            return EXIT_ALREADY_EXISTS
        self.races.append(RaceRPG(data=race_data))
        self.__order_list()
        self.__save()
        self.races_json.save_json()
        return EXIT_SUCCESS

    def get_race_data(self, race_id):
        for race in self.races:
            if race.get_id == race_id:
                return race
        return None

    def delete_race(self, race_name):
        race_id = str_to_id(race_name)
        if self.race_exists(race_id):
            for index in range(len(self.races)):
                if self.races[index].get_id() == race_id:
                    self.races.pop(index)
                    break
            self.__order_list()
            self.__save()
            self.races_json.save_json()
            logger().log_info("Race <$1> deleted.", race_name)
            return EXIT_SUCCESS
        logger().log_error("Race <$1> doesn't exists.", race_name)
        return EXIT_DOESNT_EXISTS

def add_race_from_file():
    logger().log_info("Starting race interface")
    logger().log_debug("Initializing interface configurations")
    interface_conf = ConfigHandlerRPG("interfaces.conf")
    interface_conf.log_configs()

