from __future__ import annotations

import re

from bs4 import BeautifulSoup

from careers_engine.parsers.base import BaseParser


class MarkdownTableParser(BaseParser):
    """Parser for markdown job tables."""

    TABLE_START = re.compile(r"<!-- TABLE_(.+?)_START -->")
    TABLE_END = re.compile(r"<!-- TABLE_(.+?)_END -->")

    @staticmethod
    def _extract_text(html: str) -> str:
        """Extract plain text from HTML."""
        return BeautifulSoup(html, "html.parser").get_text(strip=True)

    @staticmethod
    def _extract_href(html: str) -> str:
        """Extract hyperlink from HTML."""
        soup = BeautifulSoup(html, "html.parser")

        link = soup.find("a")

        if link and link.has_attr("href"):
            return str(link["href"])

        return html

    def parse(self, content: str) -> list[dict]:
        rows: list[dict] = []

        current_category: str | None = None
        in_table = False

        for line in content.splitlines():
            line = line.strip()

            start = self.TABLE_START.match(line)
            if start:
                current_category = start.group(1).lower()
                in_table = True
                continue

            if self.TABLE_END.match(line):
                in_table = False
                current_category = None
                continue

            if not in_table:
                continue

            if not line.startswith("|"):
                continue

            if "---" in line:
                continue

            columns = [column.strip() for column in line.strip("|").split("|")]

            if len(columns) < 5:
                continue

            if columns[0].lower() == "company":
                continue

            rows.append(
                {
                    "category": current_category,
                    "company": self._extract_text(columns[0]),
                    "role": columns[1],
                    "location": columns[2],
                    "posting": self._extract_href(columns[3]),
                    "age": columns[4],
                }
            )

        return rows
