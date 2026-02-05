from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuleResult:
    rule: str
    score: float
    rationale: str


RULES = [
    (
        "hawkish_rates",
        ["rate hike", "hawkish", "higher yields", "tightening"],
        -0.4,
        "Higher real yields tend to pressure gold and silver.",
    ),
    (
        "usd_strength",
        ["usd", "dollar strength", "greenback"],
        -0.3,
        "Stronger USD often weighs on precious metals.",
    ),
    (
        "geopolitical_risk",
        ["war", "conflict", "attack", "sanctions"],
        0.5,
        "Geopolitical risk can boost safe-haven demand.",
    ),
    (
        "inflation_surprise",
        ["inflation", "cpi", "prices", "ppi"],
        0.3,
        "Inflation surprises can lift hedge demand if policy response is unclear.",
    ),
]


def apply_rules(text: str) -> list[RuleResult]:
    lowered = text.lower()
    results = []
    for name, terms, score, rationale in RULES:
        if any(term in lowered for term in terms):
            results.append(RuleResult(rule=name, score=score, rationale=rationale))
    return results
