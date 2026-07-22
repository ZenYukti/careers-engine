from careers_engine.models import Job
from careers_engine.storage import JobDatabase, PublishHistory


def test_database(tmp_path):
    db = JobDatabase(tmp_path / "jobs.json")

    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="Bengaluru",
        apply_url="https://example.com",
    )

    db.add(job)

    jobs = db.load()

    assert len(jobs) == 1
    assert jobs[0].company == "Google"


def test_history(tmp_path):
    history = PublishHistory(tmp_path / "history.json")

    identifier = "abc123"

    history.add(identifier)

    assert history.contains(identifier)


def test_unpublished_jobs(tmp_path):
    history = PublishHistory(tmp_path / "history.json")

    jobs = [
        Job(
            company="Google",
            role="Software Engineer Intern",
            location="Bengaluru",
            apply_url="https://google.com",
        ),
        Job(
            company="Microsoft",
            role="Software Engineer Intern",
            location="Hyderabad",
            apply_url="https://microsoft.com",
        ),
    ]

    history.mark_published([jobs[0]])

    unpublished = history.unpublished(jobs)

    assert unpublished == [jobs[1]]


def test_mark_published(tmp_path):
    history = PublishHistory(tmp_path / "history.json")

    jobs = [
        Job(
            company="Google",
            role="Software Engineer Intern",
            location="Bengaluru",
            apply_url="https://google.com",
        ),
        Job(
            company="Microsoft",
            role="Software Engineer Intern",
            location="Hyderabad",
            apply_url="https://microsoft.com",
        ),
    ]

    history.mark_published(jobs)

    assert history.contains(jobs[0].identifier)
    assert history.contains(jobs[1].identifier)
