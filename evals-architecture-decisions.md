# AI Evals Skills — Architecture Decisions

Status: Working decision log  
Repository source of truth: `https://github.com/nkhus/skills-ai-evals`

This document tracks architectural decisions for the eval skill set. When it conflicts with older brainstorming, this document should be treated as the current direction unless a newer decision explicitly supersedes it.

---

## 1. Design principles

### Keep skills DRY and focused

Each skill owns one stage of the evaluation lifecycle.

```text
SKILL.md       -> workflow, deterministic locations, stage boundaries
references/    -> conditional non-obvious guidance
code/          -> reusable executable contracts and algorithms
approved specs -> evaluation semantics
```

Do not explain in prose what can be inspected directly from bundled executable code.

### Repository artifacts are the handoff

Skills should read upstream decisions from repository artifacts instead of passing large conversational summaries between stages.

Routing input should stay minimal:

```text
Component: {component}
Criterion: {criterion_id}
```

### Semantic decisions happen upstream

```text
component-analysis
→ what the component owns and how it behaves

criteria-discovery
→ what behavioral dimensions should be evaluated

criterion-design
→ how one criterion is judged and measured

implementation/runtime stages
→ implement and execute approved contracts
```

Downstream implementation stages must not reinterpret approved evaluation semantics.

---

## 2. Current design pipeline

The current semantic/design flow is:

```text
evals-project-init
        ↓
evals-component-analysis
        ↓
evals-criteria-discovery
        ↓
evals-criterion-design
```

After criterion design, work splits into two independent branches:

```text
                           ┌→ criterion-implementation
criterion-design ──────────┤
                           └→ dataset-authoring
```

These branches are siblings.

### `criterion-implementation`

Owns:

```text
grader implementation
shared metric reuse
generic metric addition when needed
criterion-specific metric implementation only when necessary
implementation smoke tests
implementation validation
bundled framework installation/reuse
```

Does not own:

```text
full evaluation dataset generation
component execution
grading orchestration
metric execution orchestration
persistence/runtime
LLM grader calibration
release policy
```

### `dataset-authoring`

Will own:

```text
concrete TestCase records
dataset construction
dataset validation
coverage realization
balancing/deduplication mechanics
regression cases
dataset files/serialization
```

It must not redefine:

```text
input semantics
expected semantics
required coverage categories
ground-truth rules
criterion semantics
grader semantics
```

---

## 3. Dataset contract

Canonical framework model:

```python
class TestCase(BaseModel):
    id: str
    input: dict[str, Any]
    expected: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)
```

Semantics:

```text
id       -> stable case identity
input    -> real component input
expected -> grader reference information
metadata -> analysis / maintenance only
```

Hard rule:

```text
input    -> component
expected -> grader
metadata -> analysis / maintenance
```

The component must never receive `expected`.

Analysis metadata must not change component behavior or grading semantics.

---

## 4. Execution and grading are independent

This is a hard architectural invariant.

### Component execution is grader-independent

Component inference/execution must know nothing about:

```text
grader
criterion
metric
expected values
quality score
```

Active execution:

```text
dataset
  +
component
  ↓
execution
  ↓
ExecutionRecord[]
```

The executor consumes only:

```text
TestCase.id
TestCase.input
```

It must not use `TestCase.expected` or `TestCase.metadata` for component behavior.

### Execution results are reusable

One execution result may be evaluated by multiple graders:

```text
                         ┌→ grader A → grades A
ExecutionRecord[] ───────┼→ grader B → grades B
                         └→ grader C → grades C
```

Changing or adding a grader must not require component reinference.

### Current execution models

```python
class ExecutionArtifact(BaseModel):
    output: dict[str, Any] | None = None
    trace: dict[str, Any] | None = None
    errors: list[Any] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExecutionRecord(BaseModel):
    execution_id: str
    case_id: str
    artifact: ExecutionArtifact
```

`ExecutionArtifact` contains observable execution evidence only.

Do not persist hidden chain-of-thought.

---

## 5. Grading is a separate stage

Grading consumes already-produced execution results.

```text
ExecutionRecord[]
      +
TestCase[]
      +
grader
      ↓
GradeRecord[]
```

Current framework model:

```python
class GradeRecord(BaseModel):
    execution_id: str
    case_id: str
    grade: Grade
```

A grader evaluates exactly:

```text
one criterion
× one TestCase
× one ExecutionArtifact
```

A grader does not:

```text
run the component
aggregate across executions
calculate dataset-level metrics
persist execution data
```

Grading should be rerunnable independently from inference.

---

## 6. Metrics are a separate stage

