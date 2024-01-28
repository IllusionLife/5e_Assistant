from Base.exit_codes import *
from Base.file_handling import FileHandlerRPG
from Base.logs import logger


class ConfigHandlerRPG(FileHandlerRPG):
    def __init__(self, confname):
        self.confs = {}
        super().__init__('./Config/', fn=confname)
        self.load_configs()

    def __conf_is_string(self, conf_key):
        if len(conf_key) > 0:
            return conf_key[0] == '"' and conf_key[-1] == '"'
        return False

    def __stringify_conf(self, conf_key):
        if not self.__conf_is_string(conf_key):
            return '"' + conf_key + '"'
        return conf_key

    def __destringify_conf(self, conf_key):
        if isinstance(conf_key, list):
            for index in range(len(conf_key)):
                conf_key[index] = self.__destringify_conf(conf_key[index])
            return conf_key
        conf_key = conf_key.strip()
        if self.__conf_is_string(conf_key):
            return conf_key[1:-1]
        elif conf_key.isdecimal():
            return int(conf_key)
        elif conf_key.isnumeric():
            return float(conf_key)
        return conf_key

    def __call__(self, other):
        if self.get_file_name() != other:
            self.close_file()
            self.set_filename(other)
            self.read_file()
            self.load_configs()

    def log_configs(self):
        for confname, confvalue in self.confs.items():
            logger().log_debug("Config <$1> = <$2>", confname, confvalue)

    def get_conf(self, conf_key, default = None):
        if conf_key in self.confs:
            return self.confs[conf_key]
        return default

    def config_exists(self, conf_key):
        if len(self.confs) == 0:
            self.load_configs()
        if conf_key in self.confs:
            return True
        return False

    def load_configs(self):
        configs = self.readFile()
        for line in configs:
            if line == "":
                continue
            line = line.split("=", 1)
            line[0] = line[0].strip(" ")
            line[1] = line[1].strip(" ")
            if line[1][0] == "[":
                line[1] = line[1].strip()[1:-1].split(",")
            self.confs[line[0]] = self.__destringify_conf(line[1])
            logger().log_debug("Config loaded: <$1> = <$2>", line[0], line[1])

    def add_config(self, config_key, value):
        self.edit_file()
        if isinstance(value, str):
            value = self.__stringify_conf(value)
        elif isinstance(value, list):
            array_of_values = value.copy()
            value = "["
            for conf_value in array_of_values:
                value += self.__stringify_conf(conf_value)
                value = ","
            value[-1] = "]"
        self.writeFile(f"{config_key}={value}")
        logger().log_info("Added config <$1> with value <$2>", config_key, value)

    def remove_config(self, conf_key):
        self.overwrite_file()
        for key, value in self.confs:
            if key != conf_key:
                self.add_config(key, value)

    def change_config(self, conf_key, conf_value):
        if not self.config_exists(conf_key):
            return EXIT_DOESNT_EXISTS
        self.overwrite_file()
        if len(self.confs) == 0:
            return
        for key, value in self.confs.items():
            if key == conf_key:
                self.add_config(conf_key, conf_value)
            else:
                self.add_config(key, value)
