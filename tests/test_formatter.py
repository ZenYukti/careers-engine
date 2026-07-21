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

    assert embed.author.name == "Google"

    fields = {field.name: field.value for field in embed.fields}

    assert fields["Location"] == "Bengaluru, India"
    assert fields["Role Type"] == "Internship"
    assert fields["\u200b"] == "🔗 **[Apply Here](https://google.com)**"

    assert embed.footer.text == "Powered by ZenYukti Jobs"

    assert embed.color.value == 0x4285F4
