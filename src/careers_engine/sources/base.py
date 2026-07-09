from __future__ import annotations

from abc import ABC, abstractmethod

from careers_engine.fetchers import HttpFetcher
from careers_engine.models import Job


class BaseSource(ABC):
    """Abstract base class for all job sources."""

    def __init__(self) -> None:
        self.fetcher = HttpFetcher()

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique source name."""

    @abstractmethod
    async def collect(self) -> list[Job]:
        """Collect jobs from the source."""

    async def close(self) -> None:
        """Release network resources."""
        await self.fetcher.close()
