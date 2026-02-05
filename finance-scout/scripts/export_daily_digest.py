from __future__ import annotations

from datetime import datetime, timezone

from app.storage.db import fetch_recent_articles


def export_digest(limit: int = 10) -> None:
    articles = fetch_recent_articles(limit=limit)
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Daily Digest {timestamp}")
    for article in articles:
        print(f"- {article['title']} ({article['source']}) {article['url']}")


if __name__ == "__main__":
    export_digest()
