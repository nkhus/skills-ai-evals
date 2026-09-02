---
name: evals-criteria-discovery
description: Discover, refine, and obtain user approval for the high-level evaluation criteria of one analyzed component. Use after component analysis and before designing any individual criterion.
user-invocable: false
---

# Evals Criteria Discovery

## Objective

Produce an approved, high-level list of behavioral evaluation criteria for one
component.

This stage answers only:

> What aspects of this component's behavior should be evaluated?

It does not answer how an individual criterion will be measured or implemented.

## Required input

The orchestrator provides the component name.

Before starting, read:

- `evals/config.yaml`
- `evals/components/{component}/README.md`

The component README is the approved source of truth for the component's
technical and functional behavior.

If either prerequisite is missing, stop and report the missing path. Do not
recreate prerequisite artifacts.

## Outputs

While the list is being discussed, maintain:

- `evals/components/{component}/criteria-discovery.draft.md`

After explicit user approval:

- create `evals/components/{component}/spec/criteria.yaml`
- rename and update `evals/components/{component}/criteria-discovery.draft.md` into `evals/components/{component}/spec/README.md`

`spec/criteria.yaml` is the pipeline completion artifact and the canonical input
for criterion-design subagents.

Do not create individual criterion specifications in this stage.

## Required process

### 1. Read the component analysis

Understand the component's:

- functional goal;
- users and downstream consumers;
- owned decisions and responsibilities;
- expected behavior and prohibited behavior;
- common, difficult, and high-consequence scenarios;
- boundaries with other components;
- observable outputs and traces;
- material unknowns.

Do not repeat component research unless a small repository lookup is required
to resolve a specific ambiguity.

### 2. Ask for the user's initial concerns

Start the criteria conversation by asking:

> What behaviors, scenarios, or quality concerns do you already want to evaluate for this component?

Do not begin with a large assistant-generated catalog.

### 3. Refine the user's proposals

For each proposed item:

- identify the intended behavior;
- confirm that the behavior is owned by this component;
- rewrite vague wording into one clear quality dimension;
- split items that combine materially different behaviors;
- merge items that measure the same behavior;
- separate behavioral evaluation from validation and operations;
- identify ambiguity or missing ownership information;
- explain any challenge or reclassification succinctly.

Classify every proposed item as one of:

- `criterion` — behavioral quality evaluated across representative records;
- `validation_check` — deterministic correctness of files, schemas, imports, or runtime contracts;
- `operational_measurement` — latency, usage, throughput, availability, or similar execution telemetry;
- `out_of_scope` — behavior owned by another component or outside the approved boundary.

Only `criterion` items enter the approved criteria list.

Read `references/criterion-discovery.md` for discovery and refinement rules.

### 4. Maintain the complete current list

After each meaningful iteration, show the full current list, not only the
changes.

For each criterion include only:

- `id`;
- `name`;
- `group`;
- `priority`;
- `intent`;
- optional `out_of_scope` when the boundary would otherwise remain ambiguous;
- status during drafting.

Do not add metric names, score ranges, dataset fields, grader approaches, or
thresholds.

### 5. Ask whether to suggest more criteria

After the user's initial concerns have been refined, ask:

> Would you like me to suggest additional criteria?

If the user says no, proceed toward approval.

If the user says yes, propose a small, component-specific set under two broad
groups:

- `basic` — whether the component performs the required behavior correctly;
- `quality` — how well the component performs the behavior when several outputs
  may be acceptable.

These groups describe the criterion's intent. They do not select the grader.

Read `references/classification-and-priority.md` before making suggestions.

Avoid generic checklists. Every suggestion must be justified by the approved
component analysis.

### 6. Iterate until the list is explicitly approved

Allow multiple rounds of:

- additions;
- removals;
- renaming;
- merging;
- splitting;
- reprioritization;
- reclassification;
- deferral.

Update `criteria-discovery.draft.md` during this process.

Do not treat silence, partial agreement, or approval of one item as approval of
the complete list.

Ask the user to explicitly approve the complete list.

### 7. Write the approved artifacts

Only after explicit approval:

1. create or replace `spec/criteria.yaml` using the approved list;
2. create or replace `spec/README.md` as the readable overview;
3. preserve the order approved by the user;
4. include separately recorded validation checks, operational measurements,
   deferred candidates, rejected candidates, and unresolved questions in the
   README, but not in the YAML `criteria` list;
5. remove the working draft, or clearly mark it superseded.

Use the templates in `templates/` and follow
`references/output-contract.md`.

## Criterion groups

### Basic

A Basic criterion asks whether the component performs a required behavioral
function correctly.

Examples depend on the component and may include correct selection, correct
routing, required action completion, expected information retrieval, or correct
handling of missing information.

Basic does not mean unit test, schema validation, or necessarily code-based.

### Quality

A Quality criterion asks how well the component performs a behavior when
multiple outputs or decisions can be acceptable.

Examples depend on the component and may include relevance, completeness,
usefulness, clarity, ranking quality, contextual appropriateness, or recovery
quality.

Quality does not necessarily require an LLM-based grader.

## Priority

Use:

- `p0` — essential to the component's primary purpose or a high-consequence
  behavioral requirement;
- `p1` — important to normal quality or a frequent meaningful failure;
- `p2` — useful secondary, edge, or exploratory behavior.

Priority represents importance, not implementation order or grader complexity.

## Criterion ID rules

Criterion IDs must:

- be stable;
- use lowercase snake_case;
- describe the behavior rather than the implementation;
- avoid metric names unless the metric is itself the user-approved concept;
- remain unique within the component.

Prefer `tool_selection_correctness` over `llm_judge_tool_score`.

## Stage boundaries

Do not:

- select code-based, LLM-based, or hybrid graders;
- define formulas or detailed metrics;
- define score ranges or thresholds;
- define dataset record fields beyond the later universal `id`, `input`, and
  `expected` envelope;
- create JSONL datasets;
- create individual criterion specs;
- create grader designs or code;
- create or modify the component runner;
- create the component manifest;
- update suites or policies;
- execute evaluations.

## Completion

The stage is complete only when:

- the user explicitly approved the complete criterion list;
- `evals/components/{component}/spec/criteria.yaml` exists;
- `evals/components/{component}/spec/README.md` exists.

Return the created artifact paths. Do not start the next pipeline stage.
