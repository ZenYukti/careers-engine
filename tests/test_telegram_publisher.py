from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from careers_engine.models import Job
from careers_engine.telegram import TelegramPublisher


@pytest.fixture
def job() -> Job:
    return Job(
        company="Google & Co",
        role="Software Engineer Intern",
        location="India",
        apply_url="https://example.com/apply?a=1&b=2",
        eligibility="Students graduating in 2028",
        stipend="Competitive",
    )


def test_format_message_escapes_html(job: Job) -> None:
    message = TelegramPublisher.format_message(job)

    assert "Google &amp; Co" in message
    assert "Software Engineer Intern" in message
    assert "Students graduating in 2028" in message
    assert "https://example.com/apply?a=1&amp;b=2" in message


def test_missing_configuration() -> None:
    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        TelegramPublisher(bot_token="", chat_id="@zenyuktijobs")

    with pytest.raises(ValueError, match="TELEGRAM_CHAT_ID"):
        TelegramPublisher(bot_token="test-token", chat_id="")


@pytest.mark.asyncio
async def test_publish_job(job: Job) -> None:
    publisher = TelegramPublisher("test-token", "@zenyuktijobs")

    response = MagicMock()
    response.json.return_value = {"ok": True}
    response.raise_for_status.return_value = None

    with patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client:
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(return_value=response)

        await publisher.publish([job])

        client_instance.post.assert_awaited_once()
        payload = client_instance.post.await_args.kwargs["json"]

        assert payload["chat_id"] == "@zenyuktijobs"
        assert payload["parse_mode"] == "HTML"
        assert "Google &amp; Co" in payload["text"]


@pytest.mark.asyncio
async def test_publish_raises_on_http_failure(job: Job) -> None:
    publisher = TelegramPublisher("test-token", "@zenyuktijobs")

    with patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client:
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(side_effect=httpx.ConnectError("connection failed"))

        with pytest.raises(httpx.ConnectError):
            await publisher.publish([job])


@pytest.mark.asyncio
async def test_publish_raises_on_telegram_api_rejection(job: Job) -> None:
    publisher = TelegramPublisher("test-token", "@zenyuktijobs")

    response = MagicMock()
    response.json.return_value = {
        "ok": False,
        "description": "Bot was blocked by the user",
    }
    response.raise_for_status.return_value = None

    with patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client:
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(return_value=response)

        with pytest.raises(RuntimeError, match="Bot was blocked by the user"):
            await publisher.publish([job])


@pytest.mark.asyncio
async def test_publish_empty_list_makes_no_requests() -> None:
    publisher = TelegramPublisher("test-token", "@zenyuktijobs")

    with patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client:
        await publisher.publish([])

        client.assert_not_called()


@pytest.mark.asyncio
async def test_publish_retries_after_rate_limit(job: Job) -> None:
    publisher = TelegramPublisher(bot_token="token", chat_id="-100123")
    history = MagicMock()
    publisher.history = history

    rate_limited = MagicMock()
    rate_limited.status_code = 429
    rate_limited.json.return_value = {
        "ok": False,
        "parameters": {"retry_after": 2},
    }

    success = MagicMock()
    success.status_code = 200
    success.json.return_value = {"ok": True, "result": {"message_id": 1}}

    with (
        patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client,
        patch(
            "careers_engine.telegram.publisher.asyncio.sleep",
            new_callable=AsyncMock,
        ) as sleep,
    ):
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(side_effect=[rate_limited, success])

        await publisher.publish([job])

        sleep.assert_awaited_once_with(2)
        assert client_instance.post.await_count == 2
        history.mark_published.assert_called_once_with([job])


@pytest.mark.asyncio
async def test_publish_records_each_success_immediately(
    job: Job,
) -> None:
    second_job = Job(
        company="Example",
        role="Software Engineer Intern",
        location="India",
        apply_url="https://example.com/second",
    )
    publisher = TelegramPublisher(bot_token="token", chat_id="-100123")
    history = MagicMock()
    publisher.history = history

    success = MagicMock()
    success.status_code = 200
    success.json.return_value = {"ok": True}

    failure = MagicMock()
    failure.status_code = 429
    failure.json.return_value = {
        "ok": False,
        "parameters": {"retry_after": "invalid"},
    }

    with (
        patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client,
        patch(
            "careers_engine.telegram.publisher.asyncio.sleep",
            new_callable=AsyncMock,
        ) as sleep,
    ):
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(side_effect=[success, failure])

        with pytest.raises(RuntimeError, match="retry_after"):
            await publisher.publish([job, second_job])

    history.mark_published.assert_called_once_with([job])
    sleep.assert_not_awaited()


@pytest.mark.asyncio
async def test_publish_without_history_remains_supported(job: Job) -> None:
    publisher = TelegramPublisher(bot_token="token", chat_id="-100123")

    success = MagicMock()
    success.status_code = 200
    success.json.return_value = {"ok": True}

    with patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client:
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(return_value=success)

        await publisher.publish([job])

        client_instance.post.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_raises_after_exhausted_rate_limit_retries(
    job: Job,
) -> None:
    publisher = TelegramPublisher(bot_token="token", chat_id="-100123")
    history = MagicMock()
    publisher.history = history

    rate_limited = MagicMock()
    rate_limited.status_code = 429
    rate_limited.json.return_value = {
        "ok": False,
        "parameters": {"retry_after": 1},
    }

    with (
        patch("careers_engine.telegram.publisher.httpx.AsyncClient") as client,
        patch(
            "careers_engine.telegram.publisher.asyncio.sleep",
            new_callable=AsyncMock,
        ) as sleep,
    ):
        client_instance = client.return_value.__aenter__.return_value
        client_instance.post = AsyncMock(
            return_value=rate_limited,
        )

        with pytest.raises(
            RuntimeError,
            match="rate limit persisted after 5 retries",
        ):
            await publisher.publish([job])

        # One initial request plus five retries.
        assert client_instance.post.await_count == 6
        assert sleep.await_count == 5
        sleep.assert_awaited_with(1)

    # A job is recorded only after a successful delivery.
    history.mark_published.assert_not_called()
