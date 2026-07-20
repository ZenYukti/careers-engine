from __future__ import annotations

import asyncio

from careers_engine.discord.client import DiscordClient
from careers_engine.pipeline import Pipeline
from careers_engine.storage import JobDatabase


async def main() -> None:
    database = JobDatabase()

    jobs = await Pipeline().collect()

    new_jobs = database.sync(jobs)

    print(f"Collected {len(jobs)} jobs.")
    print(f"New jobs: {len(new_jobs)}")

    if not new_jobs:
        return

    client = DiscordClient(new_jobs)
    await client.start_client()


if __name__ == "__main__":
    asyncio.run(main())
