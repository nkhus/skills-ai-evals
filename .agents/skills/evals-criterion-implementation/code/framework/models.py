from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class TestCase(BaseModel):
    id: str
    input: dict[str, Any]
    expected: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExecutionArtifact(BaseModel):
    output: dict[str, Any] | None = None
    trace: dict[str, Any] | None = None
    errors: list[Any] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


GradeStatus = Literal[
    "scored",
    "not_applicable",
    "error",
]


class Grade(BaseModel):
    status: GradeStatus
    label: str | None = None
    value: float | None = None
    reasoning: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_grade(self) -> "Grade":
        if self.status == "scored":
            if self.label is None and self.value is None:
                raise ValueError("A scored grade must contain label or value.")
        elif self.label is not None or self.value is not None:
            raise ValueError("Non-scored grades must not contain label or value.")
        return self


MetricStatus = Literal[
    "computed",
    "insufficient_data",
    "metric_error",
]


class MetricResult(BaseModel):
    status: MetricStatus
    value: float | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ExecutionRecord(BaseModel):
    execution_id: str
    case_id: str
    artifact: ExecutionArtifact


class GradeRecord(BaseModel):
    execution_id: str
    case_id: str
    grade: Grade
