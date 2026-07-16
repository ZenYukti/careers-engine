from __future__ import annotations

import discord

from careers_engine.discord import JobFormatter
from careers_engine.models import Job


class DiscordPublisher:
    """Publish jobs to a Discord text channel."""

    def __init__(self, channel: discord.TextChannel) -> None:
        self.channel = channel
        self.formatter = JobFormatter()

    async def publish(self, jobs: list[Job]) -> None:
        """Publish each job as a Discord embed."""

        for job in jobs:
            embed = self.formatter.format(job)
            await self.channel.send(embed=embed)
