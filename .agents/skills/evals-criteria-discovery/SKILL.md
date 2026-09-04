---
name: evals-criteria-discovery
description: Identify and approve the behavioral evaluation criteria for an analyzed component.
user-invocable: false
---

# Evals Criteria Discovery

## Purpose

Produce the approved evaluation-criteria list for a component.

## Input

```text
Component: {component}
```

## Requires

```text
evals/components/{component}/README.md
```

The component analysis must have:

```text
Status: Approved
```

## Workflow

1. Read the approved component analysis.
2. Read `references/criteria-guide.md`.
3. Derive candidate criteria from the component analysis and concerns already provided by the user.
4. Refine the list using the criteria guide.
5. Present the complete list and iterate until the user approves it.
6. Create or update:

```text
evals/components/{component}/spec/criteria.yaml
```

using:

```yaml
status: pending_approval
criteria:
  - id: criterion_id
    intent: What component behavior this criterion evaluates.
    boundary: Optional clarification when needed.
```

Omit `boundary` when unnecessary.

7. After explicit approval, change:

```yaml
status: pending_approval
```

to:

```yaml
status: approved
```

## Boundary

Do not modify the approved component analysis or perform criterion design or implementation.
