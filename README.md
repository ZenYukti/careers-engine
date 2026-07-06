# Careers Engine

> Intelligent job aggregation and publishing platform powering **ZenYukti Jobs**.

## Overview

Careers Engine automatically discovers software engineering opportunities, filters and enriches them, and publishes high-quality job updates to the [ZenYukti Discord community](https://go.zenyukti.in/discord/).

Current focus:
- 🇮🇳 India internships
- Software Engineering and other Engg. roles (SWE/SDE/AMTS/MRS/SRE/FDE etc)
- Discord publishing

Future scope:
- Hackathons
- Fellowships
- Scholarships
- Career programs

## Architecture

```
External Sources
        │
        ▼
     Fetcher
        │
        ▼
      Parser
        │
        ▼
  Filter Engine
        │
        ▼
    Job Store
        │
        ▼
    Publisher
        │
        ▼
 Discord (ZenYukti Jobs)
```

## Tech Stack

| Component          | Technology            |
| ------------------ | --------------------- |
| Language           | Python 3.13           |
| Dependency Manager | uv                    |
| Formatting         | Ruff                  |
| Typing             | mypy                  |
| Scheduler          | GitHub Actions        |
| HTTP               | httpx                 |
| HTML Parsing       | BeautifulSoup4 / lxml |
| Models             | Pydantic              |
| Discord            | discord.py            |
| Config             | YAML                  |
| Testing            | pytest                |

## Repository Structure

```
src/
tests/
docs/
data/
```

## Status

Under active development.

---

### Branch Flow
                main
                  │
        ┌─────────┴─────────┐
        │                   │
Development             GitHub Actions
(Ayush)                   (Bot)

        │                   │
        ▼                   ▼
  Source Code         data branch

                             │
                             ▼
                         jobs.json
                         history.json
                         cache.json

The workflow would be:

1) GitHub Actions checks out the `data` branch.
2) Updates `jobs.json` and `history.json`.
3) Commits as github-actions[bot].
4) Publishes the digest to Discord.
5) Your main branch remains focused on source code and documentation.