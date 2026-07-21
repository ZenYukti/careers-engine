from __future__ import annotations

from abc import ABC, abstractmethod

from careers_engine.models import Job


class JobFilter(ABC):
    """Base class for job filters."""

    @abstractmethod
    def match(self, job: Job) -> bool:
        """Return True if the job should be kept."""
