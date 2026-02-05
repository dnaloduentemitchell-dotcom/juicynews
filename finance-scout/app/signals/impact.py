from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from app.nlp.classify_event import classify_event
from app.nlp.entity_extract import extract_entities
from app.signals.rules import apply_rules


@dataclass
class ImpactSignal:
    id: str
    impact_direction: str
    impact_confidence: int
    horizon: str
    rationale: list[str]
    entities: dict[str, list[str]]
    event_types: list[str]


def build_impact_signal(text: str) -> ImpactSignal:
    rules = apply_rules(text)
    score = sum(rule.score for rule in rules)
    if score > 0.15:
        direction = "UP"
    elif score < -0.15:
        direction = "DOWN"
    else:
        direction = "MIXED"

    confidence = int(min(100, max(10, abs(score) * 100)))
    horizon = "INTRADAY" if abs(score) > 0.4 else "1-3D"
    rationale = [rule.rationale for rule in rules]
    if not rationale:
        rationale = ["Limited direct macro/market cues; signal is uncertain."]

    entities = extract_entities(text)
    event_types = classify_event(text)

    return ImpactSignal(
        id=str(uuid.uuid4()),
        impact_direction=direction,
        impact_confidence=confidence,
        horizon=horizon,
        rationale=rationale,
        entities=entities,
        event_types=event_types,
    )


def signal_to_record(article_id: str, signal: ImpactSignal) -> dict:
    return {
        "id": signal.id,
        "article_id": article_id,
        "cluster_id": None,
        "impact_direction": signal.impact_direction,
        "impact_confidence": signal.impact_confidence,
        "horizon": signal.horizon,
        "rationale": signal.rationale,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
