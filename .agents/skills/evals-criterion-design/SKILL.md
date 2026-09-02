---
name: evals-criterion-design
description: Detail one approved component evaluation criterion into a complete semantic, metric, dataset, grader, and execution-artifact design. Use after criteria discovery and before implementation.
user-invocable: false
---

# Evals Criterion Design

## Objective

Turn one approved high-level criterion into an implementation-ready design.

One invocation handles exactly one criterion.

This stage answers:

- what the criterion precisely means;
- what behavior is good, bad, acceptable, or not applicable;
- how the behavior is measured;
- which metrics and diagnostics are produced;
- which examples and fields the criterion-owned datasets require;
- which grader design pattern should be implemented;
- which execution-artifact fields the component runner must provide.

This stage does not implement datasets, graders, runners, manifests, suites, or
policies.

## Invocation

The orchestrator provides:

- component name;
- criterion ID.

Example:

```text
Component: retriever
Criterion: retrieval_coverage
```

Do not require the orchestrator to pass summaries, decisions, or artifact
contents. Read previous-stage artifacts directly.

## Required inputs

Before starting, read:

- `evals/config.yaml`;
- `evals/components/{component}/README.md`;
- `evals/components/{component}/spec/criteria.yaml`.

Find the requested criterion in `spec/criteria.yaml` and use its approved:

- `id`;
- `name`;
- `group`;
- `priority`;
- `intent`;
- optional `out_of_scope`.

If a required file is missing, or the criterion ID is not present, stop and
report the blocking path or identifier. Do not create or repair prerequisite
artifacts.

## Context boundary

Read deeply:

- the approved component README;
- the requested criterion entry;
- repository code and documentation needed to understand this criterion;
- an existing draft or final design for this same criterion.

Do not read detailed designs of other criteria by default. You may inspect their
IDs, names, intents, and brief boundaries only to avoid obvious overlap.

Do not redesign the component or the complete criterion list.

## Working artifact

While the criterion is being discussed, maintain:

- `evals/components/{component}/criterion-design.{criterion_id}.draft.md`

The draft records the current integrated proposal and unresolved decisions. Its
existence does not complete the stage.

Use `templates/criterion-design-draft.md`.

## Required process

### 1. Confirm the criterion identity

Read the approved criterion entry and restate succinctly:

- what behavior it appears to evaluate;
- why that behavior matters to the component's functional goal;
- the most important boundary with adjacent behavior.

Ask a focused question only when the approved intent leaves a material ambiguity
that repository evidence cannot resolve.

If the criterion is fundamentally invalid, duplicated, or outside the approved
component boundary, stop and recommend returning to `evals-criteria-discovery`.
Do not silently redefine the criterion into something different.

### 2. Define the semantic contract

Specify:

- purpose;
- evaluation question;
- component responsibility;
- desired behavior;
- undesired behavior;
- acceptable variability;
- out-of-scope behavior;
- applicability and not-applicable cases;
- common and high-consequence failure modes;
- meaningful edge cases;
- relationship to the component's functional goal.

Follow `references/criterion-detailing.md`.

The criterion must remain one coherent quality dimension. If the design needs
several unrelated questions or scores, propose splitting it and return to
criteria discovery rather than hiding several criteria in one specification.

### 3. Design measurement and metrics

Separate:

- criterion — the quality dimension;
- primary metric — the main measurement used to represent the criterion;
- supporting metrics — secondary measurements that explain the main result;
- diagnostics — debugging information that is not itself a quality measure.

For every metric define:

- record-level value;
- range or value set;
- direction of improvement;
- dataset-level aggregation;
- interpretation;
- handling of invalid and not-applicable records;
- limitations and dependence on dataset composition.

Do not define release thresholds or policy decisions.

Follow `references/metric-design.md`.

### 4. Design criterion-owned datasets

Define the dataset contract for this criterion only.

Every future executable record must have exactly this top-level envelope:

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

Define:

- exact fields and semantics under `input`;
- exact fields and semantics under `expected`;
- required and optional fields;
- dataset groups that are actually needed;
- scenario categories each group must cover;
- positive, negative, difficult, and regression examples;
- balance and coverage considerations;
- invalid-record examples;
- maintenance rules.

Prefer the standard dataset groups when applicable:

- `baseline`;
- `corner_cases`;
- `regression`.

Do not create JSONL files in this stage.

The runner must be able to execute using `input` without reading `expected`.

Follow `references/dataset-design.md`.

### 5. Design the grader

Choose the grader family only after the semantic, metric, and dataset contracts
are clear:

- `code_based`;
- `llm_based`;
- `hybrid`.

Document:

- design pattern;
- inputs from the dataset record;
- required execution-artifact fields;
- configuration;
- record-level score calculation;
- labels, rationale, and evidence;
- error statuses;
- not-applicable behavior;
- determinism and variability;
- calibration or test-fixture requirements;
- versioning;
- known limitations.

Prefer the simplest reliable grader capable of measuring the approved
criterion. Do not choose a grader family from the criterion's Basic or Quality
group alone.

Follow `references/grader-design.md`.

### 6. Define runner artifact requirements

List only the observable fields the future component runner must persist for
this grader, for example:

- normalized output;
- selected route or tool;
- retrieved item IDs and order;
- tool-call arguments;
- relevant trace events;
- component errors;
- configuration or version identifiers needed for interpretation.

Do not design or implement the runner itself.

Do not request fields that cannot reasonably be observed. Record missing
observability as an implementation prerequisite or grader limitation.

### 7. Present one integrated design

Present the complete current proposal together:

- semantic contract;
- metrics;
- dataset contract and groups;
- grader design;
- execution-artifact requirements;
- unresolved questions and limitations.

Do not ask the user to approve isolated fragments as though the entire design
were approved. Iterate as needed and keep the working draft current.

### 8. Obtain explicit approval

Ask the user to explicitly approve the complete design for this criterion.

Do not treat silence, approval of one section, or approval of an earlier draft
as final approval.

### 9. Write final artifacts

Only after explicit approval, rename drafts into final artifacts and write the completed content to:

- `evals/components/{component}/spec/{criterion_id}.md`;
- `evals/components/{component}/datasets/{criterion_id}/README.md`;
- `evals/components/{component}/graders/{criterion_id}.md`.

Use the templates in `templates/` and follow
`references/output-contract.md`.

Remove the working draft or clearly mark it superseded.

## Stage boundaries

Do not:

- add, remove, rename, merge, split, or reprioritize entries in
  `spec/criteria.yaml`;
- design more than one criterion in one invocation;
- create executable JSONL datasets;
- write grader implementation code;
- write component runner code;
- create or update the component manifest;
- update root configuration, suites, or policies;
- define release gates or thresholds;
- execute evaluations;
- repeat broad component analysis.

## Completion

The stage is complete only when the user explicitly approves the design and all
three final artifacts exist:

- `evals/components/{component}/spec/{criterion_id}.md`;
- `evals/components/{component}/datasets/{criterion_id}/README.md`;
- `evals/components/{component}/graders/{criterion_id}.md`.

Return the component, criterion ID, and created artifact paths. Do not start the
next pipeline stage.
