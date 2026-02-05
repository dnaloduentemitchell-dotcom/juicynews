from __future__ import annotations

from typing import Any

import requests


def fetch_gdelt(url: str, source_name: str) -> list[dict]:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    records = []
    for item in data.get("articles", []):
        records.append(
            {
                "id": item.get("url") or item.get("title"),
                "title": item.get("title", ""),
                "summary": item.get("seendate"),
                "full_text": None,
                "source": source_name,
                "url": item.get("url"),
                "published_at": item.get("seendate"),
                "tickers": [],
                "keywords": [],
                "raw_json": item,
            }
        )
    return records


def fetch_newsapi(url: str, source_name: str, api_key: str) -> list[dict]:
    response = requests.get(url, headers={"X-Api-Key": api_key}, timeout=30)
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    records = []
    for item in data.get("articles", []):
        records.append(
            {
                "id": item.get("url") or item.get("title"),
                "title": item.get("title", ""),
                "summary": item.get("description"),
                "full_text": item.get("content"),
                "source": source_name,
                "url": item.get("url"),
                "published_at": item.get("publishedAt"),
                "tickers": [],
                "keywords": [],
                "raw_json": item,
            }
        )
    return records
