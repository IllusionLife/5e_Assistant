import util as utl

menu_items = {"1": ("Create character", "C"),
              "2": ("View characters", "V"),
              "3": ("Delete character", "D"),
              "4": ("Add custom", "A"),
              "0": ("Exit", "E")}


def get_menu_selection():
    incorrect_selection = True
    while incorrect_selection:
        print("Please select from the main menu:")
        for key in menu_items.keys():
            value = menu_items[key][0].replace(menu_items[key][1], f"({menu_items[key][1]})")
            print(f"{key}. {value}")
        selection = input("Selected:")
        if (selection not in menu_items.keys() and
                not any(selection in nkey for nval, nkey in list(menu_items.values()))):
            utl.clear()
            print("Invalid choice.")
        else:
            incorrect_selection = False



def main_menu():
    get_menu_selection()

    return 0