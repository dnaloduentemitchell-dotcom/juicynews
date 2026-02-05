from __future__ import annotations

from datetime import datetime, timezone

from telegram import Bot

from app.config import settings
from app.storage.db import count_alerts_last_hour, insert_alert


def send_alert(message: str, article_id: str, payload: dict) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False
    if count_alerts_last_hour() >= settings.max_alerts_per_hour:
        return False

    bot = Bot(token=settings.telegram_bot_token)
    bot.send_message(
        chat_id=settings.telegram_chat_id,
        text=message,
        parse_mode="Markdown",
        disable_web_page_preview=False,
    )
    insert_alert(
        {
            "id": f"alert-{article_id}",
            "article_id": article_id,
            "cluster_id": None,
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "channel": "telegram",
            "payload": payload,
        }
    )
    return True
