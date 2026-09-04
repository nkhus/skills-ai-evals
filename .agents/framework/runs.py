from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from .models import ExecutionRecord, GradeRecord, MetricResult


def new_run_id() -> str:
    # timestamp-prefixed so filenames sort chronologically without reading contents
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    return f"{timestamp}-{uuid4().hex[:8]}"


class SourceRef(BaseModel):
    type: str
    path: str


class InferenceRun(BaseModel):
    run_id: str
    source: SourceRef
    config: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    records: list[ExecutionRecord]


class GradingRun(BaseModel):
    run_id: str
    inference_run_id: str
    grader: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    records: list[GradeRecord]


class MetricRun(BaseModel):
    run_id: str
    grading_run_id: str
    metric: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    results: dict[str, MetricResult]
