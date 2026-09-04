# AI Evals Skills — Target Architecture

Status: Target design  
Repository source of truth: `https://github.com/nkhus/skills-ai-evals`

This document defines the target architecture of the evaluation skill set and runtime.

---

## 1. Core design principles

### Skills build the evaluation system

Skills are used for semantic discovery, design, implementation, and integration.

They should not be used to execute deterministic runtime stages that are better represented as Python code.

```text
skills
→ build/configure the eval system

python runtime
→ execute the eval system
```

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

Skills read upstream decisions from repository artifacts rather than receiving large conversational summaries.

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

implementation/integration
→ implement and wire approved contracts
```

Downstream stages must not reinterpret approved evaluation semantics.

---

## 2. Target build pipeline

The build pipeline is:

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
          evals-component-execution
                    ↓
         evals-component-integration
                    ↓
              evals-orchestrator
                    ↓
              EVALUATION READY
```

`criterion-implementation` and `dataset-authoring` are sibling branches.

They both consume the approved criterion design and may be completed independently.

---

## 3. Current semantic/design stages

### `evals-project-init`

Ensures the repository has a valid eval workspace.

It does not introduce runtime, persistence, suite, or execution architecture.

### `evals-component-analysis`

Establishes:

```text
component purpose
component boundary
inputs / outputs / state
important dependencies
expected behavior
legitimate variability
failure behavior
observable behavior
evaluation surface
```

It does not define evaluation criteria.

### `evals-criteria-discovery`

Produces the approved list of independently meaningful behavioral criteria for the component.

It defines what should be evaluated, not how.

### `evals-criterion-design`

Turns one approved criterion into an implementation-ready semantic contract.

It defines:

```text
grader contract
generic metric selection
dataset contract
coverage requirements
authoring guidance
required observability
limitations
```

It does not create concrete dataset cases or implementation code.

---

## 4. Criterion implementation branch

`evals-criterion-implementation` consumes one approved criterion specification.

It owns:

```text
grader implementation
shared metric reuse
generic metric addition when needed
criterion-specific metric implementation only when shared metrics are insufficient
implementation smoke tests
implementation validation
bundled framework installation/reuse
```

It does not own:

```text
full evaluation dataset generation
component execution
runtime orchestration
runtime persistence
LLM grader calibration
release thresholds
evaluation execution
```

The implementation is Python-only.

Reusable framework code is installed under:

```text
evals/framework/
```

The framework provides the shared models, grader contract, LLM client abstraction, and generic metrics.

---

## 5. Dataset authoring branch

`evals-dataset-authoring` consumes the approved dataset section of one criterion design and creates the concrete evaluation cases.

It owns:

```text
concrete TestCase records
dataset construction
dataset files / serialization
coverage realization
balancing mechanics
deduplication
dataset validation
regression cases
```

It must not redefine:

```text
input semantics
expected semantics
required coverage categories
ground-truth rules
criterion semantics
grader semantics
metric semantics
```

The approved criterion design is the source of truth for dataset semantics.

---

## 6. Dataset contract

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
id       -> stable evaluation case identity
input    -> real component input
expected -> grader reference information
metadata -> analysis / maintenance only
```

Hard separation:

```text
input    -> component execution
expected -> grading
metadata -> analysis / maintenance
```

The component must never receive `expected`.

`metadata` must not change component behavior or grading semantics.

---

## 7. Component execution is grader-independent

This is a hard architectural invariant.

Component execution must know nothing about:

```text
grader
criterion
metric
expected values
quality score
```

Active execution does:

```text
TestCase.input
    +
component
    ↓
component execution
    ↓
ExecutionRecord[]
```

Execution may use:

```text
TestCase.id
TestCase.input
```

It must not use:

```text
TestCase.expected
TestCase.metadata
```

for component behavior.

Changing or adding a grader must never require component reinference.

---

## 8. Execution data model

Execution records represent reusable observations of component behavior.

Target model:

```python
class ExecutionArtifact(BaseModel):
    output: dict[str, Any] | None = None
    trace: dict[str, Any] | None = None
    errors: list[Any] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExecutionRecord(BaseModel):
    execution_id: str
    source_id: str
    input: dict[str, Any]
    artifact: ExecutionArtifact
