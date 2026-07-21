from careers_engine.filters import JobFilter
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
