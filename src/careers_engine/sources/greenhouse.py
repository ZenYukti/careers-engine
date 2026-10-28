from __future__ import annotations

from careers_engine.company.ats_registry import get_boards
from careers_engine.employment import normalize_employment_type
from careers_engine.models import Job
from careers_engine.sources.ats import fetch_board_json
from careers_engine.sources.base import BaseSource


class GreenhouseSource(BaseSource):
    """Collect jobs from configured Greenhouse job boards."""

    API_URL = (
        "https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    )

    @property
    def name(self) -> str:
        return "greenhouse"

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for board in get_boards("greenhouse"):
            slug = board["slug"]

            data = await fetch_board_json(
                fetcher=self.fetcher,
                url=self.API_URL.format(board=slug),
                provider=self.name,
                board=slug,
            )

            if data is None:
                continue

            for posting in data.get("jobs", []):
                title = posting.get("title")
                apply_url = posting.get("absolute_url")

                if not title or not apply_url:
                    continue

                location_data = posting.get("location") or {}

                jobs.append(
                    Job(
                        company=(
                            board.get("company_name")
                            or posting.get("company_name")
                            or slug
                        ),
                        role=title,
                        location=location_data.get("name") or "Not specified",
                        apply_url=apply_url,
                        employment_type=normalize_employment_type(
                            None,
                            title,
                        ),
                        description=posting.get("content"),
                    )
                )

        return jobs
