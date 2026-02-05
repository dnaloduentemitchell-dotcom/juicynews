from __future__ import annotations

import time
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from app.config import settings
from app.ingest.apis import fetch_gdelt
from app.ingest.rss import fetch_rss
from app.nlp.embeddings import cosine_similarity, embed_text
from app.signals.impact import build_impact_signal, signal_to_record
from app.signals.juicy import compute_juicy_score
from app.sources import load_sources
from app.storage.db import (
    alert_exists_for_article,
    fetch_recent_articles,
    insert_articles,
    insert_signal,
)
from app.telegram.bot import send_alert
from app.telegram.format import format_alert


def dedupe_records(records: list[dict]) -> list[dict]:
    existing = fetch_recent_articles()
    existing_titles = [row["title"] for row in existing]
    existing_vecs = [embed_text(title) for title in existing_titles if title]
    deduped: list[dict] = []
    for record in records:
        title_vec = embed_text(record["title"])
        is_duplicate = False
        for vec in existing_vecs:
            if cosine_similarity(title_vec, vec) > 0.92:
                is_duplicate = True
                break
        if not is_duplicate:
            deduped.append(record)
    return deduped


def compute_novelty(record: dict) -> float:
    return 1.0


def compute_urgency(record: dict) -> float:
    published_at = record.get("published_at")
    if not published_at:
        return 0.5
    try:
        published_dt = datetime.fromisoformat(published_at)
    except ValueError:
        return 0.5
    age_minutes = (datetime.now(timezone.utc) - published_dt).total_seconds() / 60
    if age_minutes <= 30:
        return 1.0
    if age_minutes <= 180:
        return 0.7
    return 0.4


def run_ingestion() -> None:
    logger.info("Starting ingestion cycle")
    sources = [source for source in load_sources() if source.enabled]
    records: list[dict] = []
    for source in sources:
        if source.kind == "rss":
            records.extend(fetch_rss(source.url, source.name))
        elif source.kind == "gdelt":
            records.extend(fetch_gdelt(source.url, source.name))

    records = dedupe_records(records)
    inserted = insert_articles(records)
    logger.info("Inserted {count} new articles", count=inserted)

    for record in records:
        text = " ".join(filter(None, [record.get("title"), record.get("summary")]))
        impact = build_impact_signal(text)
        signal_record = signal_to_record(record["id"], impact)
        insert_signal(signal_record)

        novelty = compute_novelty(record)
        urgency = compute_urgency(record)
        magnitude = impact.impact_confidence / 100
        juicy = compute_juicy_score(novelty, urgency, magnitude)

        if juicy.score >= settings.juicy_threshold and not alert_exists_for_article(record["id"]):
            message = format_alert(record, impact.__dict__, impact.__dict__)
            send_alert(message, record["id"], {"juicy": juicy.score, "impact": impact.__dict__})


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_ingestion, "interval", minutes=settings.fetch_interval_minutes)
    scheduler.start()
    return scheduler


def run_forever() -> None:
    scheduler = start_scheduler()
    logger.info("Scheduler started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
