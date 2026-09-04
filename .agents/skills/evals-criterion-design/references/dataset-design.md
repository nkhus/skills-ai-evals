# Dataset Design Guide

Design the dataset contract and authoring guidance for one criterion. Do not create concrete test cases.

## Contract

Use:

```yaml
id: case-id
input: {}
expected: {}
metadata: {} # optional
```

Ownership model:

```text
component contract        → input
grader + metric contracts → expected
analysis / maintenance    → metadata
```

A more general interpretation:

```text
input
→ information the real component receives

expected
→ reference truth required to evaluate the case

metadata
→ analysis / maintenance information
```

Every field should have a clear consumer.

## Input

`input` must match the real component invocation.

Include only information the component actually receives, such as:

- request;
- conversation history;
- state;
- context;
- available tools/actions;
- upstream outputs.

For stateful or multi-turn components, include required history/state directly in `input`.

Do not add evaluation-only fields, expected answers, grader labels, or grader instructions.

## Expected

`expected` contains reference truth required to evaluate the case. It may be consumed:

- directly by the grader;
- by generic metrics requiring standardized reference truth, for example `TestCase.expected["label"]` as the reference class for classification metrics.

It may define:

- expected values;
- acceptable alternatives;
- required or forbidden elements;
- reference facts;
- ranges or tolerances;
- hints/guidance for an LLM judge (e.g. what to look for, why the expected result is correct) when the criterion uses an `llm` grader.

Represent all legitimate correct behaviors. Do not force one canonical answer when several are valid.

Do not add fields the grader or metrics do not use. Never expose `expected` to component execution.

## Metadata

Optional. Use only for analysis or maintenance, for example:

```yaml
metadata:
  scenario: ambiguous_request
  source: expert_authored
  tags: [multi_turn]
```

Metadata must not affect component execution or grading semantics.

If the grader needs a field, put it in `expected`.

## Field definitions

For every `input` and `expected` field define:

- type or structure;
- meaning;
- required/optional;
- relevant constraints;
- omission semantics when optional.

Do not prescribe implementation-language schemas.

## Coverage

Define only scenario categories that can expose materially different behavior or grader outcomes.

Example for `tool_selection`:

```text
clear tool match
competing tools
multiple acceptable tools
no appropriate tool
ambiguous request
```

Do not apply generic scenario lists mechanically.

Specify:

- representative cases needed for normal behavior;
- targeted cases needed for boundaries, ambiguity, known weaknesses, high-consequence behavior, or regressions.

Do not define metric weighting.

## Authoring guidance

Provide only criterion-specific guidance needed to prevent poor case generation.

Include when relevant:

- realism constraints;
- important variation dimensions;
- source of expected truth;
- required case properties;
- cases that must be included;
- constructions that would make the eval trivial or misleading.

Example:

```text
- Requests should resemble real router traffic.
- Available tool combinations must be valid.
- Acceptable tools must be grounded in the component contract.
- Avoid wording that reveals the expected tool.
```

## Ground truth

Expected values must come from a defensible source:

- component contract;
- repository-defined specifications or invariants;
- product requirements;
- authoritative domain information;
- approved expert judgment;
- confirmed regressions.

Do not treat observed current implementation behavior as ground truth merely because it exists in the repository.

Do not invent expected truth. If required truth is unavailable, record the dependency for dataset implementation.

## Leakage

Maintain:

```text
input    → component
expected → grader
metadata → analysis/maintenance
```

Never expose `expected` or analysis metadata to component execution.

## Downstream dataset requirements

The design must define enough information for a future dataset-authoring stage to create concrete cases without inventing semantics:

- input structure or semantics;
- expected structure or semantics;
- legitimate alternatives;
- required scenario coverage;
- representative vs targeted coverage;
- ground-truth sources;
- criterion-specific authoring constraints.

The dataset-authoring stage owns concrete cases, case count, authoring/generation approach, serialization/files, dataset validation, deduplication, balancing mechanics, dataset tooling, and regression curation.

`evals-criterion-implementation` does not own full dataset creation.
