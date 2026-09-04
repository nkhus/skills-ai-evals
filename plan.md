# Target Source Changes

This document defines the target changes to the existing eval skill sources and the intended structure of `evals-criterion-implementation`.

The goal is to keep skills DRY and context-efficient:

```text
evaluation semantics     → approved specs
reusable contracts/code  → bundled framework
workflow                 → SKILL.md
conditional know-how     → references
```

Do not preserve design or reference material that duplicates another source of truth.

---

# 1. `evals-project-init/SKILL.md`

**Action:** Update

## Target responsibility

`evals-project-init` should only validate or create the minimal eval workspace required by the current workflow.

Target structure:

```text
evals/
├── README.md
├── config.yaml
└── components/
```

Remove mandatory initialization of:

```text
evals/suites/
evals/runs/
```

These belong to future execution/orchestration work and should not be introduced before their contracts are designed.

Keep:

```yaml
version: 1
components: {}
```

as the minimal configuration contract.

## Boundary

The skill must not:

* inspect evaluation progress;
* choose the next workflow stage;
* resume criterion work;
* create component-specific artifacts;
* introduce execution, persistence, suite, or run architecture.

Continuation/resume behavior belongs to the future orchestrator described later in this document.

---

# 5. `evals-criterion-design/references/grader-design.md`

**Action:** Update

## Preserve the core grader contract

Keep:

```text
grader = one criterion × one case × one execution
```

Supported grader types remain:

```text
code
llm
```

Do not introduce a `hybrid` type.

Keep the existing concepts:

* focused judgment;
* minimum required case/reference inputs;
* observable execution inputs;
* applicability;
* `scored`;
* `not_applicable`;
* `invalid_case`;
* `insufficient_evidence`;
* `grader_error`;
* label/value semantics;
* deterministic label-to-value mapping;
* details/evidence;
* legitimate alternatives.

## Replace trial terminology

Remove framework-level `trial` terminology.

Use:

```text
execution
```

when referring to one concrete component execution.

Do not define repeated-execution aggregation in grader design.

## Add atomicity as a strong design rule

An LLM grader should evaluate one atomic behavioral dimension.

Target principle:

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

If one grader must independently judge several meaningful qualities, this is normally evidence that the criterion is not atomic enough.

Prefer fixing the criterion boundary rather than compensating with a complex grader.

## LLM-as-a-judge simplicity rule

An LLM grader should normally use:

```text
one focused prompt
one structured response model
one LLM call
one Grade
```

Do not create by default:

```text
judge agents
multi-step judge workflows
multiple sequential judge calls
sub-graders for separate qualities
self-reflection loops
majority-vote judging
multi-agent debates
```

Such complexity is allowed only when the approved criterion fundamentally cannot be evaluated reliably with one focused judgment.

Deterministic:

```text
input preparation
parsing
schema validation
label → value mapping
post-processing
```

does not make the grader multi-stage and does not create another grader type.

---

# 6. `evals-criterion-design/references/metric-design.md`

**Action:** Rewrite and shorten substantially

This reference should explain the **role of metrics**, not teach custom metric design.

## Core principle

Criterion-specific semantics belong to the grader.

Metrics should remain generic reusable DS/statistical aggregations over grader outputs.

Target flow:

```text
criterion-specific behavior
        ↓
grader
        ↓
Grade(label / value / status)
        ↓
generic metric
```

The metric must not reinterpret component behavior.

## Prefer pre-implemented generic metrics

Criterion design should normally select from the reusable framework metric set.

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

The set may later grow with other established generic metrics, for example:

```text
macro / micro classification metrics
ROC-AUC
NDCG
MRR
MAP
other established DS/statistical metrics
```

when they become necessary.

A missing generic metric should normally be added to the reusable framework metric package rather than implemented specifically for one criterion.

## Remove criterion-specific metric design as the default

Do not create custom formulas merely because a criterion has custom semantics.

Instead:

```text
custom criterion semantics
→ normalize through grader output
→ reuse generic metric
```

Example:

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
numeric quality:
Grade.value

categorical prediction:
Grade.label

classification reference:
TestCase.expected["label"]

