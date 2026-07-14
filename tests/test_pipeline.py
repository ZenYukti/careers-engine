from unittest.mock import AsyncMock

import pytest

from careers_engine.models import Job
from careers_engine.pipeline import Pipeline
from careers_engine.sources import UpstreamSource


@pytest.mark.asyncio
async def test_pipeline_collect(monkeypatch):
    source = UpstreamSource()

    source.collect = AsyncMock(
        return_value=[
            Job(
                company="Google",
                role="SWE Intern",
                location="India",
                apply_url="https://example.com",
            )
        ]
    )

    monkeypatch.setattr(
        "careers_engine.pipeline.get_sources",
        lambda: [source],
    )

    jobs = await Pipeline().collect()

    assert len(jobs) == 1
