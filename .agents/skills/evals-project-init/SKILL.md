---
name: evals-project-init
description: Validate or initialize the repository eval workspace.
user-invocable: false
---

# Evals Project Init

## Purpose

Ensure the repository has a valid `evals/` workspace.

## Workflow

1. Inspect `evals/`.
2. Ensure this structure exists:

```text
evals/
├── README.md
├── config.yaml
└── components/
```

3. Create missing compatible files or directories.
4. Preserve existing content.
5. Validate `evals/config.yaml` contains:
   - `version: 1`;
   - a `components` mapping.

Minimal config:

```yaml
version: 1
components: {}
```

If existing content is incompatible with this structure or config contract, ask the user before changing it.

## Boundary

Do not introduce execution, persistence, suite, or run architecture.
Continuation/resume behavior belongs to a future orchestrator, not this skill.
