from __future__ import annotations

import discord

from careers_engine.config import DISCORD_CHANNEL_ID, DISCORD_TOKEN, DISCORD_GUILD_ID
from careers_engine.discord.publisher import DiscordPublisher
from careers_engine.models import Job


class DiscordClient(discord.Client):
    """Discord client responsible for publishing jobs."""

    def __init__(self, jobs: list[Job]) -> None:
        super().__init__(intents=discord.Intents.default())

        self.jobs = jobs

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

        # clean up existing guilds
        for guild in self.guilds:
            if guild.id != DISCORD_GUILD_ID:
                print(
                    f"Leaving unauthorized guild: "
                    f"{guild.name} ({guild.id})"
                )

                await guild.leave()

        guild = self.get_guild(DISCORD_GUILD_ID)
        if guild is None:
            raise RuntimeError(
                "Configured Discord guild not found."
            )

        channel = guild.get_channel(DISCORD_CHANNEL_ID)

        if not isinstance(channel, discord.TextChannel):
            raise RuntimeError("Configured Discord channel not found.")

        publisher = DiscordPublisher(channel)

        await publisher.publish(self.jobs)

        await self.close()

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Leave unauthorized guilds."""

        if guild.id != DISCORD_GUILD_ID:
            print(
                f"Leaving unauthorized guild "
                f"{guild.name} ({guild.id})"
            )

            await guild.leave()

    async def start_client(self) -> None:
        """Start the Discord client."""
        
        if DISCORD_GUILD_ID == 0:
            raise RuntimeError("DISCORD_GUILD_ID is not configured.")

        if DISCORD_CHANNEL_ID == 0:
            raise RuntimeError("DISCORD_CHANNEL_ID is not configured.")

        await self.start(DISCORD_TOKEN)
