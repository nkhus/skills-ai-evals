# Output Contract

## Canonical completion artifact

`evals/components/{component}/spec/criteria.yaml`

Required structure:

```yaml
component: component_name
criteria:
  - id: criterion_id
    name: Human-readable criterion name
    group: basic
    priority: p0
    intent: >
      High-level description of the behavior to evaluate and why it matters.
```

Optional criterion field:

```yaml
    out_of_scope:
      - Closely related behavior intentionally excluded from this criterion.
```

## YAML rules

- `component` must match the requested component identifier.
- `criteria` must preserve the user-approved order.
- criterion IDs must be unique lowercase snake_case strings.
- `group` must be `basic` or `quality`.
- `priority` must be `p0`, `p1`, or `p2`.
- `intent` must describe behavior and value, not measurement implementation.
- do not add grader, metric, dataset, threshold, prompt, or rubric fields.
- do not include rejected or deferred candidates in `criteria`.

## Human-readable overview

`evals/components/{component}/spec/README.md`

It must include:

1. component and stage purpose;
2. the approved criteria table;
3. a short description of each criterion;
4. validation checks identified during discovery;
5. operational measurements identified during discovery;
6. deferred, merged, rejected, and out-of-scope candidates when applicable;
7. unresolved questions relevant to later stages.

The README and YAML must describe the same approved criterion list.

## Working draft

`evals/components/{component}/criteria-discovery.draft.md`

The draft may include statuses and discussion notes. It is not a pipeline
completion artifact.

Recommended statuses:

- `proposed`;
- `needs_clarification`;
- `approved`;
- `merged`;
- `rejected`;
- `deferred`;
- `validation_check`;
- `operational_measurement`;
- `out_of_scope`.

## Completion semantics

Do not create the canonical YAML until the user explicitly approves the entire
list.

Once approved:

- render the YAML from the approved items;
- render the README from the same source list;
- remove the draft or add a clear superseded notice;
- report both final paths.
