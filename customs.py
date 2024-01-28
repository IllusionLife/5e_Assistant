from typing import Optional
import getpass

import util as utl
from Base.exit_codes import *
from globals import ENTITY_SIZES, YN_CONST
from Base.logs import logger
from Base.config_handler import ConfigHandlerRPG
from Base.json_handler import JsonHandlerRPG

from Data.proficiency import ProficienciesRPG
from Data.traits import TraitsRPG
from Data.races import RacesRPG

# ------------------------------ General ------------------------------

config_json = ConfigHandlerRPG("json.conf")


def generate_simple_data(sad):
    return {}


# ------------------------------ Proficiencies ------------------------------

proficiencies: Optional[ProficienciesRPG] = None


def init_proficiency_data():
    global proficiencies
    if proficiencies is None:
        logger().log_debug("Initializing Proficiencies object.")
        proficiencies = ProficienciesRPG()


def __delete_proficiency(prof_name: str):
    """
    Removes proficiency data in JSON file.
    :param prof_name: Proficiency name to be deleted
    :return: EXIT_SUCCESS on success, EXIT_DOESNT_EXISTS if no proficiency with this tag is found
    """
    init_proficiency_data()
    logger().log_info("Deleting proficiency <<$1>>", prof_name)
    proficiencies.delete_proficiency(prof_name)
    return EXIT_SUCCESS


def remove_proficiency():
    """
    Function to retrieve data for proficiency deletion and calling request.
    :return: EXIT_SUCCESS on success, EXIT_DOESNT_EXISTS if no proficiency with this tag is found
    """
    utl.clear()
    new_prof_name = input("Which proficiency would you like to remove to the proficiency list?\n")
    __delete_proficiency(new_prof_name)
    return EXIT_SUCCESS


def __add_new_proficiency(prof_name: str):
    """
    Adds proficiency data in JSON file.
    :param prof_name: String with proficiency name.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    init_proficiency_data()

    logger().log_info("Adding proficiency <<$1>>", prof_name)
    return proficiencies.add_proficiency(prof_name)


def new_proficiency():
    """
    Function to retrieve data for new proficiency.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    utl.clear()
    new_prof_name = input("Which proficiency would you like to add to the proficiency list?\n")
    return __add_new_proficiency(new_prof_name)


def list_proficiency():
    utl.clear()
    init_proficiency_data()
    for prof in proficiencies.list_proficiencies():
        print(prof)
    getpass.getpass("Press Enter to continue")


# ------------------------------ Traits ------------------------------
traits: Optional[TraitsRPG] = None


def init_traits_data():
    global traits
    if traits is None:
        logger().log_debug("Initializing Traits object.")
        traits = TraitsRPG()


def is_racial_trait(trait: str):
    """
    Check if the provided string is an existing trait
    :param trait: Trait name or id
    :return: True if trait already exists in JSON. False otherwise.
    """
    init_traits_data()
    return traits.trait_exists(trait)


def list_racial_traits():
    utl.clear()
    init_traits_data()
    traits.list_traits()


def __add_trait(trait_name, trait_type):
    """
    Adds trait data in JSON file.
    :param trait_data: Dictionary with trait data.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if trait already exists.
    """
    init_traits_data()
    logger().log_info("Adding trait <$1>", trait_name)
    return traits.add_trait(trait_name, trait_type)


def new_trait():
    """
    Function to retrieve data for new proficiency.
    :returns: EXIT_SUCCESS on success,\
     EXIT_ALREADY_EXISTS if trait already exists,\
     EXIT_INVALID_INPUT if invalid data is provided
    """
    utl.clear()
    new_trait_name = input("Which trait would you like to add to the traits list?\n")
    print("What type of trait is? Please choose from the folowing list")
    new_trait_type = utl.input_from_list(config_json)


    if new_trait_type is not None and new_trait_name is not None:
        logger().log_error("Trait data incomplete!"
                           , ("Name", new_trait_name)
                           , ("Type", new_trait_type))
        return EXIT_INVALID_INPUT
    return __add_trait(new_trait_name, new_trait_type)


# ------------------------------ Races ------------------------------
races_json: Optional[JsonHandlerRPG] = None


def init_racial_data():
    global races_json
    if races_json is None:
        logger().log_debug("Initializing Races JSON object.")
        races_json = JsonHandlerRPG(config_json.get_conf("SOURCES_DIR")
                                   , config_json.get_conf("RACES_FILE"))


def is_race(race: str):
    """
    Check if the provided string is a race
    :param race: Race name or id
    :return: True if race already exists in JSON. False otherwise.
    """
    init_racial_data()
    race_id = utl.str_to_id(race)
    logger().log_info("Checking if race with ID <<$1>> exists.", race_id)
    result = races_json.id_exists(config_json.get_conf("RACES_JSON_TAG"), race_id)
    logger().log_info("Result of search: " "True" if result else "False")
    return result


def delete_race(race_name: str):
    """
    Removes race data in JSON file.
    :param race_name: Race name to be deleted
    :return: EXIT_SUCCESS on success, EXIT_DOESNT_EXISTS if no race with this name is found
    """
    # init_racial_data()
    # if not is_race(race_name):
    #     logger().log_error("Race not found.")
    #     return EXIT_DOESNT_EXISTS
    #
    # logger().log_info("Deleting race with id <<$1>>", utl.str_to_id(race_name))
    # races_json.delete_id(config_json.get_conf("RACES_JSON_TAG")
    #                      , utl.str_to_id(race_name))
    test = RacesRPG()
    return EXIT_SUCCESS


def remove_race():
    """
    Function to retrieve name for race deletion and calling deletion request.
    :return: EXIT_SUCCESS on success, EXIT_DOESNT_EXISTS if no race with this name is found
    """
    utl.clear()
    race_name = input("Which race would you like to remove to the races list?\n")

    delete_race(race_name)
    return EXIT_SUCCESS


def add_new_race(race_data: dict):
    """
    Adds race data in JSON file.
    :param race_data: Dictionary with race data.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    init_racial_data()

    logger().log_info("Adding race with ID <<$1>>", race_data["id"])
    races_json.add_to_json_list(config_json.get_conf("RACES_JSON_TAG")
                                , race_data["id"]
                                , race_data)


def new_race():
    """
    Function to retrieve data for new race.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if race already exists.
    """
    utl.clear()


    return EXIT_SUCCESS

# ------------------------------ Subraces ------------------------------
