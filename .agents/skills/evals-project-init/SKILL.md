---
name: evals-project-init
description: Initialize the minimal repository structure and configuration required by the component evaluation pipeline.
user-invocable: false
---

# Evals Project Init

## Goal

Create the shared evaluation project foundation required by all later pipeline stages.

This stage creates only repository-level evaluation structure and configuration. It does not create any component-specific evaluation content.

## Completion artifact

The stage is complete when this file exists:

```text
evals/config.yaml
```

Create the completion artifact only as part of a complete initialization of the target layout below.

## Target layout

```text
evals/
├── README.md
├── config.yaml
├── components/
│   └── .gitkeep
├── e2e/
│   └── .gitkeep
├── suites/
│   └── local.yaml
├── policies/
│   └── default.yaml
└── runs/
    └── .gitignore
```

## Required behavior

1. Work from the repository root.
2. Inspect any existing `evals/` directory before making changes.
3. If the complete target already exists, make no unnecessary edits and report the stage complete.
4. If the target is partially initialized, create only missing files and directories.
5. Preserve existing compatible content.
6. Do not overwrite a conflicting non-empty file without explicit user approval.
7. Do not create component directories or component-specific manifests.
8. Do not invoke models, services, graders, or evaluation runs.

## File targets

### `evals/README.md`

```markdown
# Evaluations

This directory contains component and end-to-end evaluations for the repository.

## Structure

- `components/` contains evaluations for individual components.
- `e2e/` contains evaluations for complete workflows.
- `suites/` selects evaluations and dataset groups for execution.
- `policies/` defines how aggregated evaluation results are interpreted.
- `runs/` contains generated execution artifacts and reports.

## Evaluation model

A component evaluation links:

- a component runner;
- one or more behavioral criteria;
- criterion-owned datasets;
- one grader per criterion;
- suite and policy configuration.

Component evaluations are created through the dedicated eval pipeline stages.
```

### `evals/config.yaml`

```yaml
version: 1

components: {}

e2e: {}

suites:
  local: suites/local.yaml

policies:
  default: policies/default.yaml
```

### `evals/suites/local.yaml`

```yaml
name: local

selection:
  components: []
  criteria: []
  dataset_groups:
    - baseline

policy: default
```

### `evals/policies/default.yaml`

```yaml
name: default

gates: []
```

### `evals/runs/.gitignore`

```gitignore
*
!.gitignore
```

### Empty directories

Create these placeholder files so the target directories can be committed:

```text
evals/components/.gitkeep
evals/e2e/.gitkeep
```

## Existing-layout handling

### No `evals/` directory

Create the complete target layout.

### Partial compatible layout

Create the missing target files and directories. Keep existing content unchanged.

### Existing `evals/config.yaml`

Treat the project as initialized. Add only clearly missing compatible structural files when doing so does not overwrite user-owned content.

### Conflicting file

A conflict exists when a required target path already contains incompatible content and completing initialization would require replacing it.

Stop and ask the user whether to preserve the existing file or replace it. Ask one focused question and name the conflicting path.

## Stage boundary

Do not perform any of the following:

- inspect or document a specific application component;
- create `evals/components/{component}/README.md`;
- define Basic or Quality criteria;
- design metrics or graders;
- create datasets;
- create component runners or manifests;
- register a component in a suite;
- run evaluations.

Those responsibilities belong to later pipeline stages.

## Completion response

When complete, report:

```text
COMPLETE

Produced or confirmed:
- evals/README.md
- evals/config.yaml
- evals/components/.gitkeep
- evals/e2e/.gitkeep
- evals/suites/local.yaml
- evals/policies/default.yaml
- evals/runs/.gitignore
```

When user input is required, report:

```text
NEEDS_USER_INPUT

Question:
<one focused question>
```

When blocked by repository access or another hard prerequisite, report:

```text
BLOCKED

Reason:
<short explanation>
```
