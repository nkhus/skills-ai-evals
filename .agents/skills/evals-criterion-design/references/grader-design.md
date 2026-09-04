# Grader Design Guide

A grader evaluates one execution of one test case against one criterion and produces a case-level result.

```text
grader = one criterion × one case × one execution
```

A grader does not aggregate across cases or executions.

## Contract

Define:

```text
type
judgment
inputs
applicability
outputs
```

The grader must evaluate only the approved criterion intent and boundary.

## Type

Use:

```text
code
llm
```

### Code

Use when the judgment can be derived reliably from explicit values with deterministic logic.

Examples:

```text
selected_tool ∈ acceptable_tools
actual == expected
expected_items ⊆ returned_items
distance(actual, expected) <= tolerance
```

Prefer code when semantic interpretation is unnecessary.

### LLM

Use when the judgment inherently requires semantic interpretation, such as relevance, groundedness, adequacy, or appropriateness under ambiguity.

The LLM should make one focused judgment for one criterion.

Deterministic preparation, parsing, validation, mapping, or post-processing does not create another grader type. If the substantive judgment is made by an LLM, the type is `llm`.

## Judgment

Express one focused question about component behavior.

Examples:

```text
Did the component select an acceptable tool?
Are the retrieved items relevant to the request?
Is the answer supported by the provided evidence?
```

Avoid broad judgments such as `Is this a good response?`.

### Atomicity

An LLM grader should evaluate one atomic behavioral dimension.

```text
atomic criterion
    ↓
focused judgment
    ↓
one strong judge prompt
    ↓
one structured LLM call
    ↓
Grade
```

If a grader must independently judge several meaningful qualities, this is normally evidence that the criterion is not atomic enough. Prefer fixing the criterion boundary rather than compensating with a complex grader.

### LLM-as-a-judge simplicity

An LLM grader should normally use one focused prompt, one structured response model, and one LLM call, producing one `Grade`.

Do not create by default multi-step judge workflows.

Such complexity is allowed only when the approved criterion fundamentally cannot be evaluated reliably with one focused judgment.

Deterministic input preparation, parsing, schema validation, label-to-value mapping, and post-processing do not make the grader multi-stage and do not create another grader type.

## Inputs

Define the minimum information required by the grader.

### Fixed context

Criterion-level information shared across cases:

- intent and boundary;
- judgment rules;
- output semantics.

### Test-case inputs

Reference information required from the case, such as:

- expected values;
- acceptable alternatives;
- reference facts;
- required or forbidden elements;
- valid ranges or tolerances.

These requirements define what the dataset must provide under `expected`.

### Execution inputs

Observable execution evidence required for grading, such as:

```text
selected_tool
tool_arguments
final_output
retrieved_items
dependency_result
subsequent_action
```

Require only evidence needed for the criterion. Never require hidden chain-of-thought or internal reasoning.

If required evidence is unavailable, record an observability requirement rather than inventing a proxy.

## Applicability

Define when the criterion can be validly graded.

Use `not_applicable` when a valid test case does not exercise the criterion.

Applicability follows from the case and criterion semantics, not from whether the component performed well.

## Outputs

Separate grading status from the quality representation:

```yaml
status: scored
label: relevant   # optional
value: 1.0        # optional
details: {}       # optional
```

For `status: scored`, at least one of `label` or `value` must be present.

Statuses:

```text
scored
not_applicable
error
```

- `scored` — valid quality result produced;
- `not_applicable` — criterion does not apply to this case;
- `error` — the case could not be scored (invalid case/reference data, missing required execution evidence, or a grading mechanism failure). Use `details` to record which of these applies.

For non-scored statuses, omit `label` and `value` unless a repository-wide contract explicitly requires otherwise.

Do not convert non-scored statuses into failure grades.

A component failure may still be graded when that failure is observable behavior relevant to the criterion.

## Code grader outputs

Use the simplest representation naturally produced by the deterministic judgment.

Examples:

```text
value: 0 | 1
label: valid | invalid
value: 0.0 .. 1.0   # only when mathematically meaningful
```

Do not introduce arbitrary numeric scales for downstream convenience.

## LLM grader outputs

Prefer semantic labels over asking the LLM for numeric scores.

Example:

```text
relevant
partially_relevant
irrelevant
```

Each label must have distinct semantics. Keep the set as small as possible.

When numeric aggregation is meaningful, define a deterministic mapping in the grader contract:

```text
relevant           → 1.0
partially_relevant → 0.5
irrelevant         → 0.0
```

The LLM assigns the label. Deterministic grader logic emits the mapped `value`.

Define a mapping only when the ordering and distances between labels are defensible. Otherwise emit labels only and let metrics aggregate them directly.

## Details

Optional `details` should make the result inspectable, for example:

- expected vs observed values;
- matched or missing items;
- violated constraints;
- concise evidence supporting an LLM label.

Do not require hidden reasoning.

## Legitimate alternatives

Represent all legitimate correct behaviors explicitly. Do not compare against one canonical answer when the component contract allows meaningful variability.

## Multiple graders

Prefer one grader per criterion.

Use multiple graders only when they provide complementary case-level outputs about the same behavioral dimension. If they independently assess different qualities, those qualities should normally be separate criteria.

## Grader specification template

```yaml
type: llm # code | llm

judgment: >
  One focused question about the component behavior.

inputs:
  expected: []
  execution: []

applicability: >
  When this criterion can be validly graded.

outputs:
  labels: {}   # optional
  values: null # define range/meaning when the grader emits value
  label_to_value: {} # optional; grader-owned deterministic mapping

non_scored_statuses:
  - not_applicable
  - error

details: []
```

Omit irrelevant fields.

## Implementation handoff

Grader design is complete when implementation does not need to decide:

- grader type;
- case-level judgment;
- required case and execution inputs;
- applicability;
- statuses;
- label/value semantics;
- deterministic label-to-value mapping when relevant;
- behavior outside the judgment.

Do not define dataset-level aggregation, repeated-execution aggregation, release thresholds, or execution policy here.
