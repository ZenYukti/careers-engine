from careers_engine.sources.ashby import AshbySource
from careers_engine.sources.base import BaseSource
from careers_engine.sources.greenhouse import GreenhouseSource
from careers_engine.sources.lever import LeverSource
from careers_engine.sources.simplify import SimplifySource
from careers_engine.sources.upstream import UpstreamSource

__all__ = [
    "AshbySource",
    "BaseSource",
    "GreenhouseSource",
    "LeverSource()",
    "SimplifySource",
    "UpstreamSource",
]


def get_sources() -> list[BaseSource]:
    """Return all enabled job sources."""

    return [
        UpstreamSource(),
        SimplifySource(),
        AshbySource(),
        GreenhouseSource(),
    ]
