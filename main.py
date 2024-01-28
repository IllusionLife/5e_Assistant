import menus as mm
from Base.initialize import initializeRPG
from Base.exit_codes import *


def run():
    return mm.main_menu()


def main_loop():
    while run() != EXIT_CLOSE:
        pass


initializeRPG()
main_loop()


