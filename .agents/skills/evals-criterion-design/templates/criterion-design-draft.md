# Criterion Design Draft: {criterion_name}

- Component: `{component}`
- Criterion ID: `{criterion_id}`
- Discovery group: `{basic_or_quality}`
- Priority: `{p0_or_p1_or_p2}`
- Status: `draft`

## Approved Discovery Intent

{intent_from_criteria_yaml}

## Current Interpretation

{current_interpretation}

## Semantic Contract

### Purpose

{why_this_criterion_matters}

### Evaluation Question

{one_record_level_question}

### Component Responsibility

{why_the_component_owns_this_behavior}

### Desired Behavior

{desired_behavior}

### Undesired Behavior

{undesired_behavior}

### Acceptable Variability

{acceptable_variability}

### Out of Scope

{out_of_scope}

### Applicability

{applicable_and_not_applicable_cases}

### Failure Modes and Edge Cases

{failure_modes_and_edge_cases}

## Measurement Proposal

### Primary Metric

{primary_metric}

### Supporting Metrics

{supporting_metrics}

### Diagnostics

{diagnostics}

### Record-Level Scoring

{record_level_scoring}

### Dataset-Level Aggregation

{aggregation}

### Interpretation and Limitations

{interpretation_and_limitations}

## Dataset Proposal

### Record Envelope

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

### Input Contract

{input_fields}

### Expected Contract

{expected_fields}

### Dataset Groups

{dataset_groups}

### Required Scenario Categories

{scenario_categories}

### Invalid Record Examples

{invalid_records}

## Grader Proposal

### Family and Pattern

{grader_family_and_pattern}

### Inputs

{grader_inputs}

### Required Execution Artifact Fields

{artifact_fields}

### Output and Score Calculation

{grader_output_and_calculation}

### Rationale and Evidence

{rationale_and_evidence}

### Error and Not-Applicable Behavior

{error_and_na_behavior}

### Calibration, Versioning, and Limitations

{calibration_versioning_limitations}

## Open Questions

{open_questions}

## User Decisions

{approved_decisions_so_far}

## Approval Status

Not yet approved. Final artifacts must not be written until the user explicitly
approves the complete design.
