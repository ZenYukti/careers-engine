from __future__ import annotations

from careers_engine.models import Job
from careers_engine.sources import get_sources


class Pipeline:
    """Collect jobs from all configured sources."""

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for source in get_sources():
            jobs.extend(await source.collect())

        return jobs
