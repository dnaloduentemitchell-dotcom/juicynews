from __future__ import annotations

NEGATIVE_TERMS = ["fall", "drops", "decline", "recession", "panic", "slump"]
POSITIVE_TERMS = ["rise", "gain", "growth", "surge", "boom", "rally"]


def simple_sentiment(text: str) -> float:
    lowered = text.lower()
    score = 0
    for term in POSITIVE_TERMS:
        if term in lowered:
            score += 1
    for term in NEGATIVE_TERMS:
        if term in lowered:
            score -= 1
    if score == 0:
        return 0.0
    return max(-1.0, min(1.0, score / 3))
