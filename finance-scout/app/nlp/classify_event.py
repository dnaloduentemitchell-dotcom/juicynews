from __future__ import annotations

EVENT_TYPES = {
    "Fed/ECB/BoE/BoJ policy": ["rate", "hike", "cut", "meeting", "press conference"],
    "Inflation/CPI/PPI": ["inflation", "cpi", "ppi", "prices"],
    "Jobs/NFP": ["jobs", "employment", "nfp", "unemployment"],
    "Geopolitical risk": ["war", "conflict", "sanctions", "attack"],
    "Energy shock": ["oil", "opec", "supply", "gas"],
    "Risk-on/off": ["risk-off", "risk on", "safe haven"],
    "USD strength": ["dollar", "usd", "greenback"],
}


def classify_event(text: str) -> list[str]:
    lowered = text.lower()
    labels = []
    for label, terms in EVENT_TYPES.items():
        if any(term in lowered for term in terms):
            labels.append(label)
    return labels
