from __future__ import annotations

import asyncio

from careers_engine.pipeline import Pipeline


async def main() -> None:
    jobs = await Pipeline().collect()

    print(f"Collected {len(jobs)} jobs.")


if __name__ == "__main__":
    asyncio.run(main())
