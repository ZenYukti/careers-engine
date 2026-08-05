<center>

<picture>
  <source srcset="docs/images/careers-engine-nav-dark-removebg-preview.png" media="(prefers-color-scheme: dark)">
  <source srcset="docs/images/careers-engine-nav-bright-removebg-preview.png" media="(prefers-color-scheme: light)">
  <!-- following is for a fallback; if mode (dark/bright) fails to fetch & load -->
  <img src="docs/images/careers-engine-nav-bright.png" alt="Ayush Hardeniya Banner" style="width:100%; border-radius:10px;" />
</picture>

<p align="center">
  <strong>
    Intelligent job aggregation and publishing platform powering ZenYukti Jobs on
    <a href="https://go.zenyukti.in/discord">Discord</a>.
  </strong>
</p>

<p align="center">
  <a href="https://careers-engine.zenyukti.in">
    <img src="https://img.shields.io/badge/Documentation-Live-2563EB?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Documentation">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-16A34A?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <a href="https://github.com/ZenYukti">
  <img src="https://img.shields.io/badge/ZenYukti-Ecosystem-7C3AED?style=for-the-badge" alt="ZenYukti Ecosystem">
</a>
</p>

[Docs](https://careers-engine.zenyukti.in) • [Contributing](CONTRIBUTING.md) • [License](LICENSE)

</center>

---

## Overview

**careers-engine** is an open source backend that continuously discovers software engineering opportunities, normalizes and enriches the collected data, and publishes newly discovered opportunities through automated workflows.

The project eliminates manual tracking of company career pages by providing a reproducible pipeline for job discovery, storage, and publishing. It currently powers **ZenYukti Jobs**, while remaining modular enough to support additional sources, publishers, and deployment environments.

---

## Architecture

![careers-engine Architecture](docs/images/careers-engine-architecture.png)

**Interactive architecture diagram**:

https://excalidraw.com/#json=foywzC6vYJtpt6wl_DKTE,T7vPnfxrNQHoC7OuYd6eAA

For a detailed explanation of the system architecture and individual components, see the [project documentation](https://careers-engine.zenyukti.in/architecture/overview).

---

## Features

- Automated job discovery from supported career sources
- Intelligent normalization and metadata enrichment
- Employment type inference
- Company branding with logos and accent colors
- Duplicate detection and publish history
- Automated Discord publishing
- GitHub Actions based automation
- Extensible source, parser, and publisher architecture
- Comprehensive testing and static analysis

---

## Supported Companies

The platform currently tracks software engineering opportunities from leading technology companies, including:

Google • Microsoft • Amazon • Apple • Meta

NVIDIA • OpenAI • Anthropic • Stripe • Databricks

Cloudflare • GitHub • Atlassian • Adobe • Salesforce

Uber • Airbnb • Flipkart • Razorpay • Zoho

…and many more.

---

## Technology Stack

| Component | Technology |
| ---------- | ---------- |
| Language | Python 3.12 |
| Package Management | uv |
| CI/CD | GitHub Actions |
| Storage | JSON |
| Publisher | Discord API |
| Assets | Simple Icons |
| Testing | pytest |
| Linting | Ruff |
| Type Checking | mypy |

---

## Getting Started

### Requirements

- Python 3.12 or newer
- uv
- Git

Clone the repository.

```bash
git clone https://github.com/ZenYukti/careers-engine.git
cd careers-engine
```

Install project dependencies.

```bash
uv sync
```

See the [project documentation](https://careers-engine.zenyukti.in/getting-started/) to get started.

---

## Documentation

Project documentation is available at **https://careers-engine.zenyukti.in**.

The documentation is maintained under the `docs/` directory and is powered by [Mintlify](https://mintlify.com).

---

## Repository Structure

```text
.
├── assets/                 Static assets
├── docs/                   Project documentation
├── scripts/                CLI utilities and automation
├── src/
│   └── careers_engine/     Core application
├── tests/                  Test suite
├── .github/workflows/      CI and scheduled workflows
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions, bug reports, and feature requests are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
---

<p align="center">
  <a href="https://zenyukti.in">
    <img src="https://img.shields.io/badge/Maintained%20by-ZenYukti-2563EB?style=for-the-badge" alt="Maintained by ZenYukti">
  </a>
</p>
