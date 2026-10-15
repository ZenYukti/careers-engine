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
        client_instance.post = AsyncMock(
            side_effect=httpx.ConnectError("connection failed")
        )

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
