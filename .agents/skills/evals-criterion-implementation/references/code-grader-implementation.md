# Code-based grader implementation

## Use when

Use criterion-specific code when the approved measurement can be computed deterministically from documented record and artifact fields.

Common patterns:

- exact or normalized comparison;
- set precision, recall, or overlap;
- ranking metrics;
- numeric distance or tolerance;
- required-information coverage;
- expected action or trajectory comparison;
- deterministic constraint satisfaction.

## Contract

The grader must declare:

- criterion ID;
- grader version;
- required configuration;
- required record fields;
- required execution-artifact fields.

It receives the complete dataset record and execution artifact and returns the repository's shared `Grade` contract.

## Behavior

The grader must:

- measure exactly one criterion;
- preserve the approved score range and direction;
- provide concise rationale;
- expose raw comparison evidence;
- distinguish partial success when the metric supports it;
- distinguish invalid records and artifacts from quality failures;
- remain independent from suite thresholds and release policy;
- avoid invoking or mutating the component.

Recommended statuses:

```text
scored
not_applicable
invalid_record
invalid_artifact
grader_error
```

## Evidence

Evidence should make the score reproducible. Examples:

- expected, actual, matched, and missing IDs;
- rank positions;
- numeric difference and tolerance;
- covered and missing required items;
- expected and observed actions.

## Errors

Do not return a score of zero when:

- a required field is missing;
- the dataset record is malformed;
- the artifact is malformed;
- the grader raises an infrastructure error.

Return the matching non-scored status instead.

## Template

Use `templates/code-grader.py` only as a conceptual baseline. Adapt it to the repository's actual Grade and protocol types.
