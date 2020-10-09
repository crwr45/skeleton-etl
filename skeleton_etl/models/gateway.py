from dataclasses import dataclass, field
from typing import Any, List, Dict

from .transfer import Transfer
from ..stores.abstract import AbstractStore
from ..stores.memory import InMemoryStore


@dataclass
class Gateway:
    """
    Describes a place from which messages can be obtained.
    TODO more
    """

    path: str
    connection_settings: Dict[str, Any]
    connection_type: Any
    message_selection_policy: Any
    transfers: AbstractStore = field(default_factory=InMemoryStore)

    # TODO: auth for types that need it.
    # TODO: Odoo EDI has the concept of multiple paths for a single gateway. Consider

    def do_transfer(self):
        """
        Connect to the described resource and retrieve messages.

        This has very high-level exception logging to permit connectivity errors
        to be logged by the error logging mechanism.
        If per-message error handling is needed to allow individual messages to
        be error without ending the entire transfer then the developer needs to
        consider exactly where to introduce it. Pay careful attention to the
        consistency requirements and implications.
        """
        transfer = Transfer(self)
        self.transfers.add(transfer)
        try:
            Connection = self.connection_type
            conn = Connection.connect(self)
            transfer.do_transfer(conn)
        except Exception as err:
            transfer.raise_issue(f"Transfer failed: {err}")
            raise err
