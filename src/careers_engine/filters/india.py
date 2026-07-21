from __future__ import annotations

from careers_engine.filters.base import JobFilter
from careers_engine.models import Job


class IndiaFilter(JobFilter):
    """Keep jobs relevant to applicants in India."""

    KEYWORDS = (
        "india",
        "remote",
    )

    def match(self, job: Job) -> bool:
        location = job.location.lower()

        return any(keyword in location for keyword in self.KEYWORDS)
