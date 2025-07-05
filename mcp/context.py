from abc import ABC, abstractmethod
from typing import Any, Dict


class MemoryContext:
    def __init__(self):
        self.state = {}

    def read(self, key: str):
        return self.state.get(key)

    def write(self, key: str, value):
        self.state[key] = value

    def keys(self):
        return list(self.state.keys())

    def __str__(self):
        return f"MemoryContext({self.state})"
