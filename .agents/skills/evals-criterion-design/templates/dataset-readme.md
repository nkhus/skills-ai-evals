# {Criterion Name} Datasets

- Component: `{component}`
- Criterion ID: `{criterion_id}`
- Criterion specification: `evals/components/{component}/spec/{criterion_id}.md`

## Purpose

{what_behavior_these_datasets_are_designed_to_measure}

## Record Contract

Every record contains only:

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

No generic top-level `tags`, `metadata`, `context`, or `annotations` are used.

## `id`

{identifier_format_uniqueness_and_stability_rules}

## `input`

Everything the component runner needs to execute the scenario.

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `{input_field}` | `{type}` | Yes | {meaning} |

### Input rules

{input_rules_and_relationships}

## `expected`

Everything the grader needs to evaluate the resulting execution artifact.

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `{expected_field}` | `{type}` | Yes | {meaning} |

### Expected rules

{expected_rules_and_relationships}

The component runner must not use `expected` during execution.

## Example Record

```json
{
  "id": "{example_id}",
  "input": {
    "{input_field}": "{example_value}"
  },
  "expected": {
    "{expected_field}": "{example_expected_value}"
  }
}
```

## Dataset Groups

### Baseline

{whether_baseline_is_required_and_what_it_covers}

Expected implementation path:

`evals/components/{component}/datasets/{criterion_id}/baseline.jsonl`

### Corner Cases

{whether_corner_cases_are_required_and_what_they_cover}

Expected implementation path:

`evals/components/{component}/datasets/{criterion_id}/corner_cases.jsonl`

### Regression

{whether_regression_is_required_and_how_records_are_added}

Expected implementation path:

`evals/components/{component}/datasets/{criterion_id}/regression.jsonl`

Remove sections for groups that are not part of the approved design.

## Required Scenario Categories

{scenario_categories_and_coverage_requirements}

## Positive and Negative Coverage

{positive_negative_no_action_partial_and_multiple_valid_output_cases}

## Difficult and Boundary Cases

{ambiguous_missing_conflicting_or_high_consequence_cases}

## Balance and Coverage

{dimensions_that_must_not_be_accidentally_dominated}

## Invalid Record Examples

{invalid_examples_and_why_they_are_invalid}

## Record Authoring Rules

{rules_for_creating_clear_non_leaking_records}

## Dataset Maintenance

{when_to_add_update_or_remove_records_and_how_to_preserve_ids}
