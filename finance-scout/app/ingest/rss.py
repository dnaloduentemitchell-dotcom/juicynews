from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

import feedparser
import requests


def normalize_entry(entry: dict[str, Any], source_name: str) -> dict:
    url = entry.get("link") or entry.get("id") or ""
    title = entry.get("title", "").strip()
    summary = entry.get("summary", "")
    published = entry.get("published") or entry.get("updated")
    if published:
        try:
            published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            published_dt = datetime.now(timezone.utc)
    else:
        published_dt = datetime.now(timezone.utc)

    raw_id = f"{source_name}:{url}:{title}"
    article_id = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()

    return {
        "id": article_id,
        "title": title,
        "summary": summary,
        "full_text": None,
        "source": source_name,
        "url": url,
        "published_at": published_dt.isoformat(),
        "tickers": [],
        "keywords": [],
        "raw_json": entry,
    }


def fetch_rss(url: str, source_name: str) -> list[dict]:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    feed = feedparser.parse(response.text)
    records = []
    for entry in feed.entries:
        records.append(normalize_entry(entry, source_name))
    return records
