from abc import ABC, abstractmethod
from typing import Any


class AbstractStore(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @staticmethod
    def add(self, item: Any):
        """Returns key"""
        pass

    @abstractmethod
    def get(self, key: Any):
        pass

    @abstractmethod
    def remove(self, key: Any):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def load(self, **kwargs):
        pass

    @abstractmethod
    def save(self, **kwargs):
        pass
