import gzip
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

URL = (
    "https://raw.githubusercontent.com/"
    "moonie0201/ats-directory/main/companies.jsonl.gz"
)

PROVIDERS = {"ashby", "greenhouse", "lever"}

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "ZenYukti-Careers-Engine/1.0"},
)

with urllib.request.urlopen(request, timeout=60) as response:
    content = gzip.decompress(response.read())

records = [
    json.loads(line)
    for line in content.splitlines()
    if line.strip()
]

boards = [
    {
        "provider": row["provider"],
        "slug": row["slug"],
        "company_name": row.get("name"),
    }
    for row in records
    if row["provider"] in PROVIDERS
    and row["status"] == "ok"
]

# Remove duplicate provider/slug entries.
unique_boards = {
    (board["provider"], board["slug"]): board
    for board in boards
}
boards = list(unique_boards.values())

boards.sort(
    key=lambda row: (row["provider"], row["slug"].casefold())
)

grouped_boards = {
    provider: [
        {
            "slug": board["slug"],
            "company_name": board["company_name"],
        }
        for board in boards
        if board["provider"] == provider
    ]
    for provider in sorted(PROVIDERS)
}

registry = {
    "version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": {
        "name": "moonie0201/ats-directory",
        "url": URL,
        "license": "CC0-1.0",
    },
    "boards": grouped_boards,
}

output = Path("src/careers_engine/company/ats_registry.json")
output.write_text(json.dumps(registry, indent=2) + "\n")

print(f"Registry generated: {output}")
print(f"Total verified boards: {len(boards)}")

for provider, count in sorted(
    Counter(board["provider"] for board in boards).items()
):
    missing = sum(
        not board["company_name"]
        for board in boards
        if board["provider"] == provider
    )
    print(f"{provider}: {count} boards, {missing} missing names")
