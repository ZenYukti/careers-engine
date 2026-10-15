from __future__ import annotations

from abc import ABC, abstractmethod

from careers_engine.models import Job


class JobPublisher(ABC):
    """Interface implemented by job publishing destinations."""

    @abstractmethod
    async def publish(self, jobs: list[Job]) -> None:
        """Publish jobs to the destination."""
        ...
