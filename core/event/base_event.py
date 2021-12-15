from abc import ABC, abstractmethod
from typing import Type, Union

from pydantic import BaseModel


class BaseEvent(ABC):
    @abstractmethod
    async def run(self, parameter: Union[Type[BaseModel], None]) -> None:
        pass
