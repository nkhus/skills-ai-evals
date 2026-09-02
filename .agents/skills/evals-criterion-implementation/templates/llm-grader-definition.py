from __future__ import annotations

from typing import Any, Literal, Mapping

from pydantic import BaseModel, Field

# Replace this import with the repository's shared Grade contract.
from evals.shared.schemas import Grade


class CriterionJudgeResponse(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    label: Literal["pass", "partial", "fail"]
    rationale: str = Field(min_length=1)
    evidence: list[str] = Field(default_factory=list)


class CriterionDefinition:
    criterion = "{criterion_id}"
    version = "1"
    response_model = CriterionJudgeResponse

    prompt_template = """
You evaluate only {criterion_name}.

Evaluation question:
{evaluation_question}

Out of scope:
{out_of_scope}

Component input:
{{{{ input }}}}

Expected evaluation guidance:
{{{{ expected }}}}

Component output:
{{{{ output }}}}

Execution trace, when relevant:
{{{{ trace }}}}

Scoring:
{score_semantics}

Return a structured response matching the provided schema.
Provide a concise rationale and concrete evidence. Do not provide hidden
chain-of-thought or evaluate unrelated quality dimensions.
""".strip()

    def build_variables(
        self,
        *,
        record: Mapping[str, Any],
        artifact: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        return {
            "input": record["input"],
            "expected": record["expected"],
            "output": artifact.get("output"),
            "trace": artifact.get("trace"),
        }

    def to_grade(self, result: CriterionJudgeResponse) -> Grade:
        return Grade(
            criterion=self.criterion,
            score=result.score,
            label=result.label,
            rationale=result.rationale,
            evidence={"items": result.evidence},
            status="scored",
            grader_version=self.version,
        )


definition = CriterionDefinition()
