# Grader Design

## Purpose

Choose and document the simplest reliable grader design that measures one
approved criterion using a dataset record and execution artifact.

The output of this stage is a design document, not implementation code.

## Grader contract

Conceptually, a grader consumes:

```text
dataset record
+ execution artifact
+ grader configuration
```

and returns a structured grade containing:

- criterion ID;
- status;
- primary score or label;
- supporting metrics;
- rationale;
- evidence;
- grader version.

Recommended statuses:

- `scored`;
- `not_applicable`;
- `invalid_record`;
- `invalid_artifact`;
- `grader_error`.

Do not represent invalid data or grader failure as a quality score of zero.

## Grader families

### Code-based

Use when expected behavior and comparison logic can be represented explicitly.

Common patterns:

#### Predicate

Evaluate a boolean behavioral condition.

Examples:

- selected action is one of the valid actions;
- forbidden action was not taken;
- required refusal occurred.

#### Exact or normalized comparison

Compare normalized values, classifications, or structured outputs.

#### Set comparison

Measure precision, recall, F-score, required-item coverage, or forbidden-item
presence.

#### Ranking

Measure recall at K, reciprocal rank, nDCG, or another documented ranking
metric.

#### Numeric distance

Compare numeric values with an explicit tolerance and interpretation.

#### Information-unit coverage

Compare extracted units against required units and optional alternatives.

#### Trajectory comparison

Evaluate ordered or partially ordered decisions, tool calls, state transitions,
or stopping behavior.

Use code-based grading when it directly represents the criterion; do not force
semantic quality into brittle string matching.

### LLM-based

Use when quality requires semantic judgment and deterministic labels are
insufficient.

Common patterns:

#### Rubric judge

Score one output against a narrow criterion-specific rubric.

The rubric should define:

- the exact question;
- score or label meanings;
- evidence requirements;
- treatment of irrelevant style differences;
- handling of uncertainty;
- prohibited consideration of out-of-scope qualities.

#### Semantic reference comparison

Compare the output with reference facts, acceptable answers, or required
information without requiring surface-form equality.

#### Pairwise comparison

Compare candidate and baseline outputs for one criterion, including an explicit
tie option and order-bias controls.

#### Grounding or claim support

Identify claims and determine whether each is supported by provided evidence.

Avoid a single judge prompt that grades correctness, relevance, style, safety,
and completeness together unless the approved criterion itself legitimately
combines them.

### Hybrid

Use when deterministic processing improves the reliability or efficiency of a
semantic judgment.

Common patterns:

#### Extract then judge

Code extracts claims, actions, entities, or information units; an LLM judges
semantic properties; code aggregates results.

#### Validate then judge

Code verifies structure and identifies the content to evaluate; an LLM grades
only the semantic part.

#### Judge then enforce

An LLM produces structured subjudgments; code validates the schema and computes
the final metric.

Do not call a design hybrid merely because the LLM returns JSON.

## Required design decisions

### Inputs

Document exact paths read from:

- `record.input`;
- `record.expected`;
- execution artifact;
- grader configuration.

### Execution-artifact requirements

List observable fields required from the runner. Avoid depending on hidden
chain-of-thought or unavailable internal model reasoning.

Prefer observable:

- outputs;
- selected actions;
- tool calls and arguments;
- retrieved IDs and order;
- trace events;
- errors;
- source references;
- configuration identifiers.

### Score calculation

Define record-level computation and supporting values. For model judges, define
how judge labels map to metrics.

### Rationale

Require a concise explanation tied only to the criterion.

### Evidence

Require structured evidence useful for debugging, such as:

- missing required items;
- unsupported claims;
- chosen versus expected actions;
- relevant source IDs;
- rubric dimensions and sublabels.

### Error handling

Distinguish:

- malformed dataset record;
- missing runner evidence;
- judge failure or timeout;
- component execution failure;
- legitimate low-quality behavior.

### Not applicable

Define explicit conditions. Do not let the grader use `not_applicable` as an
escape from uncertain scoring.

### Versioning

Version changes to:

- grader logic;
- normalization;
- metric formula;
- model and configuration;
- prompt or rubric;
- aggregation mapping.

### Calibration and validation

For code-based graders, require fixed record/artifact examples covering:

- success;
- partial success;
- failure;
- invalid record;
- invalid artifact;
- not applicable.

For LLM-based graders, require a human-reviewed calibration set that includes
borderline examples. Document agreement expectations, instability checks, and
known bias risks.

## Selection guidance

Choose the simplest reliable design:

1. Use direct code when expected behavior is explicit.
2. Use semantic decomposition plus code when a complex output can be reduced to
   stable units.
3. Use a narrow LLM judge when semantic judgment remains necessary.
4. Use hybrid design when deterministic stages improve judge reliability.

The criterion group does not determine the grader family:

```text
basic ≠ always code-based
quality ≠ always LLM-based
```

## Prohibited grader behavior

A grader must not:

- execute the component;
- mutate records or artifacts;
- make release decisions;
- measure unrelated criteria;
- use undocumented fields;
- inspect hidden chain-of-thought;
- return zero for infrastructure errors;
- omit evidence for low or ambiguous scores;
- silently change metric semantics across versions.
