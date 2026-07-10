from careers_engine.sources.base import BaseSource
from careers_engine.sources.upstream import UpstreamSource

__all__ = [
    "BaseSource",
    "UpstreamSource",
]


def get_sources() -> list[BaseSource]:
    """Return all enabled job sources."""

    return [
        UpstreamSource(),
    ]
