from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from careers_engine.config import JOBS_FILE
from careers_engine.models import Job


class JobDatabase:
    """Persistent storage for discovered jobs."""

    def __init__(self, path: str | Path = JOBS_FILE) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save([])

    def load(self) -> list[Job]:
        if not self.path.exists():
            return []

        content = self.path.read_text().strip()

        if not content:
            return []

        payload = json.loads(content)

        jobs = payload.get("jobs", [])

        return [Job.from_dict(item) for item in jobs]

    def save(self, jobs: list[Job]) -> None:
        payload = {
            "version": 1,
            "updated_at": datetime.now(UTC).isoformat(),
            "jobs": [job.model_dump(mode="json") for job in jobs],
        }

        # creating parent directory beofre writing the file
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.path.write_text(json.dumps(payload, indent=4, ensure_ascii=False))

    def add(self, job: Job) -> bool:
        jobs = self.load()

        if any(existing.identifier == job.identifier for existing in jobs):
            return False

        jobs.append(job)
        self.save(jobs)

        return True

    def exists(self, identifier: str) -> bool:
        return any(job.identifier == identifier for job in self.load())

    def sync(self, jobs: list[Job]) -> list[Job]:
        """Persist jobs and return newly discovered jobs."""

        existing = self.load()

        existing_by_id = {job.identifier: job for job in existing}

        merged_jobs: list[Job] = []
        new_jobs: list[Job] = []

        for job in jobs:
            if job.identifier in existing_by_id:
                merged_jobs.append(existing_by_id[job.identifier])
            else:
                merged_jobs.append(job)
                new_jobs.append(job)

        if new_jobs:
            self.save(merged_jobs)

        return new_jobs
