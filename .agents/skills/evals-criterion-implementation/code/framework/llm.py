from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class LLMClient(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        ...
