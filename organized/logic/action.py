from . import logger
from ..storage.base_file import BaseFile

class Action:
    def __init__(self, source, reason, **kwargs):
        self.source = source
        self.reason = reason
        self.config = kwargs
        logger.debug("{} match - {}".format(source, reason))
