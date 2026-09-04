# LLM Grader Implementation Guide

Assumes the common rules in `grader-implementation.md` are already known.

## Shape

```text
criterion-specific focused prompt (injected at grader init)
+
criterion-specific Pydantic response model with a required reasoning field
+
injected LLMClient
+
one structured generation call
+
response → Grade mapping
```

Example:

```python
class RelevanceGrader:
    def __init__(self, llm: LLMClient, prompt: str):
        self.llm = llm
        self.prompt = prompt

    async def grade(self, case: TestCase, artifact: ExecutionArtifact) -> Grade:
        ...
```

## Rules

- inject `evals.framework.LLMClient`; do not instantiate provider SDK clients;
- inject the judge prompt (template) as a constructor variable; do not hardcode it inside `grade()`;
- do not embed credentials; provider/model selection belongs to the `LLMClient` implementation, not the grader;
- use one focused prompt for one atomic judgment;
- use one criterion-specific structured response model; it must always declare a `reasoning` field explaining the decision;
- always populate `Grade.reasoning` from the response model's `reasoning` field;
- use one LLM call by default;
- implement the approved deterministic label → value mapping, if any, in grader code — not in the prompt;
- map LLM/runtime failures (including invalid/unparseable structured output) to `error`;
- do not create multi-agent pipelines, multi-step judge workflows, sub-graders, self-reflection loops, majority-vote judging, or multi-agent debates unless explicitly required by the approved design.

## Boundary

The criterion-specific LLM grader owns the prompt, response model, and response-to-`Grade` mapping only. It does not own provider integration, model selection, or structured-output invocation mechanics — those belong to the `LLMClient` implementation, which is outside this skill.
