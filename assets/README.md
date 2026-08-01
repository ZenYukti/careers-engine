# Assets

Source:
- https://github.com/simple-icons/simple-icons

---

The logo generator downloads icons from the **Simple Icons CDN**
(`jsDelivr`) instead of the GitHub repository to avoid breakage
caused by changes to the upstream development branch.

Logos are generated using:

```bash
uv run scripts/fetch_logos.py
```

The script downloads icons from:

```python
ICON_BASE_URL = (
    "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons"
)
```

---

> Do not edit the generated PNGs manually.
