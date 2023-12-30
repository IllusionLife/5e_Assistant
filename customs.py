import json

import util as utl
from exit_codes import *
from globals import PROFICIENCY_PATH, RACES_PATH, TRAITS_PATH, ENTITY_SIZES, YN_CONST
from json_tags import PROFICIENCY_JSON_TAG, RACIAL_TRAITS_JSON_TAG, RACES_JSON_TAG


# Generates
def generate_simple_data(data_name: str):
    """
    Generates a simple dictionary with data using provided data_name. Dictionary contains name and id.
    :param data_name: Name to be used in JSON.
    :returns: Dictionary with 'id' and 'name'.
    """
    new_prof_id = utl.str_to_id(data_name)
    prof_data = {"id": new_prof_id,
                 "name": data_name}
    return prof_data


def add_new_proficiency(prof_data: dict):
    """
    Adds proficiency data in JSON file.
    :param prof_data: Dictionary with proficiency data.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    return utl.add_to_json_list(PROFICIENCY_PATH, PROFICIENCY_JSON_TAG, prof_data["id"], prof_data)


def new_proficiency():
    """
    Function to retrieve data for new proficiency.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    utl.clear()
    new_prof_name = input("Which proficiency would you like to add to the proficiency list?\n")

    if is_proficiency(new_prof_name):
        print("Proficiency already exists.")
        return EXIT_ALREADY_EXISTS

    prof_data = generate_simple_data(new_prof_name)
    add_new_proficiency(prof_data)
    return EXIT_SUCCESS


def is_proficiency(prof: str):
    """
    Check if the provided string is an existing proficiency
    :param prof: Proficiency name or id
    :return: True if proficiency already exists in JSON. False otherwise.
    """
    prof_id = utl.str_to_id(prof)
    return utl.check_json_by_id(PROFICIENCY_PATH, PROFICIENCY_JSON_TAG, prof_id)


def is_racial_trait(trait: str):
    """
    Check if the provided string is an existing racial trait
    :param trait: Racial trait name or id
    :return: True if racial trait already exists in JSON. False otherwise.
    """
    trait_id = utl.str_to_id(trait)
    return utl.check_json_by_id(TRAITS_PATH, RACIAL_TRAITS_JSON_TAG, trait_id)


def is_race(race: str):
    """
    Check if the provided string is an race
    :param race: Race name or id
    :return: True if race already exists in JSON. False otherwise.
    """
    race_id = utl.str_to_id(race)
    return utl.check_json_by_id(RACES_PATH, RACES_JSON_TAG, race_id)


def add_new_race(race_data: dict):
    """
    Adds race data in JSON file.
    :param race_data: Dictionary with race data.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    utl.add_to_json_list(RACES_PATH, RACES_JSON_TAG, race_data["id"], race_data)


def add_racial_trait(trait_data: dict):
    """
    Adds racial trait data in JSON file.
    :param trait_data: Dictionary with racial trait data.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if proficiency already exists.
    """
    utl.add_to_json_list(TRAITS_PATH, RACIAL_TRAITS_JSON_TAG, trait_data["id"], trait_data)


def new_race():
    """
    Function to retrieve data for new race.
    :returns: EXIT_SUCCESS on success, EXIT_ALREADY_EXISTS if race already exists.
    """
    utl.clear()
    new_race_name = input("What will your race be called?\n")

    if is_race(new_race_name):
        print("Race already exists.")
        return EXIT_ALREADY_EXISTS

    new_race_id = utl.str_to_id(new_race_name)

    while True:
        print("What is the general size of the race? Please choose from the following sizes:")
        print(', '.join(ENTITY_SIZES).title())
        new_race_size = utl.input_from_list(ENTITY_SIZES)
        if new_race_size:
            break
        utl.clear()
        print("Invalid choice.")

    new_race_traits = []
    race_trait = input("What traits do they have? Leave empty if no more traits are to be added.\n")
    while race_trait != "":
        if not is_racial_trait(race_trait):
            add_trait = False
            while not add_trait:
                print("Trait not found. Would you like to create it? (Y)es or (N)o:")
                add_trait = utl.input_from_list(YN_CONST)
            if utl.translate_yn(add_trait):
                trait_data = generate_simple_data(race_trait)
                add_racial_trait(trait_data)
                new_race_traits.append(trait_data["id"])
        else:
            trait_data = generate_simple_data(race_trait)
            new_race_traits.append(trait_data["id"])
        race_trait = input("Would you like another trait? Leave empty if no more traits are to be added.\n")

    # Optional data
    new_race_appearance = input("What does your race look like? Please provide a general description? (Optional)")
    new_race_age = input("Please give an approximate age span/life expectancy for your race? (Optional)")

    race_data = {"id": new_race_id,
                 "name": new_race_name,
                 "size": new_race_size,
                 "appearance": new_race_appearance,
                 "age_span": new_race_age,
                 "traits": new_race_traits
                 }

    utl.add_to_json_list(RACES_PATH, RACES_JSON_TAG, new_race_id, race_data)
    return EXIT_SUCCESS
