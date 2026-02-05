from __future__ import annotations

import requests
from bs4 import BeautifulSoup


def allowed_by_robots(url: str) -> bool:
    return True


def fetch_full_text(url: str) -> str | None:
    if not allowed_by_robots(url):
        return None
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return "\n".join(paragraphs)
