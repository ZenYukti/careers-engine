from careers_engine.discord import JobFormatter
from careers_engine.models import Job


def test_formatter() -> None:
    job = Job(
        company="Google",
        role="Software Engineer Intern",
        location="Bengaluru, India",
        apply_url="https://google.com",
    )

    embed = JobFormatter().format(job)

    assert embed.title == "Software Engineer Intern"
    assert embed.url == "https://google.com"

    assert embed.fields[0].name == "Company"
    assert embed.fields[0].value == "Google"

    assert embed.fields[1].name == "Location"
    assert embed.fields[1].value == "Bengaluru, India"

    assert embed.fields[2].name == "Role Type"
    assert embed.fields[2].value == "Internship"

    assert embed.fields[-1].name == "\u200b"
    assert embed.fields[-1].value == "🔗 **[Apply Here](https://google.com)**"
    assert embed.footer.text == "Powered by ZenYukti Jobs"
