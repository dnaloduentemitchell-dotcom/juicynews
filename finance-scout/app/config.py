from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()


@dataclass
class Settings:
    db_path: str = os.getenv("DB_PATH", str(BASE_DIR / "data.db"))
    sources_path: str = os.getenv("SOURCES_PATH", str(BASE_DIR / "sources.yml"))
    fetch_interval_minutes: int = int(os.getenv("FETCH_INTERVAL_MINUTES", "5"))
    juicy_threshold: float = float(os.getenv("JUICY_THRESHOLD", "0.7"))
    max_alerts_per_hour: int = int(os.getenv("MAX_ALERTS_PER_HOUR", "10"))
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    daily_digest_time: str = os.getenv("DAILY_DIGEST_TIME", "17:00")
    enable_status_api: bool = os.getenv("ENABLE_STATUS_API", "false").lower() == "true"
    status_api_port: int = int(os.getenv("STATUS_API_PORT", "8000"))


settings = Settings()
