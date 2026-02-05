CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    full_text TEXT,
    source TEXT,
    url TEXT UNIQUE,
    published_at TEXT,
    tickers TEXT,
    keywords TEXT,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS clusters (
    id TEXT PRIMARY KEY,
    label TEXT,
    created_at TEXT,
    updated_at TEXT,
    volume INTEGER,
    sentiment REAL,
    key_phrases TEXT
);

CREATE TABLE IF NOT EXISTS article_clusters (
    article_id TEXT,
    cluster_id TEXT,
    PRIMARY KEY (article_id, cluster_id)
);

CREATE TABLE IF NOT EXISTS sent_alerts (
    id TEXT PRIMARY KEY,
    article_id TEXT,
    cluster_id TEXT,
    sent_at TEXT,
    channel TEXT,
    payload TEXT
);

CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    article_id TEXT,
    cluster_id TEXT,
    impact_direction TEXT,
    impact_confidence INTEGER,
    horizon TEXT,
    rationale TEXT,
    created_at TEXT
);
