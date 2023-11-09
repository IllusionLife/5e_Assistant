import menus as mm

def run():
    return mm.main_menu()

def main_loop():
    while run() != 0:
        pass

main_loop()