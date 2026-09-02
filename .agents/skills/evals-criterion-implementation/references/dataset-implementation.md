# Dataset implementation

## Source of truth

Implement only the dataset groups and record fields approved in:

```text
evals/components/{component}/datasets/{criterion_id}/README.md
```

## Record shape

Each JSONL line must contain exactly:

```json
{
  "id": "criterion-group-001",
  "input": {},
  "expected": {}
}
```

`input` contains everything the future component runner needs to execute the example.

`expected` contains only the information the grader needs to evaluate the resulting artifact.

The runner must not use `expected` to influence execution.

## Dataset groups

Create only approved groups. Common groups are:

- `baseline.jsonl` — representative normal behavior;
- `corner_cases.jsonl` — difficult but valid behavior;
- `regression.jsonl` — known or plausible failures that must not recur.

Do not create empty groups solely to match a generic layout.

## Record quality

Each record must:

- exercise the criterion directly;
- have a stable unique ID across every group of the criterion;
- contain verifiable expectations;
- represent a meaningful scenario rather than a placeholder;
- avoid depending on hidden conversation context;
- be executable independently;
- avoid fields not defined by the approved dataset contract.

## Expected values

Do not invent facts, labels, or reference answers that cannot be established from repository evidence or user-approved domain knowledge.

When expected values require unavailable domain review, create no fabricated record. Ask for the missing source or leave the implementation blocked.

## Coverage

Implement the scenario categories required by the dataset design, including as applicable:

- straightforward success;
- clear failure;
- partial success;
- ambiguity;
- missing or conflicting information;
- boundary values;
- accepted variability;
- previously observed regressions.

## Validation

Validate before completion:

- every line is valid JSON;
- every record has only `id`, `input`, and `expected` at the top level;
- IDs are non-empty and unique across groups;
- input and expected fields match the documented contract;
- no record is an unresolved placeholder;
- referenced identifiers exist where repository-local validation is possible.
