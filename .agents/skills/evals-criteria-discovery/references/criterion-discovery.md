# Criterion Discovery and Refinement

## Start from user intent

The user's initial wording is evidence of what matters, not necessarily a final
criterion name.

Translate a request into the behavioral question behind it.

Example:

> It should not call tools randomly.

Possible refinement:

- `tool_selection_correctness`: does it choose the tool required by the request?
- `tool_use_necessity`: does it avoid tool use when no tool is needed?

Split only when the behaviors can fail independently and would lead to different
improvements.

## Criterion qualification

A candidate is a behavioral criterion when all are true:

1. It describes behavior of the component, not the evaluation framework.
2. It is owned or materially controlled by the component.
3. It matters to a user, downstream consumer, or system outcome.
4. It can vary across representative inputs or executions.
5. A later stage could define observable evidence of success.
6. Improving it would represent a meaningful component improvement.

If ownership is partial, state the boundary instead of silently assigning all
responsibility to the component.

## Reclassify non-criteria

### Validation check

Examples:

- manifest paths resolve;
- dataset records have required fields;
- runner returns the artifact schema;
- grader module imports;
- output JSON is syntactically valid when the question is only structural.

A format requirement may support a behavioral criterion when semantic
correctness is involved. For example, `correct structured extraction` is a
criterion; `JSON parses` is a validation check.

### Operational measurement

Examples:

- latency;
- token usage;
- throughput;
- availability;
- retry count;
- cache hit rate.

Record these separately. Do not promote them into behavioral criteria during
this stage.

### Out of scope

Examples:

- answer correctness assigned to a retriever that does not generate answers;
- tool execution reliability assigned to a planner that only selects actions;
- authorization enforcement owned entirely by an upstream gateway.

When ownership is shared, describe the component's exact contribution.

## Avoid implementation-shaped criteria

Weak:

- uses prompt version 3;
- calls function X;
- returns a non-empty string;
- outputs fewer than 500 tokens;
- passes schema validation.

Better:

- selects the action needed to satisfy the request;
- returns the information needed by the downstream consumer;
- gives a concise response without omitting essential information;
- produces semantically correct structured data.

The criterion should survive a change in implementation when the intended
behavior stays the same.

## Avoid overlap

Two candidates overlap when they ask effectively the same behavioral question
and would use the same evidence to drive the same improvement.

Possible actions:

- merge them into one criterion;
- keep one criterion and treat the other as a later metric or diagnostic;
- split them only when failures are independently actionable.

Example:

`answer_quality`, `helpfulness`, and `usefulness` are too vague and likely
overlapping. Refine them into distinct owned behaviors such as `task_completion`
and `essential_information_coverage`, or keep one high-level concept if the user
does not need the distinction.

## Keep discovery high-level

A high-level criterion needs enough detail to preserve intent but not enough to
pre-design its implementation.

Good discovery entry:

```yaml
id: clarification_decision
name: Clarification decision
intent: >
  Evaluate whether the component asks for clarification when the available
  information is insufficient and proceeds directly when it is sufficient.
```

Too detailed for discovery:

```yaml
metric: binary_accuracy
expected:
  should_clarify: true
grader: code_based
threshold: 0.95
```

Those details belong to criterion design.

## Iteration behavior

After each round:

- display the complete current criterion list;
- identify reclassified items separately;
- explain merges and splits briefly;
- ask one focused question when a decision is required;
- do not continue into criterion detail design.
