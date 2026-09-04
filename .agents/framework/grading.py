from abc import ABC, abstractmethod

from .models import ExecutionArtifact, Grade, TestCase


class Grader(ABC):
    @abstractmethod
    async def grade(
        self,
        case: TestCase,
        artifact: ExecutionArtifact,
    ) -> Grade:
        ...
