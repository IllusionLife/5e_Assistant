import atexit
from os import path, remove, makedirs, listdir
import shutil

import util
from Base.exit_codes import EXIT_SUCCESS
from Base.exceptions import BaseExceptionRPG


class FileExceptionRPG(BaseExceptionRPG):
    """Raised when there is an issue, related to file reading/writing"""

    def __init__(self, msg, filename, *add_info):
        super().__init__(msg, filename, *add_info)

    def log_exception(self):
        print(self.msg)
        pass


class FileHandlerRPG:
    FILE_READ_MODE = "r"
    FILE_WRITE_MODE = "w+"
    FILE_APPEND_MODE = "a+"

    def __init__(self, fd="", fn=""):
        if fd[-1:] != '/':
            fd = fd + '/'
        if fd[:2] == "./":
            abs_path = path.dirname(path.abspath(__file__)).replace("\\", "/") + '/'
        self.file_dir = fd
        self.file_name = fn
        self.fp = None
        atexit.register(self.__close)

    def __close(self):
        if self.is_file_open():
            self.fp.close()

    def get_file_mode(self):
        return self.fp.mode

    def set_filename(self, filename):
        self.file_name = filename

    def set_filedir(self, filedir):
        self.file_dir = filedir

    def set_path(self, fdir: str, fname: str):
        if fdir != "" and fdir[-1] != "/":
            fdir += "/"
        self.file_dir = fdir
        self.file_name = fname

    def get_file_name(self):
        return self.file_name

    def get_file_dir(self):
        return self.file_dir

    def get_path(self):
        return str(self.file_dir + self.file_name)

    def is_file_open(self):
        if self.fp:
            return True
        return False

    def move_file(self, newfilename:str, newfiledir:str = ""):
        current_access_mode = self.fp.mode
        self.close_file()
        shutil.move(self.get_path(), newfiledir + newfilename)
        self.set_filename(newfilename)
        if newfiledir != "":
            self.set_filedir(newfiledir)
        if current_access_mode != self.FILE_READ_MODE:
            self.__access_file(self.FILE_APPEND_MODE)
            return
        self.__access_file(self.FILE_READ_MODE)


    def close_file(self):
        if not self.is_file_open():
            errmsg = util.build_message("Attempted closing of unopened file.", self.get_path())
            raise Exception(errmsg)
        self.fp.close()

    def __access_file(self, access_mode: str, filedir: str = "", filename: str = "", init_content: str = ""):
        if self.is_file_open() and self.fp.name != self.get_path():
            # TODO add behaviour for change of file
            pass
        if self.get_path() == "":
            if filedir and filename:
                self.set_path(filedir, filename)
            else:
                errmsg = util.build_message("Unable to open file."
                                            , ("file_path", filedir)
                                            , ("file_name", filename))
                raise Exception(errmsg)
        if not self.dir_exists(self.get_file_dir()):
            makedirs(self.get_file_dir())
        if self.file_exists(self.get_path()):
            self.fp = open(self.get_path(), access_mode)
        else:
            self.fp = open(self.get_path(), self.FILE_WRITE_MODE)
            self.fp.write(init_content)

    def read_file(self, filedir: str = "", filename: str = "", init_content: str = ""):
        self.__access_file(self.FILE_READ_MODE, filedir, filename, init_content)

    def edit_file(self, filedir: str = "", filename: str = "", init_content: str = ""):
        self.__access_file(self.FILE_APPEND_MODE, filedir, filename, init_content)

    def overwrite_file(self, filedir: str = "", filename: str = "", init_content: str = ""):
        self.__access_file(self.FILE_WRITE_MODE, filedir, filename, init_content)

    def writeFile(self, msg):
        if not self.is_file_open() and self.get_path() == "":
            errmsg = util.build_message("File not open. Attempted print of message: ", msg)
            raise Exception(errmsg)
        elif not self.is_file_open() or self.get_file_mode() == self.FILE_READ_MODE:
            self.edit_file()
        self.fp.write(msg + "\n")

    def readFile(self):
        if not self.is_file_open() and not self.get_path():
            errmsg = util.build_message("File not open. Unable to read file")
            raise Exception(errmsg)
        elif not self.is_file_open() or self.get_file_mode() != self.FILE_READ_MODE:
            self.read_file()
        return self.fp.read().splitlines()

    def readFileLine(self):
        if not self.is_file_open() and not self.get_path():
            errmsg = util.build_message("File not open. Unable to read file")
            raise Exception(errmsg)
        elif not self.is_file_open() or self.get_file_mode() != self.FILE_READ_MODE:
            self.read_file()
        return self.fp.readline()

    @staticmethod
    def create_file(filename: str, filedir: str = "", content=""):
        if not FileHandlerRPG.dir_exists(filedir):
            makedirs(filedir)
        if FileHandlerRPG.file_exists(filedir + filename):
            errmsg = util.build_message("File already exists.", filedir + filename)
            raise Exception(errmsg)
        with open(filedir + filename, "w") as file:
            file.write(content)
        return EXIT_SUCCESS


    @staticmethod
    def file_exists(file_path):
        if path.isfile(file_path):
            return True
        return False

    @staticmethod
    def dir_exists(dir_path):
        if path.exists(dir_path):
            return True
        return False

    @staticmethod
    def delete_file(filename: str, filedir: str = ""):
        if path.exists(filedir) and path.isfile(filedir + filename):
            remove(filedir + filename)
        return False

    @staticmethod
    def list_files(fdir:str):
        return listdir(fdir)