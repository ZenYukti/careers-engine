from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from careers_engine.models import Job
from careers_engine.sources import AshbySource, SimplifySource, UpstreamSource

FIXTURE = Path(__file__).parent / "fixtures" / "intern_intl.md"


@pytest.mark.asyncio
async def test_collect_jobs():
    source = UpstreamSource()

    source.fetcher.fetch = AsyncMock(return_value=FIXTURE.read_text())

    jobs = await source.collect()

    assert jobs
    assert isinstance(jobs[0], Job)


@pytest.mark.asyncio
async def test_simplify_collect_jobs():
    source = SimplifySource()

    content = """
    [
        {
            "company_name": "Google",
            "title": "Software Engineer Intern",
            "active": true,
            "is_visible": true,
            "url": "https://example.com/google",
            "locations": ["Bengaluru, India"]
        }
    ]
    """

    source.fetcher.fetch = AsyncMock(return_value=content)

    jobs = await source.collect()

    assert len(jobs) == 1
    assert isinstance(jobs[0], Job)

    assert jobs[0].company == "Google"
    assert jobs[0].role == "Software Engineer Intern"
    assert jobs[0].location == "Bengaluru, India"
    assert jobs[0].apply_url == "https://example.com/google"


@pytest.mark.asyncio
async def test_simplify_ignores_inactive_jobs():
    source = SimplifySource()

    content = """
    [
        {
            "company_name": "Google",
            "title": "Software Engineer Intern",
            "active": false,
            "is_visible": true,
            "url": "https://example.com/google",
            "locations": ["Bengaluru, India"]
        }
    ]
    """

    source.fetcher.fetch = AsyncMock(return_value=content)

    jobs = await source.collect()

    assert jobs == []


@pytest.mark.asyncio
async def test_simplify_ignores_hidden_jobs():
    source = SimplifySource()

    content = """
    [
        {
            "company_name": "Google",
            "title": "Software Engineer Intern",
            "active": true,
            "is_visible": false,
            "url": "https://example.com/google",
            "locations": ["Bengaluru, India"]
        }
    ]
    """

    source.fetcher.fetch = AsyncMock(return_value=content)

    jobs = await source.collect()

    assert jobs == []


@pytest.mark.asyncio
async def test_simplify_ignores_jobs_without_location():
    source = SimplifySource()

    content = """
    [
        {
            "company_name": "Google",
            "title": "Software Engineer Intern",
            "active": true,
            "is_visible": true,
            "url": "https://example.com/google",
            "locations": []
        }
    ]
    """

    source.fetcher.fetch = AsyncMock(return_value=content)

    jobs = await source.collect()

    assert jobs == []


@pytest.mark.asyncio
async def test_ashby_collect_jobs():
    source = AshbySource()

    with patch(
        "careers_engine.sources.ashby.get_boards",
        return_value=[
            {"slug": "google", "company_name": "Google"}
        ],
    ):
        source.fetcher.fetch = AsyncMock(
            return_value="""
            {
                "jobs": [
                    {
                        "title": "Software Engineer Intern",
                        "location": "Bengaluru, India",
                        "jobUrl": "https://jobs.ashbyhq.com/google/123",
                        "applyUrl": "https://jobs.ashbyhq.com/google/123/application",
                        "isListed": true,
                        "descriptionPlain": "Internship opportunity"
                    }
                ]
            }
            """
        )

        jobs = await source.collect()

    assert len(jobs) == 1
    assert jobs[0].company == "Google"
    assert jobs[0].role == "Software Engineer Intern"
    assert jobs[0].location == "Bengaluru, India"
    assert jobs[0].apply_url == "https://jobs.ashbyhq.com/google/123/application"
    assert jobs[0].description == "Internship opportunity"


# ensure a failed board does not prevent subsequent boards from being fetched
@pytest.mark.asyncio
async def test_ashby_skips_failed_board_and_continues():
    source = AshbySource()

    with patch(
        "careers_engine.sources.ashby.get_boards",
        return_value=[
            {"slug": "invalid", "company_name": "Invalid"},
            {"slug": "google", "company_name": "Google"},
        ],
    ):
        source.fetcher.fetch = AsyncMock(
            side_effect=[
                httpx.HTTPStatusError(
                    "404 Not Found",
                    request=httpx.Request(
                        "GET", "https://example.com"
                    ),
                    response=httpx.Response(404),
                ),
                '{"jobs": []}',
            ]
        )

        jobs = await source.collect()

    assert jobs == []
    assert source.fetcher.fetch.await_count == 2
