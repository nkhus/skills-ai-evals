# Metric Design Guide

Metrics are generic, reusable statistical aggregations over grader outputs. They do not carry criterion semantics.

```text
criterion-specific behavior
        ↓
grader
        ↓
Grade(label / value / status)
        ↓
generic metric
```

Criterion-specific semantics belong to the grader. The metric must not reinterpret component behavior.

## Prefer pre-implemented generic metrics

Select from the reusable framework metric set instead of designing custom aggregation formulas.

Initial shared set:

```text
mean
median
accuracy
precision
recall
f1
label_rate
status_rate
```

The set may later grow with other established generic metrics (for example macro/micro classification metrics, ROC-AUC, NDCG, MRR, MAP) when they become necessary.

If an approved criterion needs an established generic metric that is missing, identify the required generic semantics so it can be added to the shared framework metric package. Do not design a criterion-specific formula as a substitute.

Example mappings:

```text
tool selection semantics
→ grader emits correct / incorrect
→ accuracy
```

```text
semantic relevance
→ grader emits numeric relevance value
→ mean
```

```text
classification
→ grader emits predicted label
→ accuracy / precision / recall / f1
```

## Metric inputs

Standard conventions:

```text
numeric quality          → Grade.value
categorical prediction   → Grade.label
classification reference → TestCase.expected["label"]
classification prediction → Grade.label
```

For binary `precision`, `recall`, `f1`, the positive label must be explicit.

## Primary metric

Choose one primary generic metric that best represents criterion performance. Do not invent equivalent metrics unnecessarily.

## Supporting metrics

Add supporting metrics only when they materially improve interpretation, for example:

```text
status rate
label distribution
scored coverage
error rate
```

## Non-scored results

Quality metrics normally operate only on `Grade.status == "scored"`.

Never silently convert `not_applicable` or `error` into quality score `0`.

## Slices

A slice is the same generic metric applied to a subset of cases:

```text
accuracy
accuracy[ambiguous_request]
accuracy[multi_turn]
```

Do not define a separate metric merely because a slice exists.

## Keep metric design minimal

Specify only what downstream implementation cannot infer automatically.

```yaml
primary:
  metric: accuracy

supporting:
  - metric: status_rate
    status: error

slices:
  - ambiguous_request
```

or:

```yaml
primary:
  metric: mean
  source: grade.value
```

Do not restate standard mathematical definitions, ranges, or implementation details that are intrinsic to a known generic metric.

## Implementation handoff

Metric design is complete when downstream stages do not need to invent semantic evaluation choices:

- which generic metric(s) to use;
- the primary metric;
- supporting metrics, if any;
- treatment of non-scored statuses;
- important slices.

Metric design does not own grader semantics, dataset construction, execution grouping, release thresholds, acceptance policy, or execution configuration.
