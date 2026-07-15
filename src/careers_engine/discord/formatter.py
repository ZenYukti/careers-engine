from __future__ import annotations

import discord

from careers_engine.models import Job


class JobFormatter:
    """Convert a Job into a Discord embed."""

    def format(self, job: Job) -> discord.Embed:
        embed = discord.Embed(
            title=job.role,
            url=job.apply_url,
            description=f"**{job.company}**",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="Location",
            value=job.location,
            inline=True,
        )

        embed.add_field(
            name="Employment",
            value=job.employment_type.value,
            inline=True,
        )

        if job.deadline:
            embed.add_field(
                name="Deadline",
                value=job.deadline,
                inline=True,
            )

        if job.stipend:
            embed.add_field(
                name="Stipend",
                value=job.stipend,
                inline=True,
            )

        if job.eligibility:
            embed.add_field(
                name="Eligibility",
                value=job.eligibility,
                inline=False,
            )

        embed.add_field(
            name="Apply",
            value=f"[Click Here]({job.apply_url})",
            inline=False,
        )

        embed.set_footer(text="ZenYukti Jobs")

        return embed
