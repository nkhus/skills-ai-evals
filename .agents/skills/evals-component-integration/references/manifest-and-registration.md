# Manifest and Registration

## Component manifest

Create:

```text
evals/components/{component}/manifest.yaml
```

Build it from approved and implemented artifacts. Do not use filename matching as the linking mechanism.

## Required manifest concepts

The manifest should identify:

- component name and manifest version;
- runner implementation;
- runner factory or assembly mechanism when required;
- every approved criterion;
- criterion group and priority;
- criterion specification path;
- named dataset groups and paths;
- default dataset groups;
- grader family;
- grader implementation or generic runtime;
- LLM criterion definition object when applicable;
- grader version and configuration.

## Criterion linkage

For a code-based grader:

```yaml
criterion_id:
  group: basic
  priority: p0
  spec: spec/criterion_id.md
  datasets:
    baseline:
      - datasets/criterion_id/baseline.jsonl
  default_datasets:
    - baseline
  grader:
    family: code
    implementation: graders.criterion_id:CriterionGrader
    version: "1"
```

For an LLM prompt grader:

```yaml
criterion_id:
  group: quality
  priority: p1
  spec: spec/criterion_id.md
  datasets:
    baseline:
      - datasets/criterion_id/baseline.jsonl
  default_datasets:
    - baseline
  grader:
    family: llm_prompt
    implementation: shared.graders.prompt_grader:PromptGrader
    definition: graders.criterion_id:definition
    version: "1"
```

The criterion-specific LLM module owns its prompt and Pydantic response schema. The generic runtime owns model invocation, rendering, retries, telemetry, parsing, and dependency injection.

## Shared prompt grader requirement

Do not create the generic `PromptGrader` during integration.

Require the shared runtime declared by the handoff, normally:

```text
evals/shared/graders/prompt_grader.py
```

If missing, return `BLOCKED` and direct the user to initialize or update the eval framework.

## Root registration

Update:

```text
evals/config.yaml
```

Preferred form:

```yaml
components:
  component_name:
    manifest: components/component_name/manifest.yaml
```

Preserve unrelated mappings and comments where the editing tool permits.

If the component name already points to a different manifest, do not overwrite it silently.

## Suite registration

An existing local suite may select the newly integrated component for baseline execution.

Preferred intent:

```yaml
selection:
  components:
    - component_name
  priorities:
    - p0
  dataset_groups:
    - baseline
```

Do not assume every repository uses this exact suite schema. Follow existing conventions.

Do not automatically update:

- pull-request suites;
- release suites;
- production suites;
- security gates;
- schedules or workflows.

Those changes may materially alter CI or release behavior and require explicit user intent.

## Non-destructive editing

When modifying YAML:

- preserve existing components and suite selections;
- avoid replacing the whole file with a minimal template;
- do not reorder unrelated configuration unnecessarily;
- detect duplicate entries;
- report conflicts.

## Draft publishing

Build and validate:

```text
manifest.draft.yaml
```

Publish it as `manifest.yaml` only after required checks pass.

If an incompatible `manifest.yaml` already exists, preserve it and present the draft for user review.
