from __future__ import annotations

import os

from careers_engine.config import QUEUE_FILE
from careers_engine.models import Job
from careers_engine.storage import JobDatabase


def optional(value: str | None) -> str | None:
    """Convert empty strings to None."""

    if value is None:
        return None

    value = value.strip()

    return value or None


def getenv(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise ValueError(f"Missing required environment variable: {name}")

    return value.strip()


def main() -> None:
    queue = JobDatabase(QUEUE_FILE)

    jobs = queue.load()

    job = Job(
        company=getenv("COMPANY"),
        role=getenv("ROLE"),
        location=getenv("LOCATION"),
        apply_url=getenv("APPLY_URL"),
        employment_type=getenv("EMPLOYMENT_TYPE"),
        priority=getenv("PRIORITY"),
        deadline=optional(os.getenv("DEADLINE")),
        stipend=optional(os.getenv("STIPEND")),
        eligibility=optional(os.getenv("ELIGIBILITY")),
        description=optional(os.getenv("DESCRIPTION")),
    )

    jobs.append(job)

    queue.save(jobs)

    print("Queued manual opportunity:")
    print(f"  Company : {job.company}")
    print(f"  Role    : {job.role}")
    print(f"  Queue   : {len(jobs)} job(s)")


if __name__ == "__main__":
    main()
