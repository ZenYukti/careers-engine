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
