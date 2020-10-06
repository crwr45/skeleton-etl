from dataclasses import dataclass, field
from typing import Any, List, Union

from .transfer import Transfer


@dataclass
class Gateway:
    """
    Describes a place from which messages can be obtained.
    TODO more
    """
    path: str
    address: Union[str, None]
    connection_type: Any
    message_selection_policy: Any
    transfers: List[Transfer] = field(default_factory=list)

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
        self.transfers.append(transfer)
        try:
            Connection = self.connection_type
            conn = Connection.connect(self)
            transfer.do_transfer(conn)
        except Exception as err:
            transfer.raise_issue(f"Transfer failed: {err}")
            raise err
