# Finance News → Commodity Impact → Telegram Alerts

A Windows-friendly, always-on system that collects macro/finance/central-bank/geopolitics/commodities news, deduplicates and scores it, produces probabilistic impact signals for Gold (XAU) and Silver (XAG), and sends Telegram alerts when stories look “juicy.”

> **Disclaimer:** Not financial advice. Forecasts are uncertain.

## What this does
- **Ingests** multiple RSS/API sources on a schedule (default every 5 minutes).
- **Normalizes + deduplicates** stories and stores them in SQLite.
- **Tags** macro event types and entities using transparent keyword rules.
- **Generates impact signals** (direction/confidence/horizon) for XAU/XAG.
- **Sends Telegram alerts** when the “juicy threshold” is met.
- **Stores alert history** to avoid duplicates and throttle noisy bursts.

## Limitations
- Outputs are **probabilistic impact signals**, not guaranteed predictions.
- Uses **lightweight heuristics** by default; optional ML training is provided as a stub.
- Web scraping is only implemented as a **basic fallback** and must respect site ToS/robots.txt.

## Prerequisites
- Windows 10/11
- Python **3.11+**

## Quick Start (Windows)
1) **Create and activate a virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2) **Install dependencies**
```bash
pip install -r finance-scout/requirements.txt
```

3) **Configure environment variables**
```bash
copy finance-scout\.env.example finance-scout\.env
```
Edit `finance-scout/.env` and set:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- Optional API keys if you add API sources

4) **Configure sources**
Edit `finance-scout/sources.yml` to add or remove RSS/API sources.

5) **Initialize the database**
```bash
python finance-scout/scripts/init_db.py
```

6) **Run the system**
```bash
python -m app.main
```

## Running 24/7 on Windows
### Option A: Windows Task Scheduler
1. Open **Task Scheduler** → **Create Task**.
2. **General** tab: set “Run whether user is logged on or not”.
3. **Triggers** tab: add **At startup** trigger.
4. **Actions** tab: set Program/script to your venv Python:
   - `C:\path\to\your\project\.venv\Scripts\python.exe`
   - Add arguments: `-m app.main`
   - Start in: `C:\path\to\your\project\finance-scout`
5. Save the task and enter your Windows password when prompted.

### Option B: NSSM (Optional Service)
1. Install [NSSM](https://nssm.cc/).
2. Create a service:
   ```bash
   nssm install FinanceScout "C:\path\to\project\.venv\Scripts\python.exe" "-m app.main"
   ```
3. Set **Startup Directory** to `C:\path\to\project\finance-scout`.
4. Start the service from Services.

## Configuration Guide
- **Intervals**: `.env` → `FETCH_INTERVAL_MINUTES`
- **Juicy threshold**: `.env` → `JUICY_THRESHOLD`
- **Alert throttle**: `.env` → `MAX_ALERTS_PER_HOUR`
- **Sources**: `sources.yml` allows per-source `refresh_minutes` and `weight`

### Adding a new RSS source
1. Add a new entry to `sources.yml`:
```yaml
- name: "MySource"
  kind: "rss"
  url: "https://example.com/rss.xml"
  refresh_minutes: 10
  weight: 1.0
```
2. Restart the application.

### Adding a new API source
1. Add a new entry with `kind: "gdelt"` or implement another function in `app/ingest/apis.py`.
2. Add any required API keys to `.env`.

## Alert Format
Telegram messages include:
- Title
- Source + time
- “Why it matters” bullets
- Impact Forecast (direction/confidence/horizon)
- Key drivers (entities/event types)
- Source link
- **Disclaimer**: “Not financial advice. Forecasts are uncertain.”

## Backtesting / Evaluation
Use a CSV with `title`, `summary`, and `expected_direction`:
```bash
python finance-scout/scripts/backtest.py --path data/sample_headlines.csv
```
This prints accuracy and a small confusion breakdown.

## Testing
```bash
pytest finance-scout/tests
```

## Troubleshooting
- **SSL errors**: upgrade `certifi` or update corporate proxy settings.
- **Telegram errors**: ensure the bot is added to the chat and `TELEGRAM_CHAT_ID` is correct.
- **Rate limits**: lower the `FETCH_INTERVAL_MINUTES` and source count.

## Security Notes
- Never commit `.env` or API keys.
- Use a separate Telegram bot token for production.

## Deployment Notes
- **Simplest**: Windows VPS with Task Scheduler or NSSM.
- **Optional Linux**: run with `systemd` if you later move to Linux.

## Project Structure
```
finance-scout/
  app/
    main.py
    config.py
    scheduler.py
    sources.py
    ingest/
      rss.py
      apis.py
      scrape.py
    nlp/
      embeddings.py
      entity_extract.py
      classify_event.py
      sentiment.py
    signals/
      rules.py
      ml_model.py
      impact.py
      juicy.py
    storage/
      db.py
      schema.sql
    telegram/
      bot.py
      format.py
    web/
      status_api.py
  scripts/
    init_db.py
    backtest.py
    train_model.py
    export_daily_digest.py
  tests/
    test_dedupe.py
    test_rules.py
    test_telegram_format.py
  sources.yml
  .env.example
  requirements.txt
  README.md
```
