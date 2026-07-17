from careers_engine.discord.client import DiscordClient
from careers_engine.models import Job


def test_client_stores_jobs():
    jobs = [
        Job(
            company="Google",
            role="SWE Intern",
            location="India",
            apply_url="https://google.com",
        )
    ]

    client = DiscordClient(jobs)

    assert client.jobs == jobs
