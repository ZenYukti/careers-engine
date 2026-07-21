from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyMetadata:
    """Visual branding information for a company."""

    color: int
