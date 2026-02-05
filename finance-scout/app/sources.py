from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from app.config import settings


@dataclass
class SourceConfig:
    name: str
    kind: str
    url: str
    refresh_minutes: int
    weight: float
    enabled: bool = True


def load_sources(path: str | Path | None = None) -> list[SourceConfig]:
    if path is None:
        path = settings.sources_path
    data: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    sources: list[SourceConfig] = []
    for entry in data.get("sources", []):
        sources.append(
            SourceConfig(
                name=entry["name"],
                kind=entry["kind"],
                url=entry["url"],
                refresh_minutes=int(entry.get("refresh_minutes", 5)),
                weight=float(entry.get("weight", 1.0)),
                enabled=bool(entry.get("enabled", True)),
            )
        )
    return sources
