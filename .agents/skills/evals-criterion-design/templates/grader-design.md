# {Criterion Name} Grader Design

- Component: `{component}`
- Criterion ID: `{criterion_id}`
- Criterion specification: `evals/components/{component}/spec/{criterion_id}.md`
- Dataset contract: `evals/components/{component}/datasets/{criterion_id}/README.md`
- Design version: `1`

## Grader Family

`{code_based | llm_based | hybrid}`

## Design Pattern

{predicate_exact_set_ranking_numeric_coverage_trajectory_rubric_pairwise_grounding_or_hybrid_pattern}

## Why This Design Fits the Criterion

{relationship_between_semantic_contract_available_evidence_and_grader_choice}

## Inputs

### Dataset Record

The grader reads:

- `record.expected.{field}` — {meaning}
- `record.input.{field}` — {meaning when required for interpretation}

### Execution Artifact

The grader requires:

- `artifact.{field}` — {meaning}

### Configuration

{configuration_fields_or_none}

## Output Contract

The grader returns:

- criterion ID;
- status;
- primary score or label;
- supporting metrics;
- rationale;
- evidence;
- grader version.

Supported statuses:

- `scored`;
- `not_applicable`;
- `invalid_record`;
- `invalid_artifact`;
- `grader_error`.

## Record-Level Score Calculation

{exact_formula_algorithm_or_rubric_mapping}

## Supporting Metrics

{supporting_metric_calculation_or_none}

## Labels

{labels_and_meanings_or_none}

## Rationale Requirements

{what_the_rationale_must_explain}

## Evidence Requirements

{structured_debugging_evidence}

## Invalid Record Handling

{conditions_and_status}

## Invalid Artifact Handling

{conditions_and_status}

## Grader Error Handling

{timeouts_parse_failures_retries_and_status}

## Not-Applicable Behavior

{explicit_semantic_conditions}

## Model-Based Rubric

{rubric_dimensions_labels_prompt_contract_and_structured_output_or_not_applicable}

Remove this section when the grader is fully code-based.

## Calibration and Validation

{fixed_examples_human_reviewed_calibration_borderline_cases_and_agreement_checks}

## Determinism and Variability

{determinism_expected_variance_and_repeat_strategy}

## Versioning

{changes_that_require_a_new_grader_version}

## Known Limitations

{known_false_positive_false_negative_bias_and_observability_limitations}

## Implementation Notes

{non_binding_guidance_for_the_implementation_agent}
