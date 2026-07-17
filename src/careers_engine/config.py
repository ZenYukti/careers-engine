from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "ZenYukti Jobs"

DATA_DIR = Path("data")

JOBS_FILE = DATA_DIR / "jobs.json"
HISTORY_FILE = DATA_DIR / "history.json"
CACHE_DIR = DATA_DIR / "cache"

REQUEST_TIMEOUT = 20

USER_AGENT = "ZenYukti Jobs/0.1 (https://github.com/ZenYukti/careers-engine)"

UPSTREAM_REPOSITORY = "speedyapply/2027-SWE-College-Jobs"

UPSTREAM_BRANCH = "main"

UPSTREAM_FILES = [
    "INTERN_INTL.md",
    "NEW_GRAD_INTL.md",
]

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")

DISCORD_CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID", "0"))
