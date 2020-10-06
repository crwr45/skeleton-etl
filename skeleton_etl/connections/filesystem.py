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
    
    @staticmethod
    def receive_inputs(conn, path, message_selector):

        print(conn, path)
        directory = conn.joinpath(path)

        possible_files = directory.iterdir()
    
        messages = []
        for filepath in possible_files:
            if not message_selector.message_selected(filepath):
                continue

            data = filepath.read_bytes()
            hash = hashlib.sha512(str(data).encode()).hexdigest()
            messages.append(Message(
                name=filepath.name,
                src_message_name=filepath.name,
                src_message_hash=hash,
                data=data,
            ))
            # TODO: check file has been loaded completely. e.g. Size should match on disk.
        return messages
