from __future__ import annotations

import discord

from careers_engine.company import COMPANY_BRANDS, DEFAULT_BRAND
from careers_engine.models import Job


class JobFormatter:
    """Convert a Job into a Discord embed."""

    def format(self, job: Job) -> discord.Embed:
        brand = COMPANY_BRANDS.get(
            job.company,
            DEFAULT_BRAND,
        )

        embed = discord.Embed(
            title=job.role,
            url=job.apply_url,
            color=brand.color,
        )

        # update the embed to keep company directly without label

        # embed.add_field(
        #     name="Company",
        #     value=job.company,
        #     inline=False,
        # )

        embed.set_author(
            name=job.company,
        )

        embed.add_field(
            name="Location",
            value=job.location,
            inline=True,
        )

        embed.add_field(
            name="Role Type",
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

        # embed.add_field(
        #     name="🔗 Apply",
        #     value=f"[Apply Here]({job.apply_url})",
        #     inline=False,
        # )

        # hiding the apply label

        embed.add_field(
            name="\u200b",  # Invisible field name
            value=f"🔗 **[Apply Here]({job.apply_url})**",
            inline=False,
        )

        embed.set_footer(text="Powered by ZenYukti Jobs")

        return embed
