from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def save_run(run: BaseModel, directory: Path) -> Path:
    run_id = getattr(run, "run_id")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{run_id}.json"
    path.write_text(run.model_dump_json(indent=2))
    return path


def load_run(model: type[T], path: Path) -> T:
    return model.model_validate_json(path.read_text())


def list_runs(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    # run_id filenames are timestamp-prefixed, so lexical sort is chronological
    return sorted(directory.glob("*.json"))


def latest_run(model: type[T], directory: Path) -> T | None:
    paths = list_runs(directory)
    if not paths:
        return None
    return load_run(model, paths[-1])
