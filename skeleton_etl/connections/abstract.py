from abc import ABC, abstractstaticmethod
from typing import Any, List
from ..models.message import Message

from ..models.gateway import Gateway
from ..selection_policies.abstract import SelectionPolicy


class Connection(ABC):

    @abstractstaticmethod
    def connect(gateway: Gateway) -> Any:
        """
        Create and return a connection object that is connected to the source
        described by `gateway`.
        This connection needs to be compatible with the `receive_inputs()`
        methods requirements for `conn`
        """
        return None
    
    @abstractstaticmethod
    def receive_inputs(conn: Any, path: str, message_selector: SelectionPolicy) -> List[Message]:
        """
        Using the connection `conn` returns from `SelectionPolicy.connect()`,
        and the `path` to search within that connection, collect new messages.
        
        `message_selector` is to be used to decide which messages to receive.
        
        Requiring message_selector to be correctly used in this custom code is not ideal. It would be
        far nicer if the possible messages were all retrieved, then the selection policy were
        *automatically* applied.
        However, this approach is currently used because the point at which sufficient information
        about the incoming message is available may vary depending on the connection. e.g. local
        filesystem compared to SFTP, or Google Drive.
        
        TODO reconsider requirement to use SelectionPolicy. Is it widely-applicable enough and in the right place?
        """
        return []