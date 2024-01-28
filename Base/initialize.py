from Base.logs import logger
from Base.config_handler import ConfigHandlerRPG

def init_logs():
    logger().log_debug("Logs initialized.")
    log_configs = ConfigHandlerRPG("log.conf")
    logger().change_log_level(log_configs.get_conf("LOG_LEVEL"))
    log_configs.log_configs()

    logger().set_configs(loglvl=log_configs.get_conf("LOG_LEVEL")
                         , logformat=log_configs.get_conf("LOG_FORMAT")
                         , filetimeformat=log_configs.get_conf("FILE_TIME_FORMAT")
                         , logdir=log_configs.get_conf("LOG_DIR")
                         , timeformat=log_configs.get_conf("TIME_FORMAT")
                         , maxlogs=log_configs.get_conf("MAX_LOG_COUNT"))

    logger().log_info("Logs configured.")

def initializeRPG():
    logger().log_info("Initializing program.")
    init_logs()




