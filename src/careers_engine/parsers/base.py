from __future__ import annotations

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract parser interface."""

    @abstractmethod
    def parse(self, content: str) -> list[dict]:
        """Parse raw content into normalized dictionaries."""
