from __future__ import annotations

from careers_engine.filters import IndiaFilter
from careers_engine.models import Job
from careers_engine.sources import get_sources


class Pipeline:
    """Collect jobs from all configured sources."""

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for source in get_sources():
            jobs.extend(await source.collect())

        """ today it includes only IndiaFilter() intentionally, 
            but tomorrow it can include directly other filters
            as well like:
            filters = [
                IndiaFilter(),
                InternshipFilter(),
                GraduateFilter(),
            ]
        """

        filters = [
            IndiaFilter(),
        ]

        for job_filter in filters:
            jobs = [job for job in jobs if job_filter.match(job)]

        return jobs
