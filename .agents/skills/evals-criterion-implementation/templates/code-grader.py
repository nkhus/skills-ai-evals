from __future__ import annotations

from typing import Any, Mapping

# Replace these imports with the repository's shared contracts.
from evals.shared.schemas import Grade


class CriterionGrader:
    criterion = "{criterion_id}"
    version = "1"

    async def grade(
        self,
        *,
        record: Mapping[str, Any],
        artifact: Mapping[str, Any],
        config: Mapping[str, Any],
    ) -> Grade:
        """Measure exactly one approved criterion."""
        raise NotImplementedError
