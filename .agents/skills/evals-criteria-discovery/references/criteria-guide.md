# Evaluation Criteria Guide

An evaluation criterion is one independently meaningful dimension of an AI component's behavior that should be assessed across representative scenarios.

Derive criteria from the approved component analysis. The patterns below are guidance, not a checklist.

## Common patterns

Use only patterns owned by the component, for example:

- selection or decision correctness — choosing the appropriate tool, route, action, source, or strategy;
- output correctness — producing behavior consistent with the component contract and available information;
- relevance — selecting or producing information useful for the task;
- completeness — covering information or actions the component is responsible for;
- constraint adherence — respecting behavioral rules and restrictions;
- groundedness — basing decisions or outputs on available evidence;
- context handling — using relevant conversation, workflow, or state correctly;
- ambiguity handling — behaving appropriately when several interpretations are plausible;
- failure recovery — responding appropriately to failed, unavailable, or partial dependencies;
- consistency — avoiding unjustified differences across equivalent situations;
- ranking quality — ordering alternatives appropriately when ranking is part of the component responsibility.

## Evaluation criteria vs classical testing

The distinction is not whether the check is deterministic.

An evaluation criterion measures behavioral performance across scenarios. Classical testing validates software or integration contracts.

For example, `tool_selection` may use exact expected values and a deterministic grader and still be an evaluation criterion.

These normally belong to classical testing or validation instead:

- schema validity;
- import or build correctness;
- configuration presence;
- type contracts;
- endpoint availability;
- dependency wiring;
- manifest or file-path validity.

Do not promote implementation checks into evaluation criteria merely because the component contains an LLM.

## Criteria are not measurements

A criterion states what behavior matters, not how it will be scored.

Prefer:

```text
tool_selection
retrieval_relevance
failure_recovery
```

Avoid:

```text
tool_selection_accuracy
ndcg_score
llm_judge_relevance
exact_match_tool_choice
```

Metrics, score ranges, aggregation, and grader choice belong to criterion design.

## Criteria are not scenarios

A scenario is a condition under which behavior is evaluated.

Examples:

```text
ambiguous_request
tool_timeout
missing_context
```

Related criteria might be:

```text
ambiguity_handling
failure_recovery
context_handling
```

A criterion should normally apply across multiple scenarios.

## Decomposition

A criterion should:

- represent one behavioral dimension;
- be owned by the component;
- matter independently;
- avoid substantial overlap with another criterion;
- remain independent of its future measurement implementation.

Split criteria that combine distinct behaviors. Merge criteria that describe the same behavior under different names. Reject criteria that belong to another component or describe implementation mechanics.

## Boundaries

Add `boundary` only when needed to prevent overlap or clarify ownership.

Example:

```yaml
- id: tool_selection
  intent: Select the appropriate tool for the request.
  boundary: Does not evaluate correctness of arguments passed to the selected tool.
```

Omit it when the intent is already unambiguous.
