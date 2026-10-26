from careers_engine.sources.ashby import AshbySource
from careers_engine.sources.base import BaseSource
from careers_engine.sources.simplify import SimplifySource
from careers_engine.sources.upstream import UpstreamSource

__all__ = [
    "AshbySource",
    "BaseSource",
    "SimplifySource",
    "UpstreamSource",
]


def get_sources() -> list[BaseSource]:
    """Return all enabled job sources."""

    return [
        UpstreamSource(),
        SimplifySource(),
        AshbySource(),
    ]
