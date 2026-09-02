# Basic, Quality, and Priority

## Purpose of the groups

`basic` and `quality` are broad discovery tags. They help the user reason about
coverage without imposing a component-specific taxonomy.

They do not determine:

- grader family;
- dataset shape;
- metric formula;
- execution frequency;
- difficulty or implementation effort.

## Basic

A Basic criterion asks:

> Does the component perform the required behavior correctly?

Typical characteristics:

- the expected decision or result can usually be described clearly;
- a failure often means the component did the wrong thing or omitted a required
  behavior;
- later graders are often code-based, but may be LLM-based or hybrid when the
  expected behavior is semantic.

Possible component-specific examples:

- correct route selection;
- correct tool selection;
- correct extraction;
- required information retrieval;
- appropriate refusal decision;
- appropriate clarification decision;
- required action completion;
- prohibited action avoidance.

Do not include infrastructure checks such as parsing, imports, or file
existence.

## Quality

A Quality criterion asks:

> How well does the component perform the behavior?

Typical characteristics:

- several outputs may be acceptable;
- quality is graded rather than merely matched;
- later graders are often rubric-based, but deterministic or hybrid approaches
  may still be appropriate.

Possible component-specific examples:

- relevance;
- completeness;
- usefulness;
- clarity;
- ranking quality;
- grounding quality;
- contextual appropriateness;
- plan quality;
- recovery quality;
- quality of a clarification question.

Avoid generic labels such as `overall_quality` unless the user intentionally
wants one combined judgment and accepts reduced diagnostic value.

## Suggestion rules

Only suggest additional criteria after the user asks for suggestions.

Suggestions must:

- derive from the approved component analysis;
- be limited to a small number of high-value candidates;
- include both groups only when both are applicable;
- explain why each criterion matters to this component;
- avoid duplicating accepted or rejected candidates;
- avoid forcing every component to have the same list.

## Priority

### P0

Use when failure undermines the primary functional goal or creates a severe
behavioral consequence.

A component normally has a small number of P0 criteria.

### P1

Use for important normal-operation quality, frequent meaningful failures, or a
strong secondary responsibility.

### P2

Use for secondary, uncommon, edge, or exploratory behavior that is useful but
not essential to the first evaluation implementation.

## Priority questions

Ask:

- Would the component still fulfill its main purpose if this criterion were
  consistently poor?
- How severe is failure for users or downstream systems?
- How frequently does the behavior matter?
- Is the behavior a core responsibility or a secondary enhancement?

Do not infer priority from how easy the grader seems to implement.
