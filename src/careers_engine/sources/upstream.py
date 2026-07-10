from __future__ import annotations

from careers_engine.models import Job
from careers_engine.sources.base import BaseSource


class UpstreamSource(BaseSource):
    """External upstream job source."""

    @property
    def name(self) -> str:
        return "upstream"

    async def collect(self) -> list[Job]:
        raise NotImplementedError("Source collection not implemented yet.")
