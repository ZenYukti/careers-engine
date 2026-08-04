# Contributing to careers-engine

Thank you for your interest in contributing to careers-engine.

Whether you're fixing a bug, improving documentation, adding a new source, or proposing a new feature, all contributions are welcome.

## Development setup

Clone the repository and install the project dependencies.

```bash
git clone https://github.com/ZenYukti/careers-engine.git
cd careers-engine

uv sync
```

Run the full development checks before opening a pull request.

```bash
make check
```

This runs formatting, static analysis, type checking, and the test suite.

## Development workflow

Create a new branch from `main`.

```bash
git checkout -b feat/my-feature
```

Keep pull requests focused on a single change. Smaller PRs are easier to review and merge.

When making changes:

- Add or update tests where appropriate.
- Update documentation if user-facing behavior changes.
- Ensure `make check` passes before pushing.

## Commit messages

Follow Conventional Commits where possible.

Examples:

```text
feat(parser): support new upstream format
fix(storage): preserve published jobs
docs: improve installation guide
refactor(employment): simplify inference rules
test(parser): cover malformed markdown tables
```

## Reporting issues

If you find a bug, please include:

- expected behavior
- actual behavior
- reproduction steps
- relevant logs or screenshots, if applicable

If you're proposing a feature, explain the motivation and expected behavior.

## Documentation

Documentation lives alongside the source code in the `docs/` directory.

When changing behavior, update the corresponding documentation whenever possible.

## Questions

If you're unsure about an implementation or want feedback before starting work, feel free to open an issue or start a discussion before submitting a pull request.

Thank you for helping improve careers-engine.