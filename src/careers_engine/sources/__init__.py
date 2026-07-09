from careers_engine.sources.base import BaseSource
from careers_engine.sources.private import PrivateSource

__all__ = [
    "BaseSource",
    "PrivateSource",
]


def get_sources() -> list[BaseSource]:
    """Return all enabled job sources."""

    return [
        PrivateSource(),
    ]
