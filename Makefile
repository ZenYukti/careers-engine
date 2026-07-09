.PHONY: install format lint typecheck test check clean

install:
	uv sync

format:
	uv run ruff format .

lint:
	uv run ruff check . --fix

typecheck:
	uv run mypy src

test:
	uv run pytest

run:
	uv run python -m careers_engine.pipeline.runner

collect:
	uv run python -m careers_engine.pipeline.collect

publish:
	uv run python -m careers_engine.pipeline.publish

check: lint format typecheck test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +