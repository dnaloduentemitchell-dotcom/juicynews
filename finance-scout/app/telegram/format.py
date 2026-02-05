from __future__ import annotations

from datetime import datetime


def format_alert(article: dict, signal: dict, impact: dict) -> str:
    published = article.get("published_at") or ""
    try:
        published_dt = datetime.fromisoformat(published)
        published_str = published_dt.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        published_str = published

    rationale = impact.get("rationale", [])
    rationale_lines = "\n".join([f"- {item}" for item in rationale])

    lines = [
        f"*{article.get('title', '')}*",
        f"_{article.get('source', '')}_ · {published_str}",
        "*Why it matters*",
        rationale_lines or "- Limited direct macro/market cues; signal is uncertain.",
        "*Impact Forecast (XAU/XAG)*",
        f"Direction: `{impact.get('impact_direction')}`",
        f"Confidence: `{impact.get('impact_confidence')}`",
        f"Horizon: `{impact.get('horizon')}`",
    ]

    entities = signal.get("entities", {})
    event_types = signal.get("event_types", [])
    if entities or event_types:
        lines.append("*Key drivers*")
        if event_types:
            lines.append(f"Event: {', '.join(event_types)}")
        if entities:
            for group, items in entities.items():
                lines.append(f"{group}: {', '.join(items)}")

    lines.extend(
        [
            f"[Source link]({article.get('url')})",
            "_Not financial advice. Forecasts are uncertain._",
        ]
    )
    return "\n".join(lines)
