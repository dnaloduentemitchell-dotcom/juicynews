from __future__ import annotations

from loguru import logger

from app.config import settings
from app.scheduler import run_forever
from app.storage.db import init_db
from app.web.status_api import start_status_api


def main() -> None:
    logger.info("Initializing database")
    init_db()
    if settings.enable_status_api:
        start_status_api()
    run_forever()


if __name__ == "__main__":
    main()
