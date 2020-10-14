from abc import ABC, abstractstaticmethod

from ..models.message import Message


class SelectionPolicy(ABC):
    @abstractstaticmethod
    def message_selected(possible_message: Message) -> bool:
        """
        Examine the message to determine if it is to be imported.
        """
        return True
