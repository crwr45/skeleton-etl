from abc import ABC, abstractstaticmethod

from ..models.message import Message

class MessageType(ABC):
    
    @abstractstaticmethod
    def message_is_type(message: Message) -> bool:
        """
        Given a `Message` object, decide if it is a message of this
        `MessageType`
        """
        return False

    @abstractstaticmethod
    def prepare(message: Message):
        """
        The entrypoint for custom processing of `Message`s of this type.
        This method should read the message data and take any actions required
        by the contents.
        e.g. extract all the product definitions from a warehouse, convert
        them to a standard format, then update a standard list.
        """
        pass