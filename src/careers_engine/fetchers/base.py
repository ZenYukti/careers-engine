from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    """Abstract base class for all fetchers."""

    @abstractmethod
    async def fetch(self, url: str) -> str:
        """Fetch raw content."""
