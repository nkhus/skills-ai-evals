from abc import ABC, abstractmethod
from typing import Any

from .models import ExecutionArtifact


class Executor(ABC):
    @abstractmethod
    async def execute(self, input: dict[str, Any]) -> ExecutionArtifact:
        ...