Metric calculation consumes persisted `GradeRecord[]`.

Metrics are generic reusable aggregations and should not carry criterion semantics.

Current shared metric direction:

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

Pipeline:

```text
ExecutionRecord[]
      ↓
grading
      ↓ persist
GradeRecord[]
      ↓
metric calculation
      ↓
MetricResult
```

Inference, grading, and metric calculation should be independently rerunnable stages.

---

## 7. Identity model

Current vocabulary:

```text
case_id      -> TestCase identity
execution_id -> one concrete component execution
run_id       -> one invocation/configuration of a stage
```

There is no `trial_id`.

If a case is executed multiple times, each execution receives a different `execution_id`.

The framework does not group repeated executions by case.

---

## 8. Execution acquisition must support two sources

Execution observations should eventually come from two acquisition paths.

### Active inference

```text
TestCase.input
    +
component
    ↓
execute
    ↓
ExecutionRecord
```

### Existing traces

Future trace-based evaluation:

```text
production / historical trace
        ↓
extract component input/output/trace
        ↓
ExecutionRecord-compatible observation
```

Downstream graders should not care whether an execution observation came from active eval inference or trace extraction.

---

## 9. Execution observation vs evaluation case

Do not conflate observed execution data with evaluation reference data.

```text
Execution observation
= what actually happened

Evaluation case
= component input + grader reference information
```

A production trace may provide:

```text
input
output
trace
execution metadata
```

without providing:

```text
expected
```

Therefore trace extraction should not fabricate a complete `TestCase`.

Reference information may later come from annotation, matching, or another dataset construction process.

---

## 10. Target runtime architecture

```text
                     criterion-design
                    /                \
                   /                  \
      criterion-implementation    dataset-authoring
                   |                  |
                   |                  ↓
                   |         execution acquisition
                   |          /              \
                   |     active inference   trace extraction
                   |          \              /
                   |           ExecutionRecord[]
                   |                  |
                   └──────────────────┤
                                      ↓
                                   grading
                                      ↓
                                GradeRecord[]
                                      ↓
                                   metrics
```

Execution does not depend on grader implementation.

Grading depends on:

```text
execution data
test/reference data
grader implementation
```

Metric calculation depends on:

```text
GradeRecord[]
metric selection/configuration
```

---

## 11. Persistence and stage independence

Intended logical flow:

```text
inference / acquisition
    ↓ persist
ExecutionRecord[]

grading
    ↓ persist
GradeRecord[]

metric calculation
    ↓ persist
MetricResult
```

Each stage should be runnable independently against persisted upstream outputs.

Exact run-level models and persistence schemas are not finalized yet.

Conceptually:

```text
InferenceRun
GradingRun
MetricRun
```

may later own stage-level provenance.

Do not copy run-level provenance into every framework value object unless necessary.

---

## 12. Runtime skill decomposition

Do not create one large generic runtime skill.

Current preferred decomposition:

```text
evals-component-execution
evals-grading
evals-metric-calculation
```

Future parallel acquisition path:

```text
evals-trace-extraction
```

These should compose through persisted framework records.

Final names and exact boundaries remain open.

---

## 13. Component integration

`component-integration` comes after the core implementation/data/runtime contracts are stable.

Its role should be integration/wiring, not semantic design.

It must not couple component execution to a specific grader.

Exact responsibilities are still to be designed.

---

## 14. Orchestrator

The orchestrator should be designed last.

Expected responsibility:

```text
resolve component / criterion
inspect repository state
determine next runnable stage
route work
resume independent stages
```

It must preserve the independence of:

```text
dataset authoring
component execution
grading
metric calculation
```

---

## 15. Current overall skill direction

```text
evals-project-init
        ↓
evals-component-analysis
        ↓
evals-criteria-discovery
        ↓
evals-criterion-design
        ├── evals-criterion-implementation
        └── evals-dataset-authoring
                    ↓
            execution acquisition
             ├── component execution
             └── trace extraction (future)
                    ↓
               evals-grading
                    ↓
          evals-metric-calculation
                    ↓
          component integration
                    ↓
               orchestrator
```

---

## 16. Next design step

Next skill to define:

```text
evals-dataset-authoring
```

After that, define the active execution/runtime path while preserving the grader-independent execution invariant.

Open questions:

```text
- exact dataset-authoring output layout and files
- exact runtime/persistence package layout
- run-level provenance models
- exact component-execution skill boundary
- exact trace-extraction normalization contract
- grading persistence/orchestration contract
- metric-run persistence contract
- component-integration responsibilities
- orchestrator state/resume logic
```
