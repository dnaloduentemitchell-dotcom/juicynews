from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MLSignal:
    direction: str
    confidence: float


def predict_with_ml(text: str) -> MLSignal | None:
    return None
