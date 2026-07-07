from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class PublishHistory:
    """Stores identifiers of already published jobs."""

    def __init__(self, path: str | Path = "data/history.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save(set())

    def load(self) -> set[str]:
        data = json.loads(self.path.read_text())

        return set(data["published"])

    def save(self, published: set[str]) -> None:
        payload = {
            "version": 1,
            "updated_at": datetime.now(UTC).isoformat(),
            "published": sorted(published),
        }

        self.path.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False)
        )

    def contains(self, identifier: str) -> bool:
        return identifier in self.load()

    def add(self, identifier: str) -> None:
        published = self.load()

        published.add(identifier)

        self.save(published)