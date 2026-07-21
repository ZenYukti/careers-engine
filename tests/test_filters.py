from careers_engine.filters import IndiaFilter, JobFilter
from careers_engine.models import Job


class DummyFilter(JobFilter):
    def match(self, job: Job) -> bool:
        return True


def test_filter_match() -> None:
    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="India",
        apply_url="https://google.com",
    )

    assert DummyFilter().match(job)


# IndiaFilter() tests


def test_india_filter_accepts_india() -> None:
    job = Job(
        company="Google",
        role="SWE Intern",
        location="Bengaluru, India",
        apply_url="https://google.com",
    )

    assert IndiaFilter().match(job)


def test_india_filter_accepts_remote() -> None:
    job = Job(
        company="GitLab",
        role="Backend Engineer",
        location="Remote",
        apply_url="https://gitlab.com",
    )

    assert IndiaFilter().match(job)


def test_india_filter_rejects_foreign() -> None:
    job = Job(
        company="Google",
        role="SWE Intern",
        location="Sydney, Australia",
        apply_url="https://google.com",
    )

    assert not IndiaFilter().match(job)
