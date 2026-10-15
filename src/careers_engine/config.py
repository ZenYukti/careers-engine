from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

APP_NAME = "ZenYukti Jobs"

DATA_DIR = Path(
    os.environ.get(
        "DATA_DIR",
        "data",
    )
)

# JOBS_FILE = DATA_DIR / "jobs.json"
# HISTORY_FILE = DATA_DIR / "history.json"
# CACHE_DIR = DATA_DIR / "cache"

# Update the directory structure of careers-data; these variables
# have been modified accordingly.
# TODO: Remove the above comments after the Telegram publishing
# channel is confirmed working with GitHub Actions workflows.

JOBS_FILE = DATA_DIR / "jobs.json"
DELIVERY_HISTORY_DIR = DATA_DIR / "delivery-history"
DISCORD_HISTORY_FILE = DELIVERY_HISTORY_DIR / "discord.json"
TELEGRAM_HISTORY_FILE = DELIVERY_HISTORY_DIR / "telegram.json"
CACHE_DIR = DATA_DIR / "cache"

QUEUE_FILE = DATA_DIR / "queue.json"

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

# Restrict publishing to a single Discord server
DISCORD_GUILD_ID = int(os.environ.get("DISCORD_GUILD_ID", "0"))

# telegram publishing channel
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# to be updated, when fetch_logos.py is run and assets/logos directory is updated
# i.e) new version ro new images are downloaded
# syntax: 1.0 -> 2.0 -> 3.0 -> 4.0... so on

LOGO_VERSION = "3.0"
