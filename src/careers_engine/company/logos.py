from __future__ import annotations

from careers_engine.company.slugs import COMPANY_SLUGS

LOGO_BASE_URL = "https://raw.githubusercontent.com/ZenYukti/careers-engine/main/assets/logos"


def get_logo_url(company: str) -> str | None:
    slug = COMPANY_SLUGS.get(company)

    if slug is None:
        return None

    return f"{LOGO_BASE_URL}/{slug}.png"
