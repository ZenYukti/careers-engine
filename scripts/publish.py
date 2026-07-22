from __future__ import annotations

import asyncio

from careers_engine.discord.client import DiscordClient
from careers_engine.storage import JobDatabase, PublishHistory


async def main() -> None:
    database = JobDatabase()
    history = PublishHistory()

    jobs = database.load()

    jobs = history.unpublished(jobs)

    if not jobs:
        print("No unpublished jobs found.")
        return

    client = DiscordClient(jobs)

    await client.start_client()

    history.mark_published(jobs)


if __name__ == "__main__":
    asyncio.run(main())
