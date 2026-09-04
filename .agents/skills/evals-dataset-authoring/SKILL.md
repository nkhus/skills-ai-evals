---
name: evals-dataset-authoring
description: Create and validate the concrete evaluation dataset for one approved criterion without changing its evaluation semantics.
user-invocable: false
---

# Evals Dataset Authoring

## Purpose

Turn the approved dataset design for one criterion into concrete `TestCase` records.

Dataset authoring decides how to realize the approved dataset contract, but must not invent evaluation semantics or unsupported ground truth.

## Input

```text
Component: {component}
Criterion: {criterion_id}
```

## Requires

```text
evals/components/{component}/spec/{criterion_id}.md
```

Require the criterion specification `Status: Approved`.

Use its `Dataset` section as the source of truth for:

* `input` semantics;
* `expected` semantics;
* required coverage;
* ground-truth rules;
* criterion-specific authoring constraints;
* optional analysis dimensions.

## Output

Create:

```text
evals/components/{component}/datasets/{criterion_id}/
├── dataset.yaml
└── cases.jsonl
```

### `dataset.yaml`

```yaml
name: tool-selection-eval
language: en
description: Evaluation cases for tool selection behavior.
```

Rules:

* `name` is required and human-facing;
* `language` is optional;
* `description` is optional;
* do not introduce a dataset ID or other metadata without a concrete need.

### `cases.jsonl`

One `TestCase` per line:

```json
{
  "id": "ambiguous-request-001",
  "input": {},
  "expected": {},
  "metadata": {}
}
```

`metadata` is optional.

Semantics:

```text
id       -> stable case identity within the dataset
input    -> real component input
expected -> reference information used for grading / metrics
metadata -> optional analysis / maintenance information
```

Keep this separation:

```text
input    -> component execution
expected -> evaluation reference
metadata -> analysis / maintenance
```

## Workflow

1. Read the approved criterion specification and extract the dataset contract, required coverage, ground-truth rules, and authoring guidance.

2. Inspect repository sources when useful for constructing realistic inputs or establishing authoritative facts. Do not treat current component behavior as ground truth merely because it is implemented.

3. Ask the user whether they already have examples, source inputs, scenarios, known failures, domain constraints, desired emphasis, or a desired dataset size.

   If the user has material, incorporate it into the dataset plan.

   If not, derive the plan from the approved criterion design.

4. Propose a compact dataset composition before generating cases. Include only what is useful, normally:

   * dataset name and language when applicable;
   * approximate case count;
   * user-provided vs generated material;
   * realization of required coverage;
   * important variation or emphasis.

5. Ask the user to approve the proposed dataset composition.

6. After approval, write the complete `dataset.yaml` and `cases.jsonl`.

7. Check obvious structural problems:

   * valid YAML / JSONL;
   * every case has `id`, `input`, and `expected`;
   * `input` and `expected` are objects;
   * `metadata`, when present, is an object;
   * case IDs are unique;
   * no unresolved placeholders or TODO values remain.

8. Present the generated dataset to the user and ask them to review and validate it.

9. Apply requested corrections. The stage is complete after explicit user approval of the dataset.

## Authoring Rules

### Case IDs

Case IDs must be:

* unique within `cases.jsonl`;
* stable while the conceptual scenario remains the same;
* changed when the scenario or its ground truth changes materially;
* preferably short and human-readable.

Do not use UUIDs or hashes without a concrete need.

### Case generation

Cases may be:

* based on user-provided examples;
* expert-authored;
* repository-derived;
* production-derived;
* synthetic / LLM-generated;
* based on confirmed historical failures.

Synthetic generation is allowed and encouraged when useful.

Generation may propose cases. It does not establish ground truth.

### Ground truth

Every required `expected` value must have a defensible basis, such as:

* the approved component or criterion contract;
* authoritative repository specifications or invariants;
* product requirements;
* authoritative domain information;
* explicit user or expert judgment;
* confirmed historical truth.

Do not invent expected values.

If required ground truth is unavailable, ask the user rather than guessing or silently removing the affected coverage.

`expected: {}` is valid when the approved grader genuinely requires no case-specific reference information.

### Coverage

Realize all required coverage from the approved criterion design.

Dataset authoring decides:

* concrete cases;
* case count;
* useful combinations and variations;
* how user-provided material is incorporated;
* how missing coverage is filled.

Do not add new evaluation dimensions or remove required ones.

There is no universal target dataset size or required balancing formula.

Avoid accidental overrepresentation and obvious duplicate or superficial paraphrase cases unless the variation meaningfully exercises different behavior.

### Metadata

Case-level metadata is optional.

Use it only when useful for analysis or maintenance, for example:

```json
{
  "scenario": "ambiguous_request",
  "tags": ["multi_turn"]
}
```

Do not require coverage categories to be encoded as metadata.

Do not put grader semantics or reference truth in metadata.

Dataset-wide properties such as a common language belong in `dataset.yaml` rather than being repeated on every case.

### Existing and regression cases

User-provided and existing cases may be reused or adapted when they satisfy the approved contract.

A confirmed historical failure may be represented as a normal `TestCase`.

Do not decide from evaluation results that a new failure should become a regression case; that belongs to future regression-maintenance work.

## Boundary

Do not:

* change the approved criterion or dataset semantics;
* change grader or metric semantics;
* invent ground truth;
* expose `expected` or analysis metadata to component execution;
* implement graders, metrics, component execution, runtime, or persistence;
* analyze evaluation results or define release policy;
* introduce dataset grouping or lifecycle architecture not required by the approved design.

No separate implementation handoff is required. The dataset files are the stage output.

## Completion

Complete only when:

```text
dataset.yaml exists
cases.jsonl exists
the dataset is structurally valid
the user explicitly approves the generated dataset
```
