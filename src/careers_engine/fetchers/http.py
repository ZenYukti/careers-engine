from __future__ import annotations

import httpx

from careers_engine.fetchers.base import BaseFetcher


class HttpFetcher(BaseFetcher):
    """Simple async HTTP client."""

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=20,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "ZenYukti Careers Engine/0.1 (https://github.com/ZenYukti/careers-engine)"
                )
            },
        )

    async def fetch(self, url: str) -> str:
        response = await self.client.get(url)

        response.raise_for_status()

        return response.text

    async def close(self) -> None:
        await self.client.aclose()
