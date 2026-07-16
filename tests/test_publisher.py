from unittest.mock import AsyncMock

import pytest

from careers_engine.discord import DiscordPublisher
from careers_engine.models import Job


@pytest.mark.asyncio
async def test_publish_job():
    channel = AsyncMock()

    publisher = DiscordPublisher(channel)

    jobs = [
        Job(
            company="Google",
            role="SWE Intern",
            location="India",
            apply_url="https://google.com",
        )
    ]

    await publisher.publish(jobs)

    channel.send.assert_awaited_once()
