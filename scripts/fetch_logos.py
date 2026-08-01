from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import cairosvg
import httpx

from careers_engine.company.slugs import COMPANY_SLUGS

ICON_BASE_URL = (
    "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons"
)

OUTPUT_DIR = Path("assets/logos")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--force",
    action="store_true",
    help="Re-download and regenerate existing logos.",
)
args = parser.parse_args()


def download_logo(slug: str) -> bytes:
    response = httpx.get(
        f"{ICON_BASE_URL}/{slug}.svg",
        timeout=20,
    )

    response.raise_for_status()

    return response.content


def colorize_svg(svg: bytes) -> bytes:
    """Render all logos in white for better visibility on Discord."""

    text = svg.decode("utf-8")

    text = text.replace(
        "<path",
        '<path fill="#F5F5F5"',
    )

    return text.encode("utf-8")


def save_logo(slug: str, svg: bytes) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = OUTPUT_DIR / f"{slug}.png"

    svg = colorize_svg(svg)

    cairosvg.svg2png(
        bytestring=svg,
        write_to=str(destination),
        output_width=128,
        output_height=128,
    )


def main() -> None:
    downloaded = 0
    skipped = 0

    missing: list[tuple[str, str]] = []

    for company, slug in COMPANY_SLUGS.items():
        destination = OUTPUT_DIR / f"{slug}.png"

        if destination.exists() and not args.force:
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
            missing.append((company, slug))
            print(f"✗ {company}: {exc}")

    print()
    print(f"Downloaded : {downloaded}")
    print(f"Skipped    : {skipped}")

    if missing:
        print()
        print("=" * 60)
        print("Missing logos:")
        print()

        for company, slug in missing:
            print(f"  • {company:<15} -> {slug}")

        print("=" * 60)

    result = subprocess.run(
        ["git", "diff", "--quiet", "--", "assets/logos"],
    )

    if result.returncode == 1:
        print()
        print("=" * 60)
        print("Logo assets have changed.")
        print("Remember to increment ASSETS_VERSION in config.py")
        print("before committing so Discord refreshes cached logos.")
        print("=" * 60)


if __name__ == "__main__":
    main()