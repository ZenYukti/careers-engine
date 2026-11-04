from __future__ import annotations

from careers_engine.company.ats_registry import get_boards
from careers_engine.employment import normalize_employment_type
from careers_engine.models import Job
from careers_engine.sources.ats import fetch_board_json
from careers_engine.sources.base import BaseSource


class LeverSource(BaseSource):
    """Collect jobs from configured Lever job sites."""

    API_URL = "https://api.lever.co/v0/postings/{site}?mode=json"

    @property
    def name(self) -> str:
        return "lever"

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for board in get_boards("lever"):
            slug = board["slug"]

            data = await fetch_board_json(
                fetcher=self.fetcher,
                url=self.API_URL.format(site=slug),
                provider=self.name,
                board=slug,
            )

            if data is None or not isinstance(data, list):
                continue

            for posting in data:
                title = posting.get("text")
                apply_url = posting.get("hostedUrl") or posting.get("applyUrl")

                if not title or not apply_url:
                    continue

                categories = posting.get("categories") or {}

                jobs.append(
                    Job(
                        company=board.get("company_name") or slug,
                        role=title,
                        location=categories.get("location") or "Not specified",
                        apply_url=apply_url,
                        employment_type=normalize_employment_type(
                            categories.get("commitment"),
                            title,
                        ),
                        description=posting.get("descriptionPlain"),
                    )
                )

        return jobs
