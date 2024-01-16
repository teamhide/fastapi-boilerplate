from abc import ABC, abstractmethod
from typing import Callable


class BaseKeyMaker(ABC):
    @abstractmethod
    async def make(self, *, function: Callable, prefix: str) -> str:
        """Base key maker"""
