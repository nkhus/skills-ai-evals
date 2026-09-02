# Criterion Detailing

## Purpose

Convert one approved high-level criterion intent into a precise behavioral
contract that can be measured without changing what the user approved.

## Start from behavior, not implementation

A criterion describes a quality of component behavior. It is not:

- a function name;
- a prompt implementation detail;
- a grader algorithm;
- an output schema check;
- a runtime-health check;
- a release threshold.

Prefer:

> Does the router select the action needed to satisfy the request?

Over:

> Does `select_tool()` return a valid enum?

The second statement may be an implementation check. It does not fully describe
the behavioral quality.

## Required semantic elements

### Purpose

Explain why measuring this behavior is valuable. Tie it to the component's real
functional goal and downstream consequences.

### Evaluation question

Write one question that a grader can answer for each dataset record.

A strong evaluation question:

- addresses one quality dimension;
- is answerable from the dataset record and execution artifact;
- does not embed a grader implementation;
- does not combine success, latency, formatting, and safety into one question.

### Component responsibility

Explain why this component owns the behavior. Distinguish responsibilities of
upstream and downstream components.

### Desired behavior

Describe observable successful behavior, including when several outputs may be
acceptable.

### Undesired behavior

Describe meaningful failure, not merely an invalid file or crashed runner.

### Acceptable variability

State which output differences do not represent quality differences. This is
especially important for generative or agentic behavior.

### Out of scope

Name adjacent behaviors deliberately excluded. This prevents grader prompts and
datasets from expanding into other criteria.

### Applicability

Define when the criterion applies to a record and when a record may be
`not_applicable`.

Avoid using `not_applicable` to hide difficult failures. It should represent a
real semantic mismatch between a record and criterion.

### Failure modes

Include:

- common failures;
- subtle failures;
- high-consequence failures;
- plausible false positives and false negatives in grading.

### Edge cases

Describe situations that change how success should be interpreted, such as:

- ambiguity;
- missing information;
- multiple valid actions;
- conflicting evidence;
- no-action-required scenarios;
- partial completion;
- fallback or escalation behavior.

## Detect overloaded criteria

A criterion is probably overloaded when:

- it requires multiple unrelated evaluation questions;
- one score can be high while another essential behavior is catastrophically
  wrong;
- different datasets or grader families are needed for unrelated behaviors;
- the name contains several independent nouns joined by “and”.

When overloaded, recommend returning to criteria discovery to split it.

## Detect duplicate criteria

Compare only the brief approved definitions of neighboring criteria. A criterion
is probably duplicated when both would use essentially the same evaluation
question, expected behavior, records, and score interpretation.

Do not merge or edit the criteria list yourself. Report the issue and return to
discovery.

## Traceability

The final criterion specification should make the chain explicit:

```text
component functional goal
    → owned behavior
    → evaluation question
    → dataset evidence
    → grader measurement
```
