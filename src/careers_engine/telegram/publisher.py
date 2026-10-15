from __future__ import annotations

import asyncio
from html import escape
from typing import TYPE_CHECKING

import httpx

from careers_engine.config import (
    REQUEST_TIMEOUT,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from careers_engine.models import Job
from careers_engine.publishing import JobPublisher

if TYPE_CHECKING:
    from careers_engine.storage import PublishHistory


class TelegramPublisher(JobPublisher):
    """Publish jobs to a Telegram chat."""

    def __init__(
        self,
        bot_token: str = TELEGRAM_BOT_TOKEN,
        chat_id: str = TELEGRAM_CHAT_ID,
        history: PublishHistory | None = None,
    ) -> None:
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured.")

        if not chat_id:
            raise ValueError("TELEGRAM_CHAT_ID is not configured.")

        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.chat_id = chat_id
        self.history = history

    @staticmethod
    def format_message(job: Job) -> str:
        """Format a job as an HTML Telegram message."""

        lines = [
            f"<b>{escape(job.company)}</b>",
            f"<b>{escape(job.role)}</b>",
            "",
            f"<b>Location:</b> {escape(job.location)}",
            f"<b>Role Type:</b> {escape(job.employment_type.value)}",
        ]

        if job.deadline:
            lines.append(f"<b>Deadline:</b> {escape(job.deadline)}")

        if job.stipend:
            lines.append(f"<b>Stipend:</b> {escape(job.stipend)}")

        if job.eligibility:
            lines.append(f"<b>Eligibility:</b> {escape(job.eligibility)}")

        if job.description:
            lines.extend(["", escape(job.description)])

        lines.extend(
            [
                "",
                f'<a href="{escape(job.apply_url, quote=True)}">Apply Here</a>',
                "",
                "<i>Powered by ZenYukti</i>",
            ]
        )

        return "\n".join(lines)

    async def publish(self, jobs: list[Job]) -> None:
        """Publish jobs sequentially and persist successful deliveries."""

        if not jobs:
            return

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            for job in jobs:
                retries = 0
                while True:
                    response = await client.post(
                        self.api_url,
                        json={
                            "chat_id": self.chat_id,
                            "text": self.format_message(job),
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                        },
                    )

                    if response.status_code == 429:
                        result = response.json()
                        retry_after = result.get("parameters", {}).get("retry_after")

                        if (
                            isinstance(retry_after, bool)
                            or not isinstance(retry_after, (int, float))
                            or retry_after < 0
                        ):
                            raise RuntimeError(
                                "Telegram rate-limited the request without "
                                "providing a valid retry_after value."
                            )

                        if retries >= 5:
                            raise RuntimeError(
                                f"Telegram rate limit persisted after 5 retries "
                                f"for job {job.identifier}."
                            )

                        retries += 1
                        await asyncio.sleep(retry_after)
                        continue

                    response.raise_for_status()

                    result = response.json()
                    if not result.get("ok", False):
                        raise RuntimeError(
                            f"Telegram rejected job {job.identifier}: "
                            f"{result.get('description', 'unknown error')}"
                        )

                    if self.history is not None:
                        self.history.mark_published([job])

                    break
