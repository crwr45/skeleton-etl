import pathlib
import hashlib

from ..models.message import Message

import logging

_logger = logging.getLogger(__name__)


class LocalFilesystemConnection:
    @staticmethod
    def connect(_gateway):
        """Connect to local filesystem"""
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
