import uuid
from dataclasses import dataclass, field
from typing import Any, Callable

from .grading import Grader
from .inference import Executor
from .models import ExecutionRecord, GradeRecord, MetricResult, TestCase


async def infer(
    cases: list[TestCase],
    executor: Executor,
) -> list[ExecutionRecord]:
    records: list[ExecutionRecord] = []
    for case in cases:
        artifact = await executor.execute(case.input)
        records.append(
            ExecutionRecord(
                execution_id=str(uuid.uuid4()),
                source_id=case.id,
                input=case.input,
                artifact=artifact,
            )
        )
    return records


async def grade(
    records: list[ExecutionRecord],
    cases: dict[str, TestCase],
    grader: Grader,
) -> list[GradeRecord]:
    results: list[GradeRecord] = []
    for record in records:
        case = cases.get(record.source_id)
        if case is None:
            raise KeyError(f"No TestCase found for source_id={record.source_id!r}.")

        results.append(
            GradeRecord(
                execution_id=record.execution_id,
                source_id=record.source_id,
                grade=await grader.grade(case, record.artifact),
            )
        )
    return results


@dataclass(frozen=True)
class MetricSpec:
    name: str
    fn: Callable[..., MetricResult]
    needs_references: bool = False
    kwargs: dict[str, Any] = field(default_factory=dict)


def calculate_metrics(
    grades: list[GradeRecord],
    references: dict[str, TestCase],
    metrics: list[MetricSpec],
) -> dict[str, MetricResult]:
    results: dict[str, MetricResult] = {}
    for spec in metrics:
        if spec.needs_references:
            results[spec.name] = spec.fn(grades, references, **spec.kwargs)
        else:
            results[spec.name] = spec.fn(grades, **spec.kwargs)
    return results
