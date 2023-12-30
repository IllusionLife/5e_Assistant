import json
from os import system, name
from globals import YN_CONST


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def str_to_id(str_name: str):
    res_id = str_name.replace(" ", "_").lower()
    return res_id


def translate_yn(yn):
    if YN_CONST.index(yn) % 2:
        return False
    return True


def open_json(file_path):
    json_content = None
    try:
        with open(file_path, "r") as file:
            json_content = json.load(file)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(file_path, "w") as file:
            file.write("{}")

        with open(file_path, "r") as file:
            json_content = json.load(file)
    return json_content


def input_from_list(valid_list: list):
    choice = input().lower()
    # Check if key exists
    if choice not in valid_list:
        return False
    return choice


def id_exists_in_json_list(json_content, nodes, id_value):
    # Create a pointer to iterate through json list
    json_ptr = json_content

    # Iterate through each part in the provided tag (if tag consists of multiple )
    # and check if tag_id exists in given json array
    for key in nodes:
        if key == nodes[-1]:
            if (isinstance(json_ptr.get(key, None), list)
                    and any(element["id"] == id_value for element in json_ptr[key])):
                return True
            return False
        json_ptr = json_ptr.get(key, False)
        if not json_ptr:
            return False
    return False


def add_to_json_list(file_path, nodes, id_value, block_to_add):
    json_content = open_json(file_path)
    nodes = nodes.split("/")

    if id_exists_in_json_list(json_content, nodes, id_value):
        print("Data with id <" + id_value + "> already exists!")
        return False

    json_ptr = json_content
    if len(json_ptr) == 0:
        for key in nodes[:-1]:
            json_ptr[key] = {}
            json_ptr = json_ptr[key]
        json_ptr[nodes[-1]] = [block_to_add]
    else:
        for key in nodes[:-1]:
            if not json_ptr.get(key, False):
                json_ptr[key] = {}
            json_ptr = json_ptr[key]
        if json_ptr.get(nodes[-1], False):
            json_ptr[nodes[-1]].append(block_to_add)
        else:
            json_ptr[nodes[-1]] = [block_to_add]

    with open(file_path, "w") as outfile:
        json.dump(json_content, outfile, indent=2)


def check_json_by_id(file_path, nodes, id_value):
    json_content = open_json(file_path)
    nodes = nodes.split("/")

    if id_exists_in_json_list(json_content, nodes, id_value):
        return True
    return False
