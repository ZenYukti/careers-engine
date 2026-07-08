import pytest

from careers_engine.fetchers import HttpFetcher


@pytest.mark.asyncio
async def test_fetch():
    fetcher = HttpFetcher()

    html = await fetcher.fetch("https://example.com")

    assert "Example Domain" in html

    await fetcher.close()
