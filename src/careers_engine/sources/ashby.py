from __future__ import annotations

from careers_engine.company.ats_registry import get_boards
from careers_engine.employment import normalize_employment_type
from careers_engine.models import Job
from careers_engine.sources.ats import fetch_board_json
from careers_engine.sources.base import BaseSource


class AshbySource(BaseSource):
    """Collect jobs from configured Ashby job boards."""

    API_URL = "https://api.ashbyhq.com/posting-api/job-board/{board}"

    @property
    def name(self) -> str:
        return "ashby"

    async def collect(self) -> list[Job]:
        jobs: list[Job] = []

        for board in get_boards("ashby"):
            slug = board["slug"]

            data = await fetch_board_json(
                fetcher=self.fetcher,
                url=self.API_URL.format(board=slug),
                provider=self.name,
                board=slug,
            )

            if data is None or not isinstance(data, dict):
                continue

            for posting in data.get("jobs", []):
                if not posting.get("isListed", False):
                    continue

                title = posting.get("title")
                apply_url = posting.get("applyUrl") or posting.get("jobUrl")

                if not title or not apply_url:
                    continue

                company = (
                    board.get("company_name")
                    or posting.get("companyName")
                    or posting.get("organizationName")
                    or slug
                )

                jobs.append(
                    Job(
                        company=company,
                        role=title,
                        location=posting.get("location") or "Not specified",
                        apply_url=apply_url,
                        employment_type=normalize_employment_type(
                            posting.get("employmentType"),
                            title,
                        ),
                        description=posting.get("descriptionPlain"),
                    )
                )

        return jobs
