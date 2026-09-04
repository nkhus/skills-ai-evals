from statistics import median as _median

from ..models import GradeRecord, GradeStatus, MetricResult


def mean(grades: list[GradeRecord]) -> MetricResult:
    scored = [record for record in grades if record.grade.status == "scored"]
    if not scored:
        return MetricResult(
            status="insufficient_data",
            details={"total": len(grades), "scored": 0, "excluded": len(grades)},
        )

    missing = [record.execution_id for record in scored if record.grade.value is None]
    if missing:
        return MetricResult(
            status="metric_error",
            details={
                "error": "Scored grades are missing value.",
                "execution_ids": missing,
            },
        )

    values = [record.grade.value for record in scored]
    assert all(value is not None for value in values)
    numeric_values = [float(value) for value in values]

    return MetricResult(
        status="computed",
        value=sum(numeric_values) / len(numeric_values),
        details={
            "total": len(grades),
            "scored": len(scored),
            "excluded": len(grades) - len(scored),
        },
    )


def median(grades: list[GradeRecord]) -> MetricResult:
    scored = [record for record in grades if record.grade.status == "scored"]
    if not scored:
        return MetricResult(
            status="insufficient_data",
            details={"total": len(grades), "scored": 0, "excluded": len(grades)},
        )

    missing = [record.execution_id for record in scored if record.grade.value is None]
    if missing:
        return MetricResult(
            status="metric_error",
            details={
                "error": "Scored grades are missing value.",
                "execution_ids": missing,
            },
        )

    values = [record.grade.value for record in scored]
    assert all(value is not None for value in values)
    numeric_values = [float(value) for value in values]

    return MetricResult(
        status="computed",
        value=float(_median(numeric_values)),
        details={
            "total": len(grades),
            "scored": len(scored),
            "excluded": len(grades) - len(scored),
        },
    )


def label_rate(
    grades: list[GradeRecord],
    *,
    label: str,
) -> MetricResult:
    scored = [record for record in grades if record.grade.status == "scored"]
    if not scored:
        return MetricResult(
            status="insufficient_data",
            details={"total": len(grades), "scored": 0, "excluded": len(grades)},
        )

    missing = [record.execution_id for record in scored if record.grade.label is None]
    if missing:
        return MetricResult(
            status="metric_error",
            details={
                "error": "Scored grades are missing label.",
                "execution_ids": missing,
            },
        )

    matches = sum(record.grade.label == label for record in scored)
    return MetricResult(
        status="computed",
        value=matches / len(scored),
        details={
            "label": label,
            "matches": matches,
            "total": len(grades),
            "scored": len(scored),
            "excluded": len(grades) - len(scored),
        },
    )


def status_rate(
    grades: list[GradeRecord],
    *,
    status: GradeStatus,
) -> MetricResult:
    if not grades:
        return MetricResult(status="insufficient_data", details={"total": 0})

    matches = sum(record.grade.status == status for record in grades)
    return MetricResult(
        status="computed",
        value=matches / len(grades),
        details={"status": status, "matches": matches, "total": len(grades)},
    )
