from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).with_name("ats_registry.json")


def get_boards(provider: str) -> list[dict[str, Any]]:
    with REGISTRY_PATH.open(encoding="utf-8") as file:
        registry = json.load(file)

    return registry["boards"].get(provider, [])