```

### `execution_id`

Identity of one concrete execution observation.

If the same source is executed multiple times, every execution receives a different `execution_id`.

### `source_id`

Identity of the source from which the execution originates.

For active dataset execution:

```text
TestCase.id
→ ExecutionRecord.source_id
```

For future trace-derived execution:

```text
trace / span / event identity
→ ExecutionRecord.source_id
```

`source_id` is intentionally source-neutral and replaces a dataset-specific `case_id` in persisted execution records.

### `input`

Exact component input associated with the observed execution.

Persisting the input makes the execution record self-contained and reusable independently from the original dataset.

### `artifact`

Observable execution evidence:

```text
output
trace
errors
runtime metadata
```

Never persist hidden chain-of-thought.

---

## 9. Execution acquisition

Execution observations may come from multiple sources.

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

For an authored evaluation case:

```text
source_id = TestCase.id
input     = TestCase.input
```

### Future trace extraction

```text
production / historical trace
        ↓
extract component input / output / trace
        ↓
ExecutionRecord
```

For trace-derived observations:

```text
source_id = trace/span/event identity
input     = extracted component input
artifact  = extracted output/trace/errors
```

Downstream grading must not depend on how an `ExecutionRecord` was acquired.

---

## 10. Execution observation vs evaluation case

Execution observations and evaluation cases are different concepts.

```text
ExecutionRecord
= what actually happened

TestCase
= authored evaluation input + grader reference data
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

Trace extraction must not fabricate reference truth.

Reference information for trace-derived observations may later come from:

```text
annotation
matching to an existing evaluation case
expert labeling
another reference-enrichment process
```

---

## 11. Component execution skill

`evals-component-execution` is a build-time skill.

It does not run a complete evaluation.

Its responsibility is to implement the component-specific execution adapter.

Conceptually:

```python
async def execute(input: dict[str, Any]) -> ExecutionArtifact:
    ...
```

The adapter translates:

```text
generic evaluation input
        ↓
real component invocation
        ↓
ExecutionArtifact
```

It must be grader-independent.

The adapter should expose the union of observability required by approved criterion designs.

Example:

```text
criterion A requires final output
criterion B requires selected tool
criterion C requires retrieved items

component execution adapter
→ output + selected tool + retrieved items
```

The skill does not implement grading or metrics.

---

## 12. Grading is Python runtime code

Grading is not a skill.

It is deterministic runtime infrastructure that consumes already-produced execution observations.

Conceptually:

```text
ExecutionRecord[]
      +
reference TestCase data
      +
grader
      ↓
GradeRecord[]
```

Target identity model:

```python
class GradeRecord(BaseModel):
    execution_id: str
    source_id: str
    grade: Grade
```

Semantics:

```text
execution_id -> exact execution that was graded
source_id    -> linkage to reference data when available
grade        -> case-level criterion judgment
```

One persisted execution may be reused by multiple graders:

```text
                         ┌→ grader A → GradeRecord[]
ExecutionRecord[] ───────┼→ grader B → GradeRecord[]
                         └→ grader C → GradeRecord[]
```

A grader evaluates:

```text
one criterion
× one execution
× available reference data
```

A grader does not run the component.

---

## 13. Metric calculation is Python runtime code

Metric calculation is not a skill.

It consumes persisted `GradeRecord[]` and applies the metric selection already defined during criterion design.

Current generic metric direction:

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

Metrics are reusable statistical aggregations.

Criterion semantics belong to graders, not metrics.

Conceptually:

```text
GradeRecord[]
    +
metric configuration
    ↓
MetricResult
```

---

## 14. Runtime stage independence

Runtime stages are independently rerunnable.

```text
inference
    ↓ persist
ExecutionRecord[]

grading
    ↓ persist
GradeRecord[]

metric calculation
    ↓ persist
MetricResult
```

This enables:

