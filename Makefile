.PHONY: test coverage typecheck lint clean install help

help:
	@echo "Available targets:"
	@echo "  make test       - Run all tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make typecheck  - Run mypy type checking"
	@echo "  make lint       - Run ruff linting"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make install    - Install package in development mode"

install:
	pip install -e ".[dev]"

test:
	PYTHONPATH=src python3 -m pytest tests/ -v

coverage:
	PYTHONPATH=src python3 -m pytest tests/ --cov=execution_boundary --cov-report=term-missing --cov-report=html

typecheck:
	python3 -m mypy src/execution_boundary

lint:
	python3 -m ruff check src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
