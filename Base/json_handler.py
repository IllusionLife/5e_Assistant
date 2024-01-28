import atexit
import json

from Base.exit_codes import *
from Base.file_handling import FileHandlerRPG
from Base.exceptions import BaseExceptionRPG
from Base.logs import logger, LogLL


class JsonException(BaseExceptionRPG):
    """Raised when there is an issue, related to file reading/writing"""

    def __init__(self, msg, filename, *add_info):
        super().__init__(msg, filename, *add_info)

    def log_exception(self):
        logger().log_by_level(self.msg, LogLL.ERROR)


class JsonHandlerRPG(FileHandlerRPG):
    json_conf = None

    def __init__(self, jsondir: str = "", jsonfile: str = ""):
        logger().log_debug("Creating JSONHandlerRPG instance.")
        self.json_content = None
        super().__init__(fd=jsondir, fn=jsonfile)
        if jsondir != "" and jsonfile != "":
            self.load_json()
        atexit.register(self.__close)

    def __close(self):
        logger().log_debug("Destroying JSONHandlerRPG instance.")

    def __call__(self, fdir, fname):
        if self.get_path() != (fdir + fname):
            self.close_file()
            self.json_content = None
            self.set_path(fdir, fname)
            self.read_file()
            self.load_json()

    def __print(self, arr: list = None, **kwargs):
        indent = kwargs.get("indent", 0)
        indentstr = "  " * indent
        if kwargs.get("node_to_print", None) is not None:
            for node in kwargs["node_to_print"].split("/"):
                indentstr = "  " * indent
                title = f"{indentstr}### {node.upper()} ###"
                print(title)
                print(f"{indentstr}{'^' * (len(title) - 1)}")
                self.__print(node, indent=indent + 1, specific_key=kwargs.get('specific_key', None))
                arr = arr[node]
                indent += 1

            for data_dict in arr:
                for key, value in data_dict.items():
                    specif_tag = kwargs.get('specific_key', None)
                    if specif_tag is None:
                        print(f"{indentstr} - {key.upper()} : {value}")
                    elif specif_tag.upper() == key.upper():
                        print(f"{indentstr} - {key.upper()} : {value}")
                print(f"{indentstr}------------------------")
        elif isinstance(arr, dict):
            for datatype, dictarr in arr.items():
                title = f"{indentstr}### {datatype.upper()} ###"
                print(title)
                print(f"{indentstr}{'^' * (len(title) - 1)}")
                self.__print(dictarr, indent=indent + 1, specific_key=kwargs.get('specific_key', None))
                print(f"{indentstr}### END {datatype.upper()} ###")
        elif isinstance(arr, list):
            for data_dict in arr:
                for key, value in data_dict.items():
                    specif_tag = kwargs.get('specific_key', None)
                    if specif_tag is None:
                        print(f"{indentstr} - {key.upper()} : {value}")
                    elif specif_tag.upper() == key.upper():
                        print(f"{indentstr} - {key.upper()} : {value}")
                print(f"{indentstr}------------------------")

    def print(self, **kwargs):
        self.__print(self.json_content, **kwargs)

    def __get_content(self):
        return self.json_content

    def is_loaded(self):
        if self.__get_content() is None:
            return False
        return True

    def __dump(self):
        json.dump(self.__get_content(), self.fp, indent=2)

    def pointer_to_tag(self, tags):
        if not self.is_loaded():
            self.load_json()

        if "/" in tags:
            tags = tags.split("/")

        if not isinstance(tags, list):
            tags = [tags]

        json_ptr = self.json_content
        for tag in tags:
            json_ptr = json_ptr[tag]
        return json_ptr

    def load_json(self, jsondir: str = "", jsonfile: str = ""):
        if self.is_loaded():
            self.close_file()
        if jsondir != "" and jsonfile != "" and self.get_path() != "":
            logger().log_info("File data has been altered.\nOld4 file <$1>\nNew file <$2>"
                              , self.fp.name
                              , jsondir + jsonfile)
            self.set_path(fdir=jsondir, fname=jsonfile)

        try:
            self.read_file(init_content="{}")
            self.json_content = json.load(self.fp)
        except (Exception, json.decoder.JSONDecodeError) as exc:
            raise JsonException("Unable to load JSON file <$1>. Reason:", self.get_file_name(), str(exc))

    def delete_id(self, nodes, id_value):
        if not self.is_loaded():
            raise JsonException("JSON not loaded. Unable to delete content."
                                , ("set_path", self.get_path())
                                , ("id", id_value)
                                , ("nodes", nodes))
        nodes = nodes.split("/")
        json_ptr = self.json_content

        # Iterate through each part in the provided tag (if tag consists of multiple)
        # and delete id_value in given json array
        for key in nodes:
            if key == nodes[-1]:
                for index in range(len(json_ptr[key])):
                    if json_ptr[key][index]["id"] == id_value:
                        del json_ptr[key][index]
                        self.save_json()
                        logger().log_debug("ID <$1> deleted.", id_value)
                        return EXIT_SUCCESS
                logger().log_error("ID <$1> not found", id_value)
                return EXIT_UNEXPECTED_FAIL
            json_ptr = json_ptr.get(key, False)
        logger().log_error("Tag not found!")
        return EXIT_UNEXPECTED_FAIL

    def id_exists(self, nodes, id_value):
        if not self.is_loaded():
            self.load_json()

        # Create a pointer to iterate through json list
        json_ptr = self.__get_content()
        nodes = nodes.split("/")

        # Iterate through each part in the provided tag (if tag consists of multiple )
        # and check if id_value exists in given json array
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

    def add_to_json_list(self, nodes, id_value, block_to_add):
        if not self.is_loaded():
            raise JsonException("JSON not loaded. Unable to check if"
                                , ("set_path", self.get_path())
                                , ("id", id_value)
                                , ("nodes", nodes))

        if self.id_exists(nodes, id_value):
            print("Data with id <" + id_value + "> already exists!")
            return False

        json_ptr = self.__get_content()
        nodes = nodes.split("/")

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
        return self.save_json()

    def save_json(self):
        try:
            self.close_file()
            self.overwrite_file()
            self.__dump()
            self.close_file()
            self.read_file()
        except Exception as exc:
            JsonException("Unable to save JSON file.", self.get_file_name(), str(exc))
            return EXIT_FILE_ERROR
        return EXIT_SUCCESS
