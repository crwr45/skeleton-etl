import pathlib
import hashlib
from dataclasses import dataclass, field
from typing import Union

from ..models.message import Message
from .abstract import Connection

import logging

_logger = logging.getLogger(__name__)


@dataclass
class LocalFilesystemConnectionSettings:

    root_path: Union[str, pathlib.Path, None] = field(default=None)


class LocalFilesystemConnection(Connection):

    connection_settings_type = LocalFilesystemConnectionSettings

    @classmethod
    def connect(cls, gateway):
        """Connect to local filesystem"""
        settings = gateway.connection_settings
        cls._check_connection_settings_type(settings)

        if settings.root_path:
            return pathlib.Path(settings.root_path).absolute()
        else:
            return pathlib.Path(pathlib.Path().absolute().root)

    @classmethod
    def receive_inputs(cls, conn, path, message_selector):

        print(conn, path)
        directory = conn.joinpath(path)

        possible_files = directory.iterdir()

        messages = []
        for filepath in possible_files:
            if not message_selector.message_selected(filepath):
                continue

            data = filepath.read_bytes()
            file_hash = hashlib.sha512(str(data).encode()).hexdigest()
            message = Message(
                name=filepath.name,
                src_message_name=filepath.name,
                src_message_hash=file_hash,
                data=data,
            )

            if cls.check_message_consistency(message, filepath):
                messages.append(message)

        return messages

    @staticmethod
    def check_message_consistency(message: Message, filepath: pathlib.Path) -> bool:
        return len(message.data) == filepath.stat().st_size
