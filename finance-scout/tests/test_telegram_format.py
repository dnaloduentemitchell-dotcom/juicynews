from app.telegram.format import format_alert


def test_format_alert_contains_disclaimer() -> None:
    article = {
        "title": "Gold jumps",
        "source": "Test",
        "published_at": "2024-01-01T00:00:00+00:00",
        "url": "https://example.com",
    }
    impact = {
        "impact_direction": "UP",
        "impact_confidence": 80,
        "horizon": "INTRADAY",
        "rationale": ["Safe-haven demand"],
    }
    message = format_alert(article, impact, impact)
    assert "Not financial advice" in message