```text
change grader
→ rerun grading + metrics
→ no reinference

change metric selection
→ rerun metrics only

add another grader
→ grade existing ExecutionRecord[]
```

Inference is the expensive component-execution stage and should be reusable whenever possible.

---

## 15. Runtime identity model

Target vocabulary:

```text
source_id    -> identity of the input/observation source
execution_id -> one concrete component execution observation
run_id       -> one invocation/configuration of a runtime stage
```

There is no `trial_id`.

Repeated executions of the same source are represented by distinct `execution_id` values sharing the same `source_id`.

The framework does not introduce implicit repeated-execution grouping.

---

## 16. Run-level persistence

Runtime stages persist their outputs.

Conceptually:

```text
InferenceRun
  -> execution configuration
  -> source/dataset selection
  -> ExecutionRecord[]

GradingRun
  -> execution input selection
  -> grader configuration
  -> GradeRecord[]

MetricRun
  -> grading input selection
  -> metric configuration
  -> MetricResult(s)
```

Exact Pydantic models and persistence layout are still implementation details to define in the runtime layer.

Stage-level provenance should remain at run level rather than being copied into every `Grade` or `ExecutionArtifact`.

---

## 17. Evaluation runtime

The final integrated system should expose a Python evaluation entrypoint.

Conceptually:

```text
evaluate.py
```

or a shared equivalent.

The runtime should allow independent stages:

```bash
python evaluate.py infer
python evaluate.py grade
python evaluate.py metrics
```

and a convenience full evaluation:

```bash
python evaluate.py run
```

`run` performs:

```text
infer
  ↓
persist executions
  ↓
grade
  ↓
persist grades
  ↓
metrics
  ↓
evaluation result
```

The exact CLI shape and location are implementation details to finalize later.

---

## 18. Component integration

`evals-component-integration` is the final build stage.

It combines:

```text
component execution adapter
datasets
graders
metric selections
shared Python runtime
```

into a runnable component evaluation.

It owns integration/wiring such as:

```text
component manifest/config
runtime registration
dataset registration
grader registration
metric registration
evaluation entrypoint
persistence configuration
integration validation
```

It must not redefine evaluation semantics.

It must not couple component execution to any specific grader.

Its output is a runnable evaluation configuration.

---

## 19. Orchestrator

`evals-orchestrator` is a build orchestrator.

It should be designed last, after all stage contracts are stable.

Its responsibility is to:

```text
resolve component / criterion
inspect repository state
determine incomplete build stages
route work
resume independent branches
ensure required artifacts are integrated
```

The orchestrator ends when:

> the user can run the evaluation script and obtain an evaluation result.

Success state conceptually:

```text
READY

Component evaluation is implemented and integrated.

Run:
python <evaluation-entrypoint> run
```

The orchestrator does not:

```text
run inference
run graders
calculate metrics
wait for evaluation runs
interpret evaluation results
make release decisions
```

Those are runtime or downstream lifecycle concerns.

---

## 20. Target architecture

### Build time

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
          evals-component-execution
                    ↓
         evals-component-integration
                    ↓
              evals-orchestrator
                    ↓
              EVALUATION READY
```

### Run time

```text
dataset
  +
component execution adapter
        ↓
     inference
        ↓
ExecutionRecord[]
        ↓ persist
        ↓
      grading
        ↓
  GradeRecord[]
        ↓ persist
        ↓
      metrics
        ↓
 evaluation result
```

### Future trace path

```text
active inference ─────┐
                      ├→ ExecutionRecord[]
trace extraction ─────┘
                              ↓
                           grading
                              ↓
                           metrics
```

Everything downstream of `ExecutionRecord[]` is shared.

---

## 21. Next design steps

Design next:

```text
1. evals-dataset-authoring
2. finalize ExecutionRecord / GradeRecord framework changes
3. shared Python runtime:
   - inference
   - grading
   - metric calculation
   - persistence/run models
4. evals-component-execution
5. evals-component-integration
6. evals-orchestrator
```

Later:

```text
evals-trace-extraction
trace reference annotation/enrichment
LLM grader calibration
result analysis
release / acceptance policy
regression maintenance
```
