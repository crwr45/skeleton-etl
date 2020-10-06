from csv import DictReader
from skeleton_etl.message_types.type_registry import EntryNotFoundError
import pytest

from skeleton_etl.message_types import type_registry

from skeleton_etl.message_types.product_demo import ProductMessage
from skeleton_etl.models.message import Message


@pytest.fixture
def empty_registry():
    old_reg = type_registry.registry
    old_sorted = type_registry.sorted_types
    type_registry.registry = []
    type_registry.sorted_types = []
    yield
    type_registry.registry = old_reg
    type_registry.sorted_types = old_sorted


def test_register_type(empty_registry):
    type_registry.register_type(ProductMessage, 10)
    with pytest.raises(KeyError):
        type_registry.register_type(ProductMessage, 10)
    with pytest.raises(TypeError):
        type_registry.register_type(DictReader, 10)


def test_find_type_for_message(empty_registry):
    message = Message("Test Message", "product_catalogue.csv", "None", "None")

    with pytest.raises(type_registry.EntryNotFoundError):
        type_registry.find_type_for_message(message)

    type_registry.register_type(ProductMessage, 10)
    actual = type_registry.find_type_for_message(message)
    assert actual == ProductMessage