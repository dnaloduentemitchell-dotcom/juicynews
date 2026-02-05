from __future__ import annotations

import argparse
import csv
from collections import Counter

from app.signals.impact import build_impact_signal


def run_backtest(path: str) -> None:
    results = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = f"{row.get('title', '')} {row.get('summary', '')}".strip()
            signal = build_impact_signal(text)
            expected = row.get("expected_direction", "MIXED").upper()
            results.append((expected, signal.impact_direction))

    counts = Counter(results)
    total = len(results)
    correct = sum(1 for exp, got in results if exp == got)
    accuracy = (correct / total) * 100 if total else 0

    print(f"Samples: {total}")
    print(f"Accuracy: {accuracy:.2f}%")
    for (exp, got), count in counts.items():
        print(f"{exp} -> {got}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="CSV with title, summary, expected_direction")
    args = parser.parse_args()
    run_backtest(args.path)
