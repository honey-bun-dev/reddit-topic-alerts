from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


def load_json(path: str | Path, default: T) -> T:
    file_path = Path(path)
    if not file_path.exists():
        return default

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: str | Path, data: Any) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_seen_posts(path: str | Path) -> set[str]:
    data = load_json(path, default=[])
    if not isinstance(data, list):
        return set()
    return {str(post_id) for post_id in data}


def save_seen_posts(path: str | Path, seen_ids: set[str]) -> None:
    save_json(path, sorted(seen_ids))