classification prediction:
Grade.label
```

For binary:

```text
precision
recall
f1
```

the positive label must be explicit.

## Primary metric

Choose one primary generic metric that best represents criterion performance.

Do not invent equivalent metrics unnecessarily.

Supporting metrics are allowed only when they materially improve interpretation.

Examples:

```text
status rate
label distribution
scored coverage
insufficient-evidence rate
grader-error rate
```

## Non-scored results

Quality metrics normally operate only on:

```text
Grade.status == "scored"
```

Never silently convert:

```text
not_applicable
invalid_case
insufficient_evidence
grader_error
```

into quality score `0`.

## Slices

A slice is the same generic metric applied to a subset:

```text
accuracy
accuracy[ambiguous_request]
accuracy[multi_turn]
```

Do not define a separate metric merely because a slice exists.

## Remove repeated-trial semantics

Delete all concepts such as:

```text
trial aggregation
mean_per_case
success rate per case
all trials correct
mean_across_cases
```

The framework uses flat execution observations.

If the same case is executed several times:

```text
execution_id_1 → GradeRecord
execution_id_2 → GradeRecord
execution_id_3 → GradeRecord
```

These remain independent observations at this framework level.

## Keep metric design minimal

Criterion design should specify only what downstream implementation cannot infer automatically, for example:

```yaml
primary:
  metric: accuracy

supporting:
  - metric: status_rate
    status: insufficient_evidence

slices:
  - ambiguous_request
```

or:

```yaml
primary:
  metric: mean
  source: grade.value
```

Do not restate standard mathematical definitions, ranges, or implementation details when they are intrinsic to a known generic metric.

## Boundary

Metric design does not own:

```text
grader semantics
dataset construction
execution grouping
release thresholds
acceptance policy
execution configuration
```

---

# 7. `evals-criterion-design/references/dataset-design.md`

**Action:** Update

## Record contract remains

```yaml
id: case-id
input: {}
expected: {}
metadata: {}
```

`metadata` remains optional.

## Update ownership model

Replace:

```text
component contract → input
grader contract    → expected
```

with:

```text
component contract        → input
grader + metric contracts → expected
analysis / maintenance    → metadata
```

A more general interpretation is:

```text
input
→ information the real component receives

expected
→ reference truth required to evaluate the case

metadata
→ analysis / maintenance information
```

## `expected`

`expected` may be consumed:

* directly by the grader;
* by generic metrics requiring standardized reference truth.

Example:

```text
TestCase.expected["label"]
```

may be used as the reference class for classification metrics.

Do not expose `expected` to component execution.

## Metadata

Keep the rule:

```text
metadata does not affect component execution or grading semantics
```

Generic quality metrics should not depend on metadata.

Metadata may be used externally for:

```text
analysis
maintenance
slicing
provenance
```

## Downstream ownership

Rename the final section from:

```text
Implementation handoff
```

to:

```text
Downstream dataset requirements
```

The design must define enough information for a future dataset-authoring stage to create concrete cases without inventing semantics.

The dataset-authoring stage will own:

```text
concrete cases
case count
authoring/generation approach
serialization/files
dataset validation
deduplication
balancing mechanics
dataset tooling
regression curation
```

`evals-criterion-implementation` does not own full dataset creation.

---

# 8. `evals-criterion-design/SKILL.md`

**Action:** Update slightly

## Keep workflow

Preserve:

```text
grader design
→ metric selection/design
→ dataset contract
→ required observability
→ user approval
```

## Metric step

The metric step should emphasize:

```text
select suitable generic pre-implemented metric(s)
```

rather than designing criterion-specific aggregation code.

If an appropriate established generic metric is missing, the design may identify the required generic metric semantics for later addition to the shared framework.

## Remove trial terminology

Remove `trial-count` and other repeated-trial terminology.

Execution configuration is outside criterion design.

## Clarify completion wording

Replace wording such as:

> implementation does not need to decide...

with:

> downstream stages do not need to invent semantic evaluation choices.

Different downstream stages may consume different parts of the design:

```text
criterion implementation
→ grader + generic metric support

dataset authoring
→ concrete evaluation cases

future runtime
→ execution / persistence / orchestration
```

## Preserve boundary

Criterion design still must not:

* implement evaluation code;
* generate concrete evaluation datasets;
* choose provider/model runtime;
* define execution policy;
* define acceptance/release thresholds.

---

# 9. `evals-criterion-implementation`

**Action:** Create

## Target responsibility

Consumes one approved criterion specification and implements it without changing semantic evaluation decisions.

Owns:

```text
grader implementation
reuse of shared metrics
addition of missing reusable generic metrics when necessary
minimal implementation smoke tests
implementation validation
installation/reuse of bundled framework code
```

Does not own:

```text
criterion design
grader semantic design
metric semantic design
full dataset generation
component execution
stage orchestration
persistence
LLM grader calibration
release policy
component integration
```

---

# 10. Target `evals-criterion-implementation` structure

```text
evals-criterion-implementation/
├── SKILL.md
├── references/
│   ├── grader-implementation.md
│   ├── llm-grader-implementation.md
│   └── implementation-validation.md
└── code/
    └── framework/
        ├── __init__.py
        ├── models.py
        ├── grading.py
        ├── llm.py
        └── metrics/
            ├── __init__.py
            ├── numeric.py
            └── classification.py
