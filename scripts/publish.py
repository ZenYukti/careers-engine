from __future__ import annotations

import asyncio
import os

from careers_engine.config import (
    DISCORD_HISTORY_FILE,
    JOBS_FILE,
    QUEUE_FILE,
    TELEGRAM_HISTORY_FILE,
)
from careers_engine.discord.client import DiscordClient
from careers_engine.storage import JobDatabase, PublishHistory
from careers_engine.telegram import TelegramPublisher

MAX_PUBLISH_PER_RUN = int(os.getenv("MAX_PUBLISH_PER_RUN", "25"))


async def main() -> None:
    automatic_database = JobDatabase(JOBS_FILE)
    queue_database = JobDatabase(QUEUE_FILE)

    automatic_jobs = automatic_database.load()
    queued_jobs = queue_database.load()

    discord_history = PublishHistory(DISCORD_HISTORY_FILE)
    telegram_history = PublishHistory(TELEGRAM_HISTORY_FILE)

    all_jobs = automatic_jobs + queued_jobs

    discord_jobs = discord_history.unpublished(all_jobs)[:MAX_PUBLISH_PER_RUN]
    telegram_jobs = telegram_history.unpublished(all_jobs)[:MAX_PUBLISH_PER_RUN]

    if not discord_jobs and not telegram_jobs:
        if queued_jobs:
            queue_database.save([])

        print("No unpublished jobs found.")
        return

    failures: list[str] = []

    if discord_jobs:
        try:
            print(f"Publishing batch of {len(discord_jobs)} jobs to Discord...")
            client = DiscordClient(discord_jobs)
            await client.start_client()
            discord_history.mark_published(discord_jobs)
        except Exception as exc:
            failures.append(f"Discord: {exc}")
            print(f"Discord publishing failed: {exc}")

    if telegram_jobs:
        try:
            print(f"Publishing batch of {len(telegram_jobs)} jobs to Telegram...")
            publisher = TelegramPublisher(history=telegram_history)
            await publisher.publish(telegram_jobs)
        except Exception as exc:
            failures.append(f"Telegram: {exc}")
            print(f"Telegram publishing failed: {exc}")

    if failures:
        msg = "Publishing failed for one or more destinations: " + "; ".join(failures)
        raise RuntimeError(msg)

    is_discord_done = not discord_history.unpublished(queued_jobs)
    is_telegram_done = not telegram_history.unpublished(queued_jobs)
    if queued_jobs and is_discord_done and is_telegram_done:
        queue_database.save([])


if __name__ == "__main__":
    asyncio.run(main())
