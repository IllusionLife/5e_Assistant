import os

abs_path = os.path.dirname(os.path.abspath(__file__))

ENTITY_SIZES = ("tiny", "small", "medium", "large", "gargantuan")
YN_CONST = ('y', 'n', 'yes', 'no')

# Defaults
DEFAULT_LOG_LEVEL = 1
DEFAULT_LOG_DIR = "./Logs/"
DEFAULT_FILENAME_FORMAT = "log_<$time>.log"
DEFAULT_FILENAME_TIME_FORMAT = "%Y%m%d"
DEFAULT_TIME_FORMAT = "%Y-%b-%d %H:%M:%S"
DEFAULT_MAX_LOG_COUNT = 30
