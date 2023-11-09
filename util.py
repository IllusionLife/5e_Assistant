import json
from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def add_to_json(file_path, tag, tag_id, block_to_add):
    json_file = None
    with open(file_path, "r") as file:
        json_file = json.load(file)

    obj_ptr = json_file
    for key in file_path.split("/"):
        if key == file_path[-1]:
            obj_ptr[key] = new_value
        obj_ptr = obj_ptr[key]

    if not any(profs.get('id') == tag_id for profs in find_tag[tag[-1]]):
        json_file[tag].append(block_to_add)
    else:
        #TODO: add warning to override
        print("Nope")
    print(json_file)

    with open(file_path, "w") as outfile:
        json.dump(json_file, outfile, indent=2)
