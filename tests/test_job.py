from careers_engine.models import Job


def test_identifier_generation():
    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="Bengaluru",
        apply_url="https://example.com",
    )

    assert len(job.identifier) == 64


def test_model_dump():
    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="Bengaluru",
        apply_url="https://example.com",
    )

    data = job.model_dump()

    assert data["company"] == "Google"
