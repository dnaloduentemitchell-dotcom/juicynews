from app.signals.rules import apply_rules


def test_apply_rules_detects_geo() -> None:
    results = apply_rules("War risk pushes investors to gold")
    assert any(result.rule == "geopolitical_risk" for result in results)
