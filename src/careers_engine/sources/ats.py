from __future__ import annotations

import json
import logging

import httpx

from careers_engine.fetchers.base import BaseFetcher

logger = logging.getLogger(__name__)


async def fetch_board_json(
    fetcher: BaseFetcher,
    url: str,
    provider: str,
    board: str,
) -> dict | list | None:
    """Fetch a board's JSON response without interrupting other boards."""

    try:
        content = await fetcher.fetch(url)
        data = json.loads(content)

        if not isinstance(data, (dict, list)):
            logger.warning(
                "Skipping %s board %s: unexpected response format",
                provider,
                board,
            )
            return None

        return data

    except (httpx.HTTPError, json.JSONDecodeError) as exc:
        logger.warning(
            "Skipping %s board %s: %s",
            provider,
            board,
            exc,
        )
        return None
