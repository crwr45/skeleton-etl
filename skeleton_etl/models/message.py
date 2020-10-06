from dataclasses import dataclass
from typing import Any

import logging
_logger = logging.getLogger(__name__)


@dataclass
class Message:
    name: str
    src_message_name: str
    src_message_hash: str
    data: str
    type: Any = None


    def prepare(self):
        _logger.info(f"Preparing {self.name}")
        self.type.prepare(self)
        _logger.info(f"Done Preparing {self.name}")
