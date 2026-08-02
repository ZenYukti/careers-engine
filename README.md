# careers-engine

> Intelligent job aggregation and publishing platform powering **ZenYukti Jobs**.

careers-engine is an open source backend that continuously discovers software engineering opportunities, enriches them with additional metadata, and publishes them through automated workflows.

The project was built to eliminate manual tracking of career pages and provide a reliable pipeline for delivering high quality opportunities to the community. It currently powers **ZenYukti Jobs**, while remaining modular enough to support additional sources, publishers, and workflows in the future.

---

## Features

- Automated job ingestion from upstream repositories
- Manual opportunity queue for curated postings
- Company branding with logos and accent colors
- Employment type inference
- Duplicate detection and publish history
- Scheduled automation with GitHub Actions
- Modular source, parser, and publisher architecture
- Comprehensive test suite with static analysis

---

**careers-engine** continuously tracks software engineering opportunities from leading technology companies, including FAANG, enterprise software vendors, AI companies, cloud providers, and high-growth startups.

Some of the companies currently covered include:

```text
Google      Microsoft     Amazon      Apple      Meta
NVIDIA      OpenAI        Anthropic   Stripe     Databricks
Cloudflare  GitHub        Atlassian   Adobe      Salesforce
Uber        Airbnb        Flipkart    Razorpay   Zoho
```

and so on...

---

## Architecture

> to be put soon

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Package Management | uv |
| CI/CD | GitHub Actions |
| Storage | JSON |
| Publisher | Discord API |
| Assets | Simple Icons |
| Testing | pytest |
| Formatting & Linting | Ruff |
| Type Checking | mypy |

---

## Repository Structure

```text
.
├── assets/                 Company logos and static assets
├── docs/                   Project documentation
├── scripts/                CLI utilities and automation entrypoints
├── src/
│   └── careers_engine/     Core application
├── tests/                  Automated test suite
├── .github/workflows/      CI and scheduled workflows
├── pyproject.toml
└── README.md
```

---

## Getting Started

### Requirements

- Python 3.12 or newer
- uv
- Git

The project is primarily developed and tested on Ubuntu, but should work on any platform supported by Python and uv.

### Clone the repository

```bash
git clone https://github.com/ZenYukti/careers-engine.git
cd careers-engine
```

### Install dependencies

```bash
uv sync
```

---

## Configuration

Create a `.env` file containing the required environment variables.

```env
DISCORD_TOKEN=
DISCORD_CHANNEL_ID=
CAREERS_DATA_TOKEN=
```

Additional configuration options are documented in the project documentation.

---

## Running Locally

Collect opportunities from upstream sources.

```bash
uv run scripts/collect.py
```

Publish unpublished opportunities.

```bash
uv run scripts/publish.py
```

Queue a manual opportunity.

```bash
uv run scripts/queue_opportunity.py
```

Run all quality checks.

```bash
make check
```

---

## GitHub Actions

The project uses GitHub Actions to automate ingestion, publishing, and manual queue management.

### Ingest Jobs

Runs on a schedule (currently twice daily) or can be triggered manually.

```text
Upstream Sources
        │
        ▼
Collect Opportunities
        │
        ▼
Update careers-data/jobs.json
```

### Publish Jobs

Publishes only previously unpublished opportunities.

```text
careers-data
      │
      ▼
Compare against publish history
      │
      ▼
Generate Discord embeds
      │
      ▼
Publish to ZenYukti Jobs
```

### Queue Opportunity

Allows maintainers to add curated opportunities without modifying the source repositories.

```text
GitHub Actions
      │
      ▼
Queue Opportunity
      │
      ▼
queue.json
```

---

## Documentation

Project documentation is maintained alongside the source code in the `docs/` directory.

The long term documentation site will be available at:

**https://careers-engine.zenyukti.in**

Documentation will include:

- Getting Started
- Architecture
- Developer Guide
- Configuration
- Workflows
- API Reference
- Contribution Guide

---

## Roadmap

Current focus areas include:

- Additional upstream sources
- More publishing platforms
- Richer company branding
- Production documentation
- Public API
- Web dashboard

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the development workflow and contribution guidelines.

---

## License

This project is licensed under the **[MIT License](LICENSE)**.