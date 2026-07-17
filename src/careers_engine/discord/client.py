from __future__ import annotations

import discord

from careers_engine.config import DISCORD_CHANNEL_ID, DISCORD_TOKEN
from careers_engine.discord.publisher import DiscordPublisher
from careers_engine.models import Job


class DiscordClient(discord.Client):
    """Discord client responsible for publishing jobs."""

    def __init__(self, jobs: list[Job]) -> None:
        super().__init__(intents=discord.Intents.default())

        self.jobs = jobs

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

        guild = self.guilds[0]

        channel = guild.get_channel(DISCORD_CHANNEL_ID)

        if not isinstance(channel, discord.TextChannel):
            raise RuntimeError("Configured Discord channel not found.")

        publisher = DiscordPublisher(channel)

        await publisher.publish(self.jobs)

        await self.close()

    async def start_client(self) -> None:
        """Start the Discord client."""
        await self.start(DISCORD_TOKEN)
