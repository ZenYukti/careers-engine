import discord

from careers_engine.discord import JobFormatter
from careers_engine.models import Job


def test_job_formatter():
    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="Bengaluru, India",
        apply_url="https://careers.google.com",
    )

    embed = JobFormatter().format(job)

    assert isinstance(embed, discord.Embed)
    assert embed.title == job.role
    assert embed.url == job.apply_url
    assert "Google" in embed.description
    assert len(embed.fields) >= 3
