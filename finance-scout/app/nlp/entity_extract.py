from __future__ import annotations

KEYWORDS = {
    "central_banks": ["fed", "federal reserve", "ecb", "boe", "boj", "pboc"],
    "macro": ["inflation", "cpi", "ppi", "jobs", "nfp", "gdp", "rates"],
    "geo": ["war", "conflict", "sanctions", "missile", "attack", "geopolitical"],
    "commodities": ["gold", "silver", "oil", "wti", "brent", "copper", "natural gas"],
    "risk": ["risk-off", "risk on", "safe haven", "volatility", "vix"],
}


def extract_entities(text: str) -> dict[str, list[str]]:
    lowered = text.lower()
    found: dict[str, list[str]] = {}
    for group, terms in KEYWORDS.items():
        hits = [term for term in terms if term in lowered]
        if hits:
            found[group] = hits
    return found
