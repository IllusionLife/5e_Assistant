import util as utl
import customs as cstm
import characters as chrs


def dummy():
    """
    Dummy function for menu items
    """
    print("Dummy!")
    return



menu_items = {"1": ("Create character", "C", chrs.create_character),
              "2": ("View characters", "V", dummy),
              "3": ("Delete character", "D", dummy),
              "4": ("Add custom", "A", cstm.add_new_proficiency),
              "0": ("Exit", "E", dummy)}
"""
Create a dictionary of a key (str) and a list. List must contain:
  1. Title of functionality (str)
  2. Access letter (can be left blank) (str)
  3. Reference to function of the functionality (func)
"""

def get_menu_selection():
    # Initiate variables
    selection = None
    incorrect_selection = True

    # Loop until valid selection
    while incorrect_selection:
        # Print selections to the console
        print("Please select from the main menu:")
        for key in menu_items.keys():
            value = menu_items[key][0].replace(menu_items[key][1], f"({menu_items[key][1]})")
            print(f"{key}. {value}")
        selection = input("Selected:")

        # If access letter has been provided, convert it to key value
        if any(selection in nkey for nval, nkey, nfunc in list(menu_items.values())):
            for key, val in menu_items.items():
                if val[1] == selection:
                    selection = key

        # Check if key exists
        if selection not in menu_items.keys():
            utl.clear()
            print("Invalid choice.")
        else:
            incorrect_selection = False
    # Call linked function
    menu_items[selection][2]()


def main_menu():
    get_menu_selection()

    return 0