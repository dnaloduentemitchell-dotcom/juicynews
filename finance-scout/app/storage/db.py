from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable, Optional

from app.config import settings


def connect_db() -> sqlite3.Connection:
    Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(schema_path: Optional[Path] = None) -> None:
    if schema_path is None:
        schema_path = Path(__file__).resolve().parent / "schema.sql"
    conn = connect_db()
    with conn:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.close()


def insert_articles(records: Iterable[dict]) -> int:
    conn = connect_db()
    inserted = 0
    with conn:
        for record in records:
            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO articles
                    (id, title, summary, full_text, source, url, published_at, tickers, keywords, raw_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record["id"],
                        record["title"],
                        record.get("summary"),
                        record.get("full_text"),
                        record.get("source"),
                        record.get("url"),
                        record.get("published_at"),
                        json.dumps(record.get("tickers", [])),
                        json.dumps(record.get("keywords", [])),
                        json.dumps(record.get("raw_json", {})),
                    ),
                )
                if conn.total_changes > 0:
                    inserted += 1
            except sqlite3.IntegrityError:
                continue
    conn.close()
    return inserted


def fetch_recent_articles(limit: int = 200) -> list[dict]:
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def insert_signal(signal: dict) -> None:
    conn = connect_db()
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO signals
            (id, article_id, cluster_id, impact_direction, impact_confidence, horizon, rationale, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                signal["id"],
                signal.get("article_id"),
                signal.get("cluster_id"),
                signal.get("impact_direction"),
                signal.get("impact_confidence"),
                signal.get("horizon"),
                json.dumps(signal.get("rationale", [])),
                signal.get("created_at"),
            ),
        )
    conn.close()


def insert_alert(alert: dict) -> None:
    conn = connect_db()
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO sent_alerts
            (id, article_id, cluster_id, sent_at, channel, payload)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                alert["id"],
                alert.get("article_id"),
                alert.get("cluster_id"),
                alert.get("sent_at"),
                alert.get("channel"),
                json.dumps(alert.get("payload", {})),
            ),
        )
    conn.close()


def count_alerts_last_hour() -> int:
    conn = connect_db()
    row = conn.execute(
        """
        SELECT COUNT(*) as count FROM sent_alerts
        WHERE sent_at >= datetime('now', '-1 hour')
        """
    ).fetchone()
    conn.close()
    return int(row["count"])


def alert_exists_for_article(article_id: str) -> bool:
    conn = connect_db()
    row = conn.execute(
        "SELECT 1 FROM sent_alerts WHERE article_id = ? LIMIT 1",
        (article_id,),
    ).fetchone()
    conn.close()
    return row is not None
