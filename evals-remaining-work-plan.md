The next work should be split into **three phases**. We’ve essentially finished the semantic/design side; now we need to stabilize the runtime core before building the remaining skills around it.

## Phase A — Shared runtime contracts

### 1. Finalize `ExecutionRecord` / `GradeRecord`

This should be the **next working session**.

Current framework still has:

```python
class ExecutionRecord(BaseModel):
    execution_id: str
    case_id: str
    artifact: ExecutionArtifact

class GradeRecord(BaseModel):
    execution_id: str
    case_id: str
    grade: Grade
```

while our target is source-neutral.

We should resolve only these questions:

```text
execution_id semantics
source_id semantics
source_id scope
input persistence
ExecutionRecord final shape
GradeRecord final shape
case_id migration impact
```

The important issue we have now uncovered is:

```text
TestCase.id
→ unique only inside one dataset

but

ExecutionRecord.source_id
→ must later locate reference data
```

Because we deliberately decided **not** to introduce `dataset_id`, I think the clean model is:

> `source_id` is source-local, not globally unique. Its namespace belongs to the run/source context.

For active datasets:

```text
source_id = TestCase.id
```

For future traces:

```text
source_id = trace/span/event identity
```

Later an `InferenceRun` tells us *which source collection* those IDs belong to.

That lets us keep:

```python
class ExecutionRecord(BaseModel):
    execution_id: str
    source_id: str
    input: dict[str, Any]
    artifact: ExecutionArtifact
```

without encoding dataset architecture into every record.

I would also keep:

```python
class GradeRecord(BaseModel):
    execution_id: str
    source_id: str
    grade: Grade
```

and no:

```text
case_id
trial_id
dataset_id
run_id inside every record
```

Run-level provenance comes later.

### 2. Impact analysis and framework model update

Once those semantics are agreed, update:

```text
models.py
metrics using case_id
tests
references mentioning case_id
```

Classification metrics currently explicitly resolve `TestCase` by `record.case_id`, so this is one known migration point.

We should change that deliberately rather than patching it later.

---

## Phase B — Build the generic Python runtime

### 3. Design pure runtime interfaces

Only after models are stable.

No persistence yet.

Conceptually:

```python
infer(...)
    -> list[ExecutionRecord]

grade(...)
    -> list[GradeRecord]

calculate_metrics(...)
    -> list[MetricResult]
```

The key questions are:

```text
what infer receives
executor contract
how execution IDs are created

how grade receives executions + reference cases
how source_id resolves reference data
grader invocation

what calculate_metrics receives
how metrics access reference TestCases where required

record-level failures
stage-level failures
```

One decision we already effectively made should be explicit here:

```text
GradeRecord[] alone is NOT always sufficient for metrics.
```

Classification metrics need reference truth from `TestCase.expected`.

So conceptually:

```python
calculate_metrics(
    grades,
    references,
    metric_config,
)
```

rather than pretending every metric is:

```python
metric(grades)
```

This is important.

### 4. Keep these APIs persistence-free

The pure runtime should work entirely in memory:

```text
TestCase[]
    ↓
infer
    ↓
ExecutionRecord[]
    ↓
grade
    ↓
GradeRecord[]
    ↓
metrics
    ↓
MetricResult[]
```

No:

```text
filesystem lookup
run selection
run_id
serialization
latest-run logic
```

inside these functions.

That gives us a testable computational core.

---

### 5. Then design persistence + run models

Only now introduce:

```text
InferenceRun
GradingRun
MetricRun
```

This layer owns:

```text
run_id
source context / namespace
parent-run relationships
configuration
provenance
serialization
filesystem layout
selection of persisted runs
```

This is also where our source-ID decision becomes concrete.

For example, conceptually:

```text
InferenceRun
source:
  type: dataset
  path: components/router/datasets/tool-selection
```

Then:

```text
source_id = ambiguous-request-001
```

is perfectly sufficient.

No need to turn it into:

```text
router/tool-selection/dataset-x/ambiguous-request-001
```

inside every execution record.

### 6. Implement the complete shared runtime

After interfaces + persistence are settled:

```text
inference
grading
metrics
persistence
run models
```

Then framework-level tests:

```text
TestCase[]
    ↓
FakeExecutor
    ↓
ExecutionRecord[]
    ↓ persist/reload
    ↓
Deterministic FakeGrader
    ↓
GradeRecord[]
    ↓ persist/reload
    ↓
Metric
    ↓
MetricResult
```

Also prove independently:

```text
reuse executions → new grader
reuse grades → new metric
```

At this point we should have a working evaluation engine **without any real component**.

That is a major architecture milestone.

---

# Phase C — Build the remaining skills around the runtime

### 7. `evals-component-execution`

Only now design the component adapter skill.

Its job becomes extremely narrow:

```text
generic Executor contract
        +
real repository component
        ↓
component-specific adapter
```

Conceptually:

```python
async def execute(
    input: dict[str, Any],
) -> ExecutionArtifact:
    ...
```

It owns:

```text
component construction
dependency injection
input mapping
output normalization
trace / observable normalization
error normalization
```

And absolutely nothing about:

```text
TestCase.expected
grader
metric
criterion quality
```

Because the generic inference runtime already works, we can test the adapter independently.

---

### 8. `evals-component-integration`

Once all pieces exist:

```text
dataset
grader
metric selection
executor
runtime
persistence
```

integration only wires them.

This is where we settle:

```text
manifest/config
registrations
evaluation entrypoint
runtime configuration
persistence configuration
integration validation
```

No new semantics.

---

### 9. `evals-orchestrator`

Last.

By then the orchestrator doesn't need architectural intelligence.

It only needs to understand completion dependencies:

```text
project-init
↓
component-analysis
↓
criteria-discovery
↓
criterion-design
├─ criterion-implementation
└─ dataset-authoring
↓
component-execution
↓
component-integration
↓
READY
```

Its job becomes:

```text
inspect
→ identify missing stage
→ route
→ resume
→ verify ready
```

Exactly what we want.

---

## One additional architectural question to defer until runtime implementation

Right now the reusable framework source lives under:

```text
evals-criterion-implementation/code/framework/
```

and that skill installs it into:

```text
evals/framework/
```

Once `evals/framework/` also contains inference, persistence, and run models, we should decide where the **canonical bundled framework source** lives in the skills repository.

I would **not solve this now**. It doesn't block the data model or API design. But we should solve it before implementing Phase B step 6 so we don't accidentally create several copies of the framework.

---

## Therefore our immediate sequence

```text
NOW

1. Finalize ExecutionRecord / GradeRecord
   ├─ source_id semantics
   ├─ ID scope
   ├─ input persistence
   └─ case_id migration

2. Update shared models + affected metrics/tests

3. Design pure runtime API
   ├─ infer
   ├─ grade
   └─ calculate_metrics

4. Design run/persistence layer

5. Implement + test complete shared runtime

THEN

6. evals-component-execution
7. evals-component-integration
8. evals-orchestrator
```

I would start the next discussion specifically with **`source_id` and `ExecutionRecord`**, because that decision propagates into almost everything that follows.
