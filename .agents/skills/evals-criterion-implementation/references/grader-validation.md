# Grader validation

## Purpose

Validate the grader as software without conflating validation fixtures with the evaluation dataset.

Store fixtures at:

```text
evals/components/{component}/grader-validation/{criterion_id}.jsonl
```

## Fixture shape

Each fixture contains:

```json
{
  "id": "fixture-id",
  "record": {
    "id": "record-id",
    "input": {},
    "expected": {}
  },
  "artifact": {},
  "expected_grade": {}
}
```

## Code-based grader coverage

Include as applicable:

- ideal behavior;
- clear failure;
- partial success;
- boundary score;
- malformed record;
- malformed artifact;
- not-applicable case;
- important metric edge cases.

Expected scores may be exact for deterministic graders.

## LLM prompt grader coverage

Validate two layers separately where practical.

### Structural validation

Without calling a provider, validate:

- definition imports;
- Pydantic schema constraints;
- prompt variables resolve;
- prompt and schema are colocated;
- definition exposes the expected entry point;
- conversion to Grade preserves fields;
- malformed structured responses map correctly.

### Semantic calibration fixtures

Provide representative fixed records and artifacts with acceptable outcomes:

- expected label;
- minimum and maximum acceptable score;
- required evidence concepts where useful.

Do not require an exact score from a nondeterministic judge.

The implementation stage should not run external judge calls unless the user explicitly requests calibration execution and the surrounding eval framework supports it.

## Completion status

The implementation handoff records which checks ran and their result. Do not mark validation as passed when commands were unavailable or skipped; record a truthful status such as `not_run` with the reason.
