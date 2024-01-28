import util as utl
import customs as cstm
from Base.logs import logger
from Base.exit_codes import *
from Base.gui import *
from Data import characters as chrs
from Data import races as race


def exit_menu():
    return EXIT_CLOSE


def back_menu():
    return EXIT_BACK


def dummy():
    """
    Dummy function for menu items
    """
    logger().log_debug("Dummy!")
    return


def set_log_level():
    level_selection = input("Please select log level: ")
    if not level_selection.isdigit():
        logger().log_error("Invalid option for log level.")
        return EXIT_INVALID_INPUT
    level_selection = int(level_selection)
    if 0 <= level_selection <= 3:
        logger().change_log_level(level_selection)
    return EXIT_SUCCESS


def call_menu_selection(menu_items):
    # Initiate variables
    selection = None
    incorrect_selection = True

    # Loop until valid selection
    while incorrect_selection:
        # Print selections to the console
        print("Please select an option from the menu:")
        for key in menu_items.keys():
            if key is None:
                continue
            value = menu_items[key][0]
            if menu_items[key][1] is not None or menu_items[key][1] == "":
                value.replace(menu_items[key][1], f"({menu_items[key][1]})")
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
    return menu_items[selection][2]()


def configs():
    configs_menu = {
        "1": ("Add configuration", "P", dummy),
        "2": ("Edit configuration", "R", dummy),
        "3": ("Delete configuration", "r", dummy),
        "0": ("Back", "B", back_menu)
    }
    """
    Menu for configurations.
    Create a dictionary of a key (str) and a list. List must contain:
      1. Title of functionality (str)
      2. Access letter (can be left blank) (str)
      3. Reference to function of the functionality (func)
    """


def add_custom_menu():
    custom_menu = {
        "1": ("Proficiency", "P", proficiency_menu),
        "2": ("Race", "R", races_menu),
        "4": ("Trait", "T", trait_menu),
        "0": ("Back", "B", back_menu)
    }
    """
    Menu for customisations.
    Create a dictionary of a key (str) and a list. List must contain:
      1. Title of functionality (str)
      2. Access letter (can be left blank) (str)
      3. Reference to function of the functionality (func)
    """

    utl.clear()
    exitcode = call_menu_selection(custom_menu)
    if exitcode == EXIT_BACK:
        return EXIT_REPEAT
    elif exitcode == EXIT_REPEAT:
        return add_custom_menu()
    return exitcode


def proficiency_menu():
    custom_prof_menu = {
        "1": ("New", "N", cstm.new_proficiency),
        "2": ("Edit", "E", dummy),
        "3": ("Delete", "D", cstm.remove_proficiency),
        "4": ("List", "L", cstm.list_proficiency),
        "0": ("Back", "B", back_menu)
    }
    """
    Menu for proficiency customisations.
    Create a dictionary of a key (str) and a list. List must contain:
      1. Title of functionality (str)
      2. Access letter (can be left blank) (str)
      3. Reference to function of the functionality (func)
    """

    utl.clear()
    exitcode = call_menu_selection(custom_prof_menu)
    if exitcode == EXIT_BACK:
        return EXIT_REPEAT
    elif exitcode == EXIT_REPEAT:
        return proficiency_menu()
    return exitcode

def trait_menu():
    custom_traits_menu = {
        "1": ("New", "N", cstm.new_trait),
        "2": ("Edit", "E", dummy),
        "3": ("Delete", "D", cstm.remove_race),
        "0": ("Back", "B", back_menu)
    }
    """
    Menu for trait customisations.
    Create a dictionary of a key (str) and a list. List must contain:
      1. Title of functionality (str)
      2. Access letter (can be left blank) (str)
      3. Reference to function of the functionality (func)
    """
    utl.clear()
    exitcode = call_menu_selection(custom_traits_menu)
    if exitcode == EXIT_BACK:
        return EXIT_REPEAT
    elif exitcode == EXIT_REPEAT:
        return trait_menu()
    return exitcode

def races_menu():
    custom_races_menu = {
        "1": ("New", "N", race.add_race_from_file),
        "2": ("Edit", "E", dummy),
        "3": ("Delete", "D", cstm.remove_race),
        "0": ("Back", "B", back_menu)
    }
    """
    Menu for race customisations.
    Create a dictionary of a key (str) and a list. List must contain:
      1. Title of functionality (str)
      2. Access letter (can be left blank) (str)
      3. Reference to function of the functionality (func)
    """

    utl.clear()
    exitcode = call_menu_selection(custom_races_menu)
    if exitcode == EXIT_BACK:
        return EXIT_REPEAT
    elif exitcode == EXIT_REPEAT:
        return races_menu()
    return exitcode


def main_menu():
    main_menu_window = WindowRPG("Main menu")
    main_menu_frame = WindowFrameRPG(main_menu_window, "Menu frame")
    txtbox: FrameWidgetRPG = main_menu_frame.add_textbox("Testbox", 200, text="Insert text here")
    txtbox.disable_widget()

    return main_menu_window.loop()
