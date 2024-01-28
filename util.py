from os import system, name


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


def build_message(msg, *info):
    excess_info = []
    for i in range(len(info)):
        placeholder = f"<${str(i + 1)}>"
        if msg.find(placeholder) != -1:
            msg = msg.replace(placeholder, "<" + str(info[i]) + ">")
        else:
            excess_info.append(str(info[i]))
    if len(excess_info) > 0:
        msg = msg + "(" + ", ".join(excess_info) + ")"
    return msg


def list_lower(my_list):
    return [x.lower() for x in my_list]


def input_from_list(valid_list: list, caseInsensitive=False, loop = False):
    choice = input()
    # Check if key exists
    if not loop:
        if caseInsensitive and choice.lower() not in list_lower(valid_list):
            return False
        elif choice not in valid_list:
            return False
    else:
        if caseInsensitive and choice.lower() not in list_lower(valid_list):
            print("Invalid selection. Please select from the following list:")
            print(*valid_list, sep=",")
            return input_from_list(valid_list, caseInsensitive, loop)
        elif choice not in valid_list:
            return input_from_list(valid_list, caseInsensitive, loop)
    return choice


def clear_dict(d):
    if not isinstance(d, dict) and not isinstance(d, list):
        return
    d_copy = d.copy()
    if isinstance(d_copy, list):
        for data in d_copy:
            clear_dict(data)
        return
    for key, value in d_copy.items():
        if isinstance(value, list):
            for data in value:
                clear_dict(data)
        elif isinstance(value, dict):
            clear_dict(value)
        else:
            if value is None:
                d.pop(key)
