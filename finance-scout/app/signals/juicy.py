from __future__ import annotations

from dataclasses import dataclass


@dataclass
class JuicyScore:
    score: float
    novelty: float
    urgency: float
    magnitude: float


def compute_juicy_score(novelty: float, urgency: float, magnitude: float) -> JuicyScore:
    score = 0.4 * novelty + 0.3 * urgency + 0.3 * magnitude
    return JuicyScore(score=score, novelty=novelty, urgency=urgency, magnitude=magnitude)
