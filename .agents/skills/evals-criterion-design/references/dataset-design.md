# Dataset Design

## Purpose

Define the complete authoring contract for the datasets owned by one criterion.
The implementation stage will later create the executable JSONL files.

## Criterion-owned datasets

Each criterion owns its own dataset directory:

```text
evals/components/{component}/datasets/{criterion_id}/
```

Do not introduce a shared case bank or an annotation join.

Some scenario duplication across criteria is acceptable because each dataset
represents a different measurement contract.

## Universal record envelope

Every executable record contains only:

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

Do not add generic top-level `tags`, `metadata`, `context`, or `annotations`.

### `id`

A stable, unique identifier used for reporting, caching, comparison, and
regression tracking.

IDs should:

- remain stable when wording changes but the scenario meaning does not;
- be unique within the criterion's datasets;
- use a readable consistent convention;
- not encode mutable array positions.

### `input`

Everything the component runner needs to execute the scenario.

Place criterion-specific execution context inside `input`, for example:

- request or messages;
- available tools;
- retrieved context supplied to the component;
- configuration flags;
- user or permission context;
- prior state needed for invocation.

The runner should not need `expected` to execute the component.

### `expected`

Everything the grader needs to evaluate the execution artifact.

Examples:

- expected class or route;
- required and forbidden items;
- reference facts;
- relevance judgments;
- rubric-specific required information;
- valid action alternatives;
- source-support mappings.

Do not store grader implementation instructions inside individual records when
they belong in the criterion or grader contract.

## Define field schemas semantically

For every field define:

- path;
- type;
- required or optional status;
- semantic meaning;
- valid values;
- relationship to other fields;
- behavior when omitted;
- one concise example.

Avoid unconstrained generic dictionaries when the implementation can use a
clearer contract.

## Dataset groups

Use only groups that add a distinct maintenance purpose.

### Baseline

Representative normal behavior and the main functional distribution.

A good baseline includes:

- common paths;
- meaningful variation;
- both successful and failure-sensitive scenarios;
- enough diversity to avoid measuring one narrow pattern.

### Corner cases

Difficult, ambiguous, boundary, adversarial, rare, or structurally unusual
valid scenarios.

Corner cases should exercise the criterion, not random malformed data that only
tests parser resilience.

### Regression

Scenarios created from known failures. Each record should preserve the exact
behavior that must not recur.

Regression datasets should grow from production incidents, user complaints,
review findings, and previously observed model regressions.

## Scenario design

Define the categories the implementation stage must cover, including where
relevant:

- positive success cases;
- negative or no-action cases;
- partial-success cases;
- multiple-valid-answer cases;
- ambiguous cases;
- missing-information cases;
- conflicting-information cases;
- boundary cases;
- high-consequence cases;
- known regressions.

## Balance and coverage

Specify dimensions that should not be accidentally dominated, such as:

- intent category;
- difficulty;
- input length;
- number of available options;
- answerable versus unanswerable;
- action versus no action;
- single-turn versus multi-turn;
- domain category;
- language, when relevant.

The dataset README may describe these dimensions without adding generic metadata
to every record. Encode only execution- or grading-relevant data in records.

## Invalid records

Document examples that should fail dataset validation, such as:

- missing `id`, `input`, or `expected`;
- duplicate IDs;
- expected references to unavailable entities;
- incompatible alternatives;
- expected values that cannot be observed by the grader;
- fields whose meaning conflicts with the criterion spec.

Invalid data is not component failure.

## Leakage prevention

Expected answers must not influence execution.

The future runner should receive only `input`. The grader receives the full
record and execution artifact.

Avoid input fields whose names or values reveal the expected answer unless that
information is genuinely available to the real component.

## Maintenance contract

Define when records are added, revised, or removed:

- add a regression record for meaningful confirmed failures;
- update records when underlying domain truth changes;
- preserve stable IDs where scenario identity is unchanged;
- review expected values when component boundaries change;
- avoid deleting hard examples merely because they reduce scores.
