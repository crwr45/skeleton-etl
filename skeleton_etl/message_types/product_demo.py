from csv import DictReader
from io import StringIO

from .abstract import MessageType

import logging

_logger = logging.getLogger(__name__)


class ProductMessage(MessageType):
    @staticmethod
    def message_is_type(message):
        return True

    @staticmethod
    def prepare(message):
        _logger.info("Preparing", message.name)
        reader = DictReader(StringIO(message.data.decode("utf-8")))
        for row in reader:
            print(row)
        _logger.info("Preparing", message.name)
