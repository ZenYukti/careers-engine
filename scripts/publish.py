from __future__ import annotations

import asyncio

from careers_engine.config import (
    DISCORD_HISTORY_FILE,
    JOBS_FILE,
    QUEUE_FILE,
    TELEGRAM_HISTORY_FILE,
)
from careers_engine.discord.client import DiscordClient
from careers_engine.storage import JobDatabase, PublishHistory
from careers_engine.telegram import TelegramPublisher


async def main() -> None:
    automatic_database = JobDatabase(JOBS_FILE)
    queue_database = JobDatabase(QUEUE_FILE)

    automatic_jobs = automatic_database.load()
    queued_jobs = queue_database.load()

    discord_history = PublishHistory(DISCORD_HISTORY_FILE)
    telegram_history = PublishHistory(TELEGRAM_HISTORY_FILE)

    discord_jobs = discord_history.unpublished(automatic_jobs + queued_jobs)
    telegram_jobs = telegram_history.unpublished(automatic_jobs + queued_jobs)

    if not discord_jobs and not telegram_jobs:
        if queued_jobs:
            queue_database.save([])

        print("No unpublished jobs found.")
        return

    failures: list[str] = []

    if discord_jobs:
        try:
            client = DiscordClient(discord_jobs)
            await client.start_client()
            discord_history.mark_published(discord_jobs)
        except Exception as exc:
            failures.append(f"Discord: {exc}")
            print(f"Discord publishing failed: {exc}")

    if telegram_jobs:
        try:
            publisher = TelegramPublisher()
            await publisher.publish(telegram_jobs)
            telegram_history.mark_published(telegram_jobs)
        except Exception as exc:
            failures.append(f"Telegram: {exc}")
            print(f"Telegram publishing failed: {exc}")

    if failures:
        raise RuntimeError("Publishing failed for one or more destinations: " + "; ".join(failures))

    if queued_jobs:
        queue_database.save([])


if __name__ == "__main__":
    asyncio.run(main())
