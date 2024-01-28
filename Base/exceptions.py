from abc import ABC, abstractmethod
from util import build_message


class BaseExceptionRPG(Exception, ABC):
    """Base exception class"""

    def __init__(self, msg, *info):
        self.msg = build_message(msg, info)
        self.log_exception()
        super().__init__(self.msg)

    @abstractmethod
    def log_exception(self):
        pass
