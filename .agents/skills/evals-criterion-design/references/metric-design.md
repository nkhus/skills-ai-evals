# Metric Design

## Purpose

Define measurements that faithfully represent one approved criterion and remain
interpretable across dataset records and runs.

## Separate four concepts

### Criterion

The behavioral quality being evaluated.

Example:

```text
Retrieval coverage
```

### Primary metric

The main quantitative or categorical representation of the criterion.

Example:

```text
Recall at K
```

### Supporting metrics

Secondary measurements that explain or complement the primary metric without
becoming separate criteria.

Examples:

- full-coverage rate;
- missing-required-item count;
- partial-credit score.

### Diagnostics

Debugging signals that help understand results but do not represent quality by
themselves.

Examples:

- number of returned items;
- duplicate count;
- judge retry count;
- unsupported claim list.

Do not promote every metric or diagnostic into a criterion.

## Record-level metric contract

For every metric define:

- name;
- meaning;
- value type;
- range or allowed labels;
- whether higher or lower is better;
- exact computation or rubric interpretation;
- treatment of partial success;
- treatment of ties;
- `not_applicable` behavior;
- invalid-record behavior;
- invalid-artifact behavior.

Do not convert infrastructure failures into legitimate quality scores.

## Dataset-level aggregation

Define how record-level values are summarized, for example:

- arithmetic mean;
- median;
- percentile;
- success rate;
- macro average;
- micro average;
- pairwise win rate;
- distribution of rubric labels.

Choose aggregation based on meaning, not convenience.

### Macro versus micro

Use macro aggregation when each record or category should contribute equally.
Use micro aggregation when individual units inside records should contribute
proportionally.

Document which is used and why.

### Missing and not-applicable values

Specify whether these values are:

- excluded from the denominator;
- reported separately;
- considered dataset-design defects;
- considered grader failures.

Never silently drop them.

## Score interpretation

Explain what high, medium, and low values mean behaviorally. Avoid definitions
that merely repeat numeric ranges.

Example:

```text
A score of 1 means every required source was present within the first K results.
A score between 0 and 1 means only part of the required evidence was retrieved.
A score of 0 means none of the required evidence was retrieved.
```

## Dataset dependence

Every aggregate is conditional on dataset composition. Document important
sources of distortion:

- overrepresentation of easy examples;
- repeated near-duplicates;
- unbalanced intents or languages;
- missing no-action or unanswerable cases;
- incomplete expected labels;
- judge-friendly references that do not represent production behavior.

## Basic and Quality are not metric types

A `basic` criterion may use partial credit or an LLM judge.

A `quality` criterion may use a deterministic metric.

Choose measurement from the criterion contract and available evidence, not the
high-level group alone.

## Thresholds are out of scope

This stage defines what a score means. It does not decide:

- pass/fail thresholds;
- release gates;
- acceptable regression deltas;
- suite-specific policy.

Those decisions belong to policy and suite configuration.
