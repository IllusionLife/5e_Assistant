from Base.exit_codes import *
from Base.file_handling import FileHandlerRPG
from Base.config_handler import ConfigHandlerRPG
from Base.logs import logger


class InterfaceRPG:
    def __init__(self):
        logger().log_info("Starting race interface")
        logger().log_debug("Initializing interface configurations")
        self.interface_conf = ConfigHandlerRPG("interfaces.conf")

    def get_files(self):
        pass