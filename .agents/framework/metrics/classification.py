from dataclasses import dataclass

from ..models import GradeRecord, MetricResult, TestCase


@dataclass(frozen=True)
class _ConfusionCounts:
    total: int
    scored: int
    excluded: int
    tp: int
    fp: int
    tn: int
    fn: int


def _classification_pairs(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
) -> tuple[list[tuple[str, str]], MetricResult | None]:
    scored = [record for record in grades if record.grade.status == "scored"]
    if not scored:
        return [], MetricResult(
            status="insufficient_data",
            details={"total": len(grades), "scored": 0, "excluded": len(grades)},
        )

    pairs: list[tuple[str, str]] = []
    errors: list[dict[str, str]] = []

    for record in scored:
        predicted = record.grade.label
        if predicted is None:
            errors.append(
                {
                    "execution_id": record.execution_id,
                    "source_id": record.source_id,
                    "error": "Scored grade is missing label.",
                }
            )
            continue

        case = cases.get(record.source_id)
        if case is None:
            errors.append(
                {
                    "execution_id": record.execution_id,
                    "source_id": record.source_id,
                    "error": "TestCase not found.",
                }
            )
            continue

        reference = case.expected.get("label")
        if not isinstance(reference, str):
            errors.append(
                {
                    "execution_id": record.execution_id,
                    "source_id": record.source_id,
                    "error": 'TestCase.expected["label"] must be a string.',
                }
            )
            continue

        pairs.append((reference, predicted))

    if errors:
        return [], MetricResult(
            status="metric_error",
            details={"error": "Invalid classification metric input.", "records": errors},
        )

    return pairs, None


def accuracy(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
) -> MetricResult:
    pairs, error = _classification_pairs(grades, cases)
    if error is not None:
        return error

    correct = sum(reference == predicted for reference, predicted in pairs)
    return MetricResult(
        status="computed",
        value=correct / len(pairs),
        details={
            "correct": correct,
            "incorrect": len(pairs) - correct,
            "total": len(grades),
            "scored": len(pairs),
            "excluded": len(grades) - len(pairs),
        },
    )


def _confusion_counts(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
    *,
    positive_label: str,
) -> tuple[_ConfusionCounts | None, MetricResult | None]:
    pairs, error = _classification_pairs(grades, cases)
    if error is not None:
        return None, error

    tp = fp = tn = fn = 0
    for reference, predicted in pairs:
        reference_positive = reference == positive_label
        predicted_positive = predicted == positive_label

        if reference_positive and predicted_positive:
            tp += 1
        elif not reference_positive and predicted_positive:
            fp += 1
        elif not reference_positive and not predicted_positive:
            tn += 1
        else:
            fn += 1

    return (
        _ConfusionCounts(
            total=len(grades),
            scored=len(pairs),
            excluded=len(grades) - len(pairs),
            tp=tp,
            fp=fp,
            tn=tn,
            fn=fn,
        ),
        None,
    )


def _details(counts: _ConfusionCounts, positive_label: str) -> dict[str, int | str]:
    return {
        "positive_label": positive_label,
        "total": counts.total,
        "scored": counts.scored,
        "excluded": counts.excluded,
        "tp": counts.tp,
        "fp": counts.fp,
        "tn": counts.tn,
        "fn": counts.fn,
    }


def precision(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
    *,
    positive_label: str,
) -> MetricResult:
    counts, error = _confusion_counts(grades, cases, positive_label=positive_label)
    if error is not None:
        return error
    assert counts is not None

    denominator = counts.tp + counts.fp
    if denominator == 0:
        return MetricResult(
            status="insufficient_data",
            details={
                **_details(counts, positive_label),
                "reason": "No predicted positive observations.",
            },
        )

    return MetricResult(
        status="computed",
        value=counts.tp / denominator,
        details=_details(counts, positive_label),
    )


def recall(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
    *,
    positive_label: str,
) -> MetricResult:
    counts, error = _confusion_counts(grades, cases, positive_label=positive_label)
    if error is not None:
        return error
    assert counts is not None

    denominator = counts.tp + counts.fn
    if denominator == 0:
        return MetricResult(
            status="insufficient_data",
            details={
                **_details(counts, positive_label),
                "reason": "No reference positive observations.",
            },
        )

    return MetricResult(
        status="computed",
        value=counts.tp / denominator,
        details=_details(counts, positive_label),
    )


def f1(
    grades: list[GradeRecord],
    cases: dict[str, TestCase],
    *,
    positive_label: str,
) -> MetricResult:
    counts, error = _confusion_counts(grades, cases, positive_label=positive_label)
    if error is not None:
        return error
    assert counts is not None

    denominator = (2 * counts.tp) + counts.fp + counts.fn
    if denominator == 0:
        return MetricResult(
            status="insufficient_data",
            details={
                **_details(counts, positive_label),
                "reason": "No positive reference or predicted observations.",
            },
        )

    return MetricResult(
        status="computed",
        value=(2 * counts.tp) / denominator,
        details=_details(counts, positive_label),
    )
