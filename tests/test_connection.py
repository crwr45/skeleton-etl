from pathlib import Path
import os.path

import pytest

from skeleton_etl.models.gateway import Gateway
from skeleton_etl.connections.filesystem import (
    LocalFilesystemConnection,
    LocalFilesystemConnectionSettings,
)
from skeleton_etl.selection_policies.all import SelectionPolicyAll


TEST_DIR = Path(os.path.abspath(__file__)).parent.absolute()
DATA_DIR = TEST_DIR / "data"


@pytest.fixture
def root_path():
    return DATA_DIR


@pytest.fixture
def good_gateway(root_path):
    return Gateway(
        path=str(DATA_DIR),
        connection_settings=LocalFilesystemConnectionSettings(root_path=root_path),
        connection_type=LocalFilesystemConnection,
        message_selection_policy=SelectionPolicyAll,
    )


@pytest.fixture
def bad_gateway():
    class IncorrectConnectionSettings:
        pass

    return Gateway(
        path=str(DATA_DIR),
        connection_settings=IncorrectConnectionSettings(),
        connection_type=LocalFilesystemConnection,
        message_selection_policy=SelectionPolicyAll,
    )


def test_good_local_collection(good_gateway, root_path):
    conn = LocalFilesystemConnection()
    con_path = conn.connect(good_gateway)
    assert con_path == root_path


def test_bad_connection(bad_gateway):
    conn = LocalFilesystemConnection()
    with pytest.raises(TypeError):
        conn.connect(bad_gateway)
