from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from careers_engine.models import Job
from scripts import publish


@pytest.fixture
def job() -> Job:
    return Job(
        company="Acme",
        role="Backend Intern",
        location="India",
        apply_url="https://example.com/apply",
    )


@pytest.mark.asyncio
async def test_publishes_to_both_destinations(job: Job) -> None:
    automatic_database = MagicMock()
    automatic_database.load.return_value = [job]

    queue_database = MagicMock()
    queue_database.load.return_value = []

    discord_history = MagicMock()
    discord_history.unpublished.return_value = [job]

    telegram_history = MagicMock()
    telegram_history.unpublished.return_value = [job]

    with (
        patch.object(
            publish,
            "JobDatabase",
            side_effect=[automatic_database, queue_database],
        ),
        patch.object(
            publish,
            "PublishHistory",
            side_effect=[discord_history, telegram_history],
        ),
        patch.object(publish, "DiscordClient") as discord_client,
        patch.object(publish, "TelegramPublisher") as telegram_publisher,
    ):
        discord_client.return_value.start_client = AsyncMock()
        telegram_publisher.return_value.publish = AsyncMock()

        await publish.main()

        discord_client.return_value.start_client.assert_awaited_once()
        telegram_publisher.return_value.publish.assert_awaited_once_with([job])
        discord_history.mark_published.assert_called_once_with([job])


@pytest.mark.asyncio
async def test_preserves_queue_when_destination_fails(job: Job) -> None:
    automatic_database = MagicMock()
    automatic_database.load.return_value = []

    queue_database = MagicMock()
    queue_database.load.return_value = [job]

    history = MagicMock()
    history.unpublished.return_value = [job]

    with (
        patch.object(
            publish,
            "JobDatabase",
            side_effect=[automatic_database, queue_database],
        ),
        patch.object(publish, "PublishHistory", return_value=history),
        patch.object(publish, "DiscordClient") as discord_client,
        patch.object(publish, "TelegramPublisher") as telegram_publisher,
    ):
        discord_client.return_value.start_client = AsyncMock()
        telegram_publisher.return_value.publish = AsyncMock(
            side_effect=RuntimeError("Telegram unavailable")
        )

        with pytest.raises(RuntimeError, match="Publishing failed"):
            await publish.main()

        queue_database.save.assert_not_called()


@pytest.mark.asyncio
async def test_records_only_successful_destination_on_partial_failure(
    job: Job,
) -> None:
    automatic_database = MagicMock()
    automatic_database.load.return_value = []

    queue_database = MagicMock()
    queue_database.load.return_value = [job]

    discord_history = MagicMock()
    discord_history.unpublished.return_value = [job]

    telegram_history = MagicMock()
    telegram_history.unpublished.return_value = [job]

    with (
        patch.object(
            publish,
            "JobDatabase",
            side_effect=[automatic_database, queue_database],
        ),
        patch.object(
            publish,
            "PublishHistory",
            side_effect=[discord_history, telegram_history],
        ),
        patch.object(publish, "DiscordClient") as discord_client,
        patch.object(publish, "TelegramPublisher") as telegram_publisher,
    ):
        discord_client.return_value.start_client = AsyncMock()
        telegram_publisher.return_value.publish = AsyncMock(
            side_effect=RuntimeError("Telegram unavailable")
        )

        with pytest.raises(RuntimeError, match="Publishing failed"):
            await publish.main()

        discord_history.mark_published.assert_called_once_with([job])
        telegram_history.mark_published.assert_not_called()
        queue_database.save.assert_not_called()


@pytest.mark.asyncio
async def test_skips_publishing_when_all_jobs_are_already_published() -> None:
    automatic_database = MagicMock()
    automatic_database.load.return_value = []

    queue_database = MagicMock()
    queue_database.load.return_value = []

    with (
        patch.object(
            publish,
            "JobDatabase",
            side_effect=[automatic_database, queue_database],
        ),
        patch.object(
            publish,
            "PublishHistory",
        ) as history_class,
        patch.object(publish, "DiscordClient") as discord_client,
        patch.object(publish, "TelegramPublisher") as telegram_publisher,
    ):
        discord_history = MagicMock()
        discord_history.unpublished.return_value = []
        telegram_history = MagicMock()
        telegram_history.unpublished.return_value = []
        history_class.side_effect = [discord_history, telegram_history]

        await publish.main()

        discord_client.assert_not_called()
        telegram_publisher.assert_not_called()
        queue_database.save.assert_not_called()


@pytest.mark.asyncio
async def test_retries_only_failed_destination(job: Job) -> None:
    automatic_database = MagicMock()
    automatic_database.load.return_value = []

    queue_database = MagicMock()
    queue_database.load.return_value = [job]

    discord_published: set[str] = set()
    telegram_published: set[str] = set()

    discord_history = MagicMock()
    discord_history.unpublished.side_effect = lambda jobs: [
        item for item in jobs if item.apply_url not in discord_published
    ]
    discord_history.mark_published.side_effect = lambda jobs: discord_published.update(
        item.apply_url for item in jobs
    )

    telegram_history = MagicMock()
    telegram_history.unpublished.side_effect = lambda jobs: [
        item for item in jobs if item.apply_url not in telegram_published
    ]
    telegram_history.mark_published.side_effect = lambda jobs: telegram_published.update(
        item.apply_url for item in jobs
    )

    with (
        patch.object(
            publish,
            "JobDatabase",
            side_effect=[
                automatic_database,
                queue_database,
                automatic_database,
                queue_database,
            ],
        ),
        patch.object(
            publish,
            "PublishHistory",
            side_effect=[
                discord_history,
                telegram_history,
                discord_history,
                telegram_history,
            ],
        ),
        patch.object(publish, "DiscordClient") as discord_client,
        patch.object(publish, "TelegramPublisher") as telegram_publisher,
    ):
        discord_client.return_value.start_client = AsyncMock()
        telegram_client = telegram_publisher.return_value

        async def publish_telegram_jobs(jobs: list[Job]) -> None:
            if telegram_client.publish.await_count == 1:
                raise RuntimeError("Telegram unavailable")

            telegram_published.update(item.apply_url for item in jobs)

        telegram_client.publish = AsyncMock(
            side_effect=publish_telegram_jobs,
        )

        with pytest.raises(RuntimeError, match="Publishing failed"):
            await publish.main()

        queue_database.save.assert_not_called()
        assert job.apply_url in discord_published
        assert job.apply_url not in telegram_published

        await publish.main()

        discord_client.assert_called_once()
        discord_client.return_value.start_client.assert_awaited_once()
        assert telegram_client.publish.await_count == 2
        telegram_client.publish.assert_awaited_with([job])
        assert job.apply_url in telegram_published
        queue_database.save.assert_called_once_with([])