```

Do **not** create:

```text
custom-metric-implementation.md
```

as a standard reference.

---

# 11. Bundled framework code

**Action:** Keep as executable code, not references

The framework package is the authoritative executable contract for:

```text
TestCase
ExecutionArtifact
ExecutionRecord
Grade
GradeRecord
MetricResult

Grader Protocol
LLMClient Protocol

shared metrics
```

Do not create prose references duplicating these APIs.

## Installation target

Bundled code is reused/installed under:

```text
evals/framework/
```

Rules:

* create missing framework files from bundled code;
* preserve compatible existing framework implementations;
* do not silently overwrite incompatible framework code.

---

# 12. Shared metrics package

Shared metrics are part of the framework:

```text
code/framework/metrics/
├── __init__.py
├── numeric.py
└── classification.py
```

Initial shared functions:

```text
mean
median
label_rate
status_rate
accuracy
precision
recall
f1
```

## Adding missing metrics

If an approved criterion requires an established generic metric that is missing:

```text
identify reusable generic metric
→ add it to framework/metrics/
→ add framework-level tests
→ reuse it from criterion implementation
```

Example future modules may include:

```text
ranking.py
statistics.py
```

Avoid:

```text
evals/components/{component}/metrics/{criterion_id}.py
```

for normal criterion implementation.

Criterion semantics should not be encoded in metric functions.

A genuinely domain-specific mathematical measure should be treated as an exceptional architectural case rather than a default extension mechanism.

---

# 13. Criterion grader implementation

Target location:

```text
evals/components/{component}/graders/{criterion_id}.py
```

One criterion produces one grader implementation.

Code grader example:

```text
ToolSelectionGrader
```

LLM grader example:

```text
RelevanceGrader
```

No implementation manifest or handoff YAML is required.

---

# 14. `references/grader-implementation.md`

**Action:** Create

This reference contains implementation rules common to all graders.

Expected scope:

```text
one criterion × one case × one execution

async Grader interface

allowed semantic inputs:
- case.input
- case.expected
- artifact.output
- artifact.trace
- artifact.errors

case.metadata is not grading semantics
artifact.metadata is not grading semantics

non-scored statuses are not quality zero

component failure may still be graded when relevant

reasoning is concise justification
details contain structured evidence

no aggregation
no metric calculation
no component execution
no persistence
```

Include only minimal deterministic grader guidance.

Do not repeat upstream design guidance about:

```text
choosing code vs llm
designing labels
defining applicability
selecting metrics
```

---

# 15. `references/llm-grader-implementation.md`

**Action:** Create

Load only when:

```yaml
type: llm
```

Assume common grader rules are already known from `grader-implementation.md`.

Expected implementation shape:

```text
criterion-specific focused prompt
+
criterion-specific Pydantic response model
+
injected LLMClient
+
one structured generation call
+
response → Grade mapping
```

Rules:

* inject `LLMClient`;
* do not instantiate provider SDK clients;
* do not embed credentials;
* provider/model selection belongs to `LLMClient`;
* use one focused prompt;
* use one structured response model;
* use one LLM call by default;
* implement approved label → value mapping deterministically;
* map LLM/runtime failures to `grader_error`;
* do not create multi-agent/multi-step judge pipelines unless explicitly required by the approved design.

---

# 16. `references/implementation-validation.md`

**Action:** Create

Defines sufficient evidence for criterion implementation to be considered complete.

## Smoke tests

Test only implementation behavior needed by the approved contract.

Typical tests when relevant:

```text
positive
negative
partial / boundary
not_applicable
invalid_case
insufficient_evidence
```

## Code graders

Validate:

```text
grader imports
grader instantiates
expected Grade behavior
non-scored behavior
label/value semantics
details/reasoning when relevant
```

## LLM graders

Use an injected fake/stub `LLMClient`.

Do not require a real external judge call.

Validate:

```text
prompt path executes
Pydantic response model is accepted
response → Grade mapping
label → value mapping
provider/runtime failure → grader_error
```

## Metrics

If the implementation adds a new generic framework metric:

```text
add framework-level tests
validate normal case
validate no usable data
validate invalid scored data
validate relevant edge cases
```

## Completion

Run the repository's normal relevant test command.

Tests are implementation smoke tests, not evidence of:

```text
dataset coverage
representativeness
balancing
statistical confidence
LLM judge calibration
```

---

# 17. Implementation test location

Criterion implementation tests live in the repository's global project-level test tree.

Do not place tests inside:

```text
evals/components/{component}/
```

The exact path follows existing repository test conventions.

Do not introduce a separate fixture-file abstraction unless the repository already needs one.

Construct:

```text
TestCase
ExecutionArtifact
fake LLMClient
```

directly in normal Python tests.

---

# 18. References explicitly not needed

Do not create:

```text
models.md
framework.md
metric-api.md
shared-metrics.md
llm-client.md
layout.md
dataset-implementation.md
persistence.md
runtime-flow.md
implementation-handoff.md
code-grader-implementation.md
custom-metric-implementation.md
test-fixtures.md
```

Ownership:

```text
models / protocols / metrics
→ bundled executable framework

