from __future__ import annotations

from careers_engine.parsers.base import BaseParser


class MarkdownTableParser(BaseParser):
    """Parser for Markdown tables."""

    def parse(self, content: str) -> list[dict]:
        raise NotImplementedError
