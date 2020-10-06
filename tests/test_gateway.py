from pathlib import Path
import os.path
from unittest import mock

import pytest

from skeleton_etl.models.gateway import Gateway
from skeleton_etl.models.transfer import Transfer
from skeleton_etl.connections.filesystem import LocalFilesystemConnection
from skeleton_etl.selection_policies.all import SelectionPolicyAll

from skeleton_etl.message_types.product_demo import ProductMessage
from skeleton_etl.message_types import type_registry


TEST_DIR = Path(os.path.abspath(__file__)).parent.absolute()

DATA_DIR = TEST_DIR / "data"


@pytest.fixture(scope="session")
def register_product_demo_type():
    type_registry.register_type(ProductMessage, 10)


@pytest.fixture
def gateway(register_product_demo_type):
    return Gateway(
        path=str(DATA_DIR),
        address=None,
        connection_type=LocalFilesystemConnection,
        message_selection_policy=SelectionPolicyAll,
    )


def test_gateway(gateway):
    assert len(gateway.transfers) == 0


def test_gateway_do_transfer_exception(gateway):
    def raise_exception(*args, **kwargs):
        raise BrokenPipeError

    with mock.patch.object(Transfer, "receive_inputs") as patched:
        patched.side_effect = raise_exception
        with pytest.raises(BrokenPipeError):
            gateway.do_transfer()


def test_gateway_do_transfer(gateway):
    gateway.do_transfer()
    assert len(gateway.transfers) == 1
