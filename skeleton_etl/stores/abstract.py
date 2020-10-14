from abc import ABC, abstractmethod
from typing import TypeVar, List, Iterator

# Define some generic types
T = TypeVar("T")
K = TypeVar("K")


class AbstractStore(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @staticmethod
    def add(self, value: T) -> K:
        """Returns key"""
        pass

    @abstractmethod
    def get(self, key: K) -> T:
        pass

    @abstractmethod
    def remove(self, key: K) -> None:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass

    @abstractmethod
    def save(self) -> None:
        """Persist values"""
        pass

    @abstractmethod
    def load(self, **kwargs) -> None:
        """Load data from external persistance mechanism. Args will vary with
        mechanism
        """
        pass

    @abstractmethod
    def dump(self) -> List[T]:
        """Returns a list of the values stored to allow for values to be
        persisted elsewhere
        """
        return list(self)
