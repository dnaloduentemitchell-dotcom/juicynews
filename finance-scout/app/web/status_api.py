from __future__ import annotations

import threading
from datetime import datetime, timezone

from app.config import settings
from app.storage.db import fetch_recent_articles


app_state = {
    "started_at": datetime.now(timezone.utc).isoformat(),
}


def start_status_api() -> None:
    from fastapi import FastAPI
    import uvicorn

    api = FastAPI()

    @api.get("/health")
    def health() -> dict:
        articles = fetch_recent_articles(limit=5)
        return {
            "status": "ok",
            "started_at": app_state["started_at"],
            "recent_articles": len(articles),
        }

    def run() -> None:
        uvicorn.run(api, host="0.0.0.0", port=settings.status_api_port)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
