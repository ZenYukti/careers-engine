from __future__ import annotations

import asyncio

from careers_engine.config import JOBS_FILE, QUEUE_FILE
from careers_engine.discord.client import DiscordClient
from careers_engine.storage import JobDatabase, PublishHistory


async def main() -> None:
    automatic_database = JobDatabase(JOBS_FILE)
    queue_database = JobDatabase(QUEUE_FILE)

    history = PublishHistory()

    automatic_jobs = history.unpublished(automatic_database.load())

    queued_jobs = queue_database.load()

    jobs = automatic_jobs + queued_jobs

    if not jobs:
        print("No unpublished jobs found.")
        return

    client = DiscordClient(jobs)

    try:
        await client.start_client()

    except Exception:
        raise

    history.mark_published(automatic_jobs)

    queue_database.save([])


if __name__ == "__main__":
    asyncio.run(main())
