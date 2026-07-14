from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from careers_engine.models import Job
from careers_engine.sources import UpstreamSource

FIXTURE = Path(__file__).parent / "fixtures" / "intern_intl.md"


@pytest.mark.asyncio
async def test_collect_jobs():
    source = UpstreamSource()

    source.fetcher.fetch = AsyncMock(return_value=FIXTURE.read_text())

    jobs = await source.collect()

    assert jobs
    assert isinstance(jobs[0], Job)
