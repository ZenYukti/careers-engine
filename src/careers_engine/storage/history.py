from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from careers_engine.config import HISTORY_FILE
from careers_engine.models import Job


class PublishHistory:
    """Stores identifiers of already published jobs."""

    def __init__(self, path: str | Path = HISTORY_FILE) -> None:
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

        self.path.write_text(json.dumps(payload, indent=4, ensure_ascii=False))

    def contains(self, identifier: str) -> bool:
        return identifier in self.load()

    def add(self, identifier: str) -> None:
        published = self.load()

        published.add(identifier)

        self.save(published)

    def unpublished(self, jobs: list[Job]) -> list[Job]:
        """Return jobs that have not been published."""

        published = self.load()

        return [job for job in jobs if job.identifier not in published]

    def mark_published(self, jobs: list[Job]) -> None:
        """Record published jobs."""

        published = self.load()

        published.update(job.identifier for job in jobs)

        self.save(published)
