import atexit
from datetime import datetime as dt
from enum import Enum
import re
import os

from Base.exit_codes import EXIT_FILE_ERROR
import globals

from util import build_message
from Base.file_handling import FileHandlerRPG, FileExceptionRPG
from Base.exceptions import BaseExceptionRPG


class LogLL(Enum):
    DEBUG = 0
    INFO = 1
    ERROR = 2
    CRITICAL = 3


class LogExceptionRPG(BaseExceptionRPG):
    """Raised when there is an issue, related to log writing"""

    def __init__(self, msg, filename, *add_info):
        super().__init__(msg, filename, *add_info)

    def log_exception(self):
        try:
            logger().log_by_level(self.msg, LogLL.ERROR)
        except FileExceptionRPG:
            print("Error creating log. Exiting...")
            exit(EXIT_FILE_ERROR)


class LogRPG(FileHandlerRPG):
    mainLog = None

    def __init__(self, logname: str = ""):
        self.open_time = dt.now()
        self.log_level = LogLL(globals.DEFAULT_LOG_LEVEL)
        self.time_format = globals.DEFAULT_TIME_FORMAT
        self.log_format = globals.DEFAULT_FILENAME_FORMAT
        self.log_name = ""
        self.max_cnt = None
        if logname != "":
            self.log_name = logname
        else:
            file_time_format = globals.DEFAULT_FILENAME_TIME_FORMAT
            self.log_name = self.log_format.replace("<$time>", self.open_time.strftime(file_time_format))
        super().__init__(fd=globals.DEFAULT_LOG_DIR, fn=self.log_name)
        try:
            self.edit_file()
        except Exception as exc:
            exit(EXIT_FILE_ERROR)
        atexit.register(self._close)

    def set_configs(self, **kwargs):
        if "maxlogs" in kwargs:
            self.max_cnt = kwargs["maxlogs"]
        if "loglvl" in kwargs:
            self.log_level = LogLL(kwargs["loglvl"])
        if "timeformat" in kwargs:
            self.time_format = kwargs["timeformat"]
        if "logformat" in kwargs:
            self.log_format = kwargs["logformat"]
            logdir = globals.DEFAULT_LOG_DIR
            filetimeformat = globals.DEFAULT_FILENAME_TIME_FORMAT
            if "filetimeformat" in kwargs:
                filetimeformat = kwargs["filetimeformat"]
            if "logdir" in kwargs:
                logdir = kwargs["logdir"]
            self.log_name = self.log_format.replace("<$time>", self.open_time.strftime(filetimeformat))
            super().move_file(self.log_name, logdir)
            try:
                self.edit_file()
            except Exception as exc:
                exit(EXIT_FILE_ERROR)

    def _close(self):
        close_time = dt.now()
        self.clean_old_logs()
        self.log_info("Closing file.")
        self.log_debug(f"Time worked: {close_time - self.open_time}")

    def change_log_level(self, loglevel):
        self.log_level = LogLL(loglevel)

    def get_log_level(self):
        return self.log_level

    def get_stamp(self, level: int = -1):
        curr_lvl = int()
        if level != -1:
            curr_lvl = level
        else:
            curr_lvl = self.get_log_level()

        stamp = str()
        if curr_lvl == LogLL.INFO:
            stamp = "[INFO]"
        elif curr_lvl == LogLL.DEBUG:
            stamp = "[DEBUG]"
        elif curr_lvl == LogLL.ERROR:
            stamp = "[ERROR]"
        elif curr_lvl == LogLL.CRITICAL:
            stamp = "[CRITICAL]"
        else:
            # TODO add proper exception
            stamp = "[???]"
        res = stamp.ljust(10, ' ') + " (" + dt.now().strftime(self.time_format) + ") -> "
        return res

    def __log(self, msg, level):
        if level.value >= self.log_level.value:
            self.writeFile(self.get_stamp(level) + msg)

    def log_by_level(self, message, level):
        self.writeFile(self.get_stamp(level) + message)

    def log_info(self, message, *add_info):
        message = build_message(message, *add_info)
        self.__log(message, LogLL.INFO)

    def log_debug(self, message, *add_info):
        message = build_message(message, *add_info)
        self.__log(message, LogLL.DEBUG)

    def log_error(self, message, *add_info):
        message = build_message(message, *add_info)
        self.__log(message, LogLL.ERROR)

    def log_critical(self, message, *add_info):
        message = build_message(message, *add_info)
        self.__log(message, LogLL.CRITICAL)

    def clean_old_logs(self):
        if self.max_cnt is None:
            return
        list_logs = os.listdir(self.get_file_dir())
        for log in list_logs:
            if len(list_logs) < self.max_cnt + 1:
                break
            if re.match(fr"{self.log_format.replace('<$time>', '.+')}", log):
                os.remove(self.get_file_dir() + log)
                list_logs.remove(log)

    @staticmethod
    def logger():
        if LogRPG.mainLog is None:
            LogRPG.mainLog = LogRPG()
        return LogRPG.mainLog


def logger():
    return LogRPG.logger()
