# Makefile — turns multi-line commands into single words.
# `make test` is easier to remember (and harder to get wrong) than the full pytest invocation.
# Run `make help` to see everything available.

.PHONY: help setup data pipeline test lint format clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup:  ## Install the package + dev tools in editable mode
	pip install -e ".[dev]"
	pre-commit install

data:  ## Generate the bundled toy dataset
	python scripts/download_data.py

pipeline:  ## Run the full analysis pipeline end-to-end
	python scripts/run_pipeline.py

test:  ## Run the test suite with coverage
	pytest

lint:  ## Check code style without changing files
	ruff check src tests

format:  ## Auto-fix style and sort imports
	ruff check --fix src tests
	ruff format src tests

clean:  ## Remove caches and generated artifacts
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f data/processed/*.csv
