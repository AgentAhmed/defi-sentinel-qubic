from typing import Any, Dict

class MemoryContext:
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def read(self, key: str, default=None):
        return self.state.get(key, default)

    def write(self, key: str, value):
        self.state[key] = value

    def keys(self):
        return list(self.state.keys())

    def __str__(self):
        return f"MemoryContext({self.state})"