layout / workflow
→ SKILL.md

dataset authoring
→ future dedicated stage

persistence / execution orchestration
→ downstream runtime work

implementation handoff
→ intentionally absent

code grader specifics
→ grader-implementation.md

LLM specifics
→ llm-grader-implementation.md

test behavior
→ implementation-validation.md
```

---

# 19. Sources/artifacts to remove

## Superseded implementation-decision documents

Delete old criterion-implementation brainstorming documents once their decisions have been incorporated into the target sources.

Keep only the consolidated decision document while the implementation skill is still being designed.

## Consolidated decision document

Keep temporarily:

```text
evals-criterion-implementation-decisions-consolidated.md
```

Delete it from the shipped skill after:

```text
SKILL.md
references/*
code/framework/*
```

fully encode its decisions.

It is a design artifact, not runtime context.

## Framework ZIP

Do not ship:

```text
evals-framework-code.zip
```

Ship the extracted `code/framework/` tree directly.

---

# 20. Future orchestrator requirements

**Apply when ****`evals-orchestrator`**** is designed.**

Do not add this responsibility to `evals-project-init`.

## Goal

The user should be able to say things such as:

```text
continue eval work
continue criterion relevance
implement the next criterion
resume component X
```

without manually selecting a workflow skill.

## Orchestrator responsibility

The orchestrator should:

```text
resolve component / criterion when specified
        ↓
inspect existing eval artifacts and approval states
        ↓
determine current workflow position
        ↓
find the earliest required incomplete step
        ↓
invoke the correct specialized skill
        ↓
continue from repository state
```

Example:

```text
User:
"Continue working on relevance."

Repository:
component analysis       → approved
criteria                 → approved
relevance criterion spec → approved
grader implementation    → missing

Result:
invoke evals-criterion-implementation
for criterion relevance
```

Another example:

```text
criterion exists
but criterion design is not approved

→ resume evals-criterion-design
```

## State source

Prefer deriving workflow state from deterministic repository artifacts and explicit approval statuses.

Do not introduce a separate orchestration state database/file unless artifact-derived state proves insufficient.

Examples:

```text
component README Status: Approved
criteria.yaml status: approved
criterion spec Status: Approved
expected implementation file exists
```

## Boundary

The orchestrator owns:

```text
routing
resume/continue semantics
workflow progression
```

It does not own:

```text
component analysis semantics
criteria discovery
criterion design
grader implementation
dataset generation
evaluation execution
```

Specialized skills remain responsible for their own stages.

## Invocation model

Target direction:

```text
evals-orchestrator
→ user-invocable entry point

specialized evals-* skills
→ internal workflow skills
```

The exact orchestration mechanism should be decided when this skill is designed.

---

# 21. Target source set after this phase

```text
evals-project-init/
└── SKILL.md

evals-component-analysis/
└── SKILL.md

evals-criteria-discovery/
├── SKILL.md
└── references/
    └── criteria-guide.md

evals-criterion-design/
├── SKILL.md
└── references/
    ├── grader-design.md
    ├── metric-design.md
    └── dataset-design.md

evals-criterion-implementation/
├── SKILL.md
├── references/
│   ├── grader-implementation.md
│   ├── llm-grader-implementation.md
│   └── implementation-validation.md
└── code/
    └── framework/
        ├── __init__.py
        ├── models.py
        ├── grading.py
        ├── llm.py
        └── metrics/
            ├── __init__.py
            ├── numeric.py
            └── classification.py
```

Future:

```text
evals-orchestrator/
└── SKILL.md
```

Additional dataset/runtime/execution skills will be designed separately rather than being anticipated inside the current skills.

---

# 22. Implementation order

Apply changes in this order:

```text
1. Rewrite metric-design.md
2. Update dataset-design.md
3. Update grader-design.md
4. Update evals-criterion-design/SKILL.md
5. Simplify evals-project-init/SKILL.md
6. Create grader-implementation.md
7. Create llm-grader-implementation.md
8. Create implementation-validation.md
9. Write final evals-criterion-implementation/SKILL.md
10. Validate bundled framework code against the final skill
11. Remove superseded decision artifacts / ZIP
12. Design orchestrator later using section 20 as requirements
```
