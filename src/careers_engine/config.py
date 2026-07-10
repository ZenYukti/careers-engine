from pathlib import Path

APP_NAME = "ZenYukti Jobs"

DATA_DIR = Path("data")

JOBS_FILE = DATA_DIR / "jobs.json"
HISTORY_FILE = DATA_DIR / "history.json"
CACHE_DIR = DATA_DIR / "cache"

REQUEST_TIMEOUT = 20

USER_AGENT = "ZenYukti Jobs/0.1 (https://github.com/ZenYukti/careers-engine)"
