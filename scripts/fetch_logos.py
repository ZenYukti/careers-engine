from __future__ import annotations

from pathlib import Path

import cairosvg
import httpx

from careers_engine.company.slugs import COMPANY_SLUGS

ICON_BASE_URL = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons"

OUTPUT_DIR = Path("assets/logos")


def download_logo(slug: str) -> bytes:
    response = httpx.get(
        f"{ICON_BASE_URL}/{slug}.svg",
        timeout=20,
    )

    response.raise_for_status()

    return response.content


def save_logo(slug: str, svg: bytes) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = OUTPUT_DIR / f"{slug}.png"

    cairosvg.svg2png(
        bytestring=svg,
        write_to=str(destination),
        output_width=64,
        output_height=64,
    )


def main() -> None:
    downloaded = 0
    skipped = 0

    for company, slug in COMPANY_SLUGS.items():
        destination = OUTPUT_DIR / f"{slug}.png"

        if destination.exists():
            print(f"Skipping {company}")
            skipped += 1
            continue

        print(f"Downloading {company}")

        try:
            svg = download_logo(slug)
            save_logo(slug, svg)

            downloaded += 1

            print(f"✓ {company}")

        except Exception as exc:
            print(f"✗ {company}: {exc}")

    print()

    print(f"Downloaded : {downloaded}")
    print(f"Skipped    : {skipped}")


if __name__ == "__main__":
    main()
