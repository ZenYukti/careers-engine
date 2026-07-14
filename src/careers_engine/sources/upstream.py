from __future__ import annotations

from careers_engine.config import (
    UPSTREAM_BRANCH,
    UPSTREAM_FILES,
    UPSTREAM_REPOSITORY,
)
from careers_engine.models import Job
from careers_engine.parsers import MarkdownTableParser
from careers_engine.sources.base import BaseSource


class UpstreamSource(BaseSource):
    """Collect jobs from the configured upstream repository."""

    def __init__(self) -> None:
        super().__init__()

        self.parser = MarkdownTableParser()

    @property
    def name(self) -> str:
        return "upstream"

    @property
    def base_url(self) -> str:
        return f"https://raw.githubusercontent.com/{UPSTREAM_REPOSITORY}/{UPSTREAM_BRANCH}"

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for filename in UPSTREAM_FILES:
            markdown = await self.fetcher.fetch(f"{self.base_url}/{filename}")

            rows = self.parser.parse(markdown)

            for row in rows:
                jobs.append(
                    Job(
                        company=row["company"],
                        role=row["role"],
                        location=row["location"],
                        apply_url=row["posting"],
                    )
                )

        return jobs
