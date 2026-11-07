from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

from careers_engine.config import JOBS_FILE
from careers_engine.models import Job

MAX_RETENTION_DAYS = 7


class JobDatabase:
    """Persistent storage for discovered jobs."""

    def __init__(self, path: str | Path = JOBS_FILE) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.save([])

    @staticmethod
    def _purge_expired_jobs(jobs: list[Job]) -> list[Job]:
        """Automatically remove jobs older than the retention window."""
        now = datetime.now(timezone.utc)
        valid_jobs = []
        for job in jobs:
            if job.discovered_at is None:
                valid_jobs.append(job)
                continue

            # Ensure timezone-aware comparison
            discovered = job.discovered_at
            if discovered.tzinfo is None:
                discovered = discovered.replace(tzinfo=timezone.utc)

            if (now - discovered) <= timedelta(days=MAX_RETENTION_DAYS):
                valid_jobs.append(job)
        return valid_jobs

    def load(self) -> list[Job]:
        if not self.path.exists():
            return []

        content = self.path.read_text().strip()

        if not content:
            return []

        payload = json.loads(content)
        jobs = payload.get("jobs", [])

        parsed_jobs = [Job.from_dict(item) for item in jobs]

        # Automatically purge expired jobs on load so storage stays lean
        return self._purge_expired_jobs(parsed_jobs)

    def save(self, jobs: list[Job]) -> None:
        # Purge expired jobs before saving
        valid_jobs = self._purge_expired_jobs(jobs)

        cleaned_jobs = []
        seen_urls = set()

        for job in valid_jobs:
            # Drop descriptions to keep jobs.json tiny for Discord/Telegram bots
            job_clean = job.model_copy(update={"description": None})

            # Normalize apply_url for deduplication
            url = (job_clean.apply_url or "").strip().rstrip("/")
            if url and url in seen_urls:
                continue
            if url:
                seen_urls.add(url)

            cleaned_jobs.append(job_clean)

        payload = {
            "version": 1,
            "updated_at": datetime.now(UTC).isoformat(),
            "jobs": [job.model_dump(mode="json") for job in cleaned_jobs],
        }

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=4, ensure_ascii=False))

    def add(self, job: Job) -> bool:
        jobs = self.load()

        job_clean = job.model_copy(update={"description": None})
        url = (job_clean.apply_url or "").strip().rstrip("/")
        if any((existing.apply_url or "").strip().rstrip("/") == url for existing in jobs if url):
            return False

        if any(existing.identifier == job_clean.identifier for existing in jobs):
            return False

        jobs.append(job_clean)
        self.save(jobs)

        return True

    def exists(self, identifier: str) -> bool:
        return any(job.identifier == identifier for job in self.load())

    def sync(self, jobs: list[Job]) -> list[Job]:
        """Persist jobs and return newly discovered jobs."""

        existing = self.load()
        existing_by_id = {job.identifier: job for job in existing}
        existing_urls = {
            (job.apply_url or "").strip().rstrip("/") for job in existing if job.apply_url
        }

        merged_jobs: list[Job] = list(existing)
        new_jobs: list[Job] = []

        for job in jobs:
            job_clean = job.model_copy(update={"description": None})
            url = (job_clean.apply_url or "").strip().rstrip("/")

            if job_clean.identifier in existing_by_id or (url and url in existing_urls):
                continue

            merged_jobs.append(job_clean)
            new_jobs.append(job_clean)
            if url:
                existing_urls.add(url)
            existing_by_id[job_clean.identifier] = job_clean

        if new_jobs or len(merged_jobs) != len(existing):
            self.save(merged_jobs)

        return new_jobs
