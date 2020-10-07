from .abstract import AbstractStore


class InMemoryStore(AbstractStore):
    def __init__(self):
        self._store = {}

    def __len__(self):
        return len(self._store)

    def __iter__(self):
        for _, value in sorted(self._store.items()):
            yield value

    def _get_next_key(self):
        return len(self._store)

    def add(self, value):
        key = self._get_next_key()
        self._store[key] = value
        return key

    def get(self, key):
        return self._store[key]

    def remove(self, key):
        self._store.pop(key, None)

    def dump(self):
        return list(self)

    def load(self, values: list):
        for v in values:
            self.add(v)

    def save(self):
        """For in memory store there is no need to save anything"""
        pass
