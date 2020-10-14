"""
a pseudo-singleton defined as a module to track possible document types.
"""
from typing import Type
from .abstract import MessageType
from ..models.message import Message

import logging

_logger = logging.getLogger(__name__)


# TODO:  "message" used too many times.

registry = []
sorted_types = []


class EntryNotFoundError(Exception):
    pass


def register_type(new_type: Type[MessageType], priority):
    qual_name = new_type.__qualname__
    _logger.info(f"registering {qual_name} at priority {priority}")

    if qual_name in registry:
        raise KeyError(f"{qual_name} is already registered")
    if not hasattr(new_type, "message_is_type") or not hasattr(new_type, "prepare"):
        raise TypeError(f"{new_type} does not have required methods")

    registry.append(qual_name)
    sorted_types.append((priority, new_type))
    sorted_types.sort(key=lambda i: i[0])

    _logger.debug(f"current registry: {registry}")


def find_type_for_message(message: Message) -> Type[MessageType]:
    for _prio, message_type in sorted_types:
        if message_type.message_is_type(message):
            _logger.debug(f"{message_type} matched {message.name}")
            return message_type
        _logger.debug(f"{message_type} does not match {message.name}")
    raise EntryNotFoundError(f"no match found for {message}")
