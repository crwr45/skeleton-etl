from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Union

from .message import Message
from ..message_types.product_demo import ProductMessage

from ..message_types import type_registry
from ..stores.abstract import AbstractStore
from ..stores.memory import InMemoryStore

import logging

_logger = logging.getLogger(__name__)


@dataclass
class Transfer:
    """
    Records a single connection and its outcome(s)
    """

    gateway: Any
    messages: AbstractStore = field(default_factory=InMemoryStore)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # TODO: relations to messages created, and to issues raised

    def raise_issue(self, msg):
        _logger.error(f"Transfer Issue: {msg}")

    def do_transfer(self, connection):
        _logger.info(f"{self} transfer complete")
        self.receive_inputs(connection)
        for inp in self.messages:
            try:
                inp.prepare()
            except Exception as err:
                self.raise_issue(f"Message preparation failed: {err}")
        _logger.info(f"{self} transfer complete")

    def receive_inputs(self, connection):
        Connection = self.gateway.connection_type
        SelectionPolicy = self.gateway.message_selection_policy
        for message in Connection.receive_inputs(connection, self.gateway.path, SelectionPolicy):
            message.type = type_registry.find_type_for_message(message)
            _logger.debug(f"Determined type {message.type} for message {message.name}")
            self.messages.add(message)
        _logger.debug(f"transfer at {self.timestamp} got {len(self.messages)} new messages")
