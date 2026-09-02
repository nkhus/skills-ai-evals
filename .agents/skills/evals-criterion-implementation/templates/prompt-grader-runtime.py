from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Mapping, Protocol, TypeVar

from pydantic import BaseModel

# Replace with the repository's shared Grade contract.
from evals.shared.schemas import Grade


ResponseT = TypeVar("ResponseT", bound=BaseModel)


class StructuredLLMClient(Protocol):
    async def complete_structured(
        self,
        *,
        prompt: str,
        response_model: type[ResponseT],
    ) -> ResponseT:
        ...


class PromptRenderer(Protocol):
    def render(
        self,
        template: str,
        variables: Mapping[str, Any],
    ) -> str:
        ...


class RetryPolicy(Protocol):
    async def run(self, operation: Any) -> Any:
        ...


class GraderTelemetry(Protocol):
    def record_success(self, *, criterion: str, version: str) -> None:
        ...

    def record_error(
        self,
        *,
        criterion: str,
        version: str,
        error: Exception,
    ) -> None:
        ...


class PromptGraderDefinition(Protocol[ResponseT]):
    criterion: str
    version: str
    response_model: type[ResponseT]
    prompt_template: str

    def build_variables(
        self,
        *,
        record: Mapping[str, Any],
        artifact: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        ...

    def to_grade(self, result: ResponseT) -> Grade:
        ...


@dataclass(frozen=True)
class PromptGraderDependencies:
    llm_client: StructuredLLMClient
    renderer: PromptRenderer
    retry_policy: RetryPolicy | None = None
    telemetry: GraderTelemetry | None = None


class PromptGrader(Generic[ResponseT]):
    def __init__(
        self,
        *,
        definition: PromptGraderDefinition[ResponseT],
        dependencies: PromptGraderDependencies,
    ) -> None:
        self._definition = definition
        self._dependencies = dependencies

    async def grade(
        self,
        *,
        record: Mapping[str, Any],
        artifact: Mapping[str, Any],
    ) -> Grade:
        try:
            variables = self._definition.build_variables(
                record=record,
                artifact=artifact,
            )
            prompt = self._dependencies.renderer.render(
                self._definition.prompt_template,
                variables,
            )

            async def invoke() -> ResponseT:
                return await self._dependencies.llm_client.complete_structured(
                    prompt=prompt,
                    response_model=self._definition.response_model,
                )

            if self._dependencies.retry_policy is None:
                result = await invoke()
            else:
                result = await self._dependencies.retry_policy.run(invoke)

            grade = self._definition.to_grade(result)

            if self._dependencies.telemetry is not None:
                self._dependencies.telemetry.record_success(
                    criterion=self._definition.criterion,
                    version=self._definition.version,
                )

            return grade
        except Exception as exc:
            if self._dependencies.telemetry is not None:
                self._dependencies.telemetry.record_error(
                    criterion=self._definition.criterion,
                    version=self._definition.version,
                    error=exc,
                )

            return Grade(
                criterion=self._definition.criterion,
                score=None,
                label="grader_error",
                rationale=str(exc),
                evidence={},
                status="grader_error",
                grader_version=self._definition.version,
            )
