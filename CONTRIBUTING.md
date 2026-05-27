# Contributing to execution-boundary

## Development Setup

**1. Clone the repository:**

```bash
git clone https://github.com/Jh-justinHarmon/ai-execution-boundaries
cd ai-execution-boundaries
```

**2. Install development dependencies:**

```bash
pip install -e ".[dev]"
```

**3. Verify setup:**

```bash
make test
```

## Running Tests

**All tests:**

```bash
make test
```

**With coverage:**

```bash
make coverage
```

**Specific test file:**

```bash
pytest tests/test_core.py -v
```

## Type Checking

```bash
make typecheck
```

## Code Style

```bash
make lint
```

## Development Workflow

1. Create a branch for your changes
2. Write tests for new functionality
3. Ensure all tests pass (`make test`)
4. Ensure type checks pass (`make typecheck`)
5. Ensure linting passes (`make lint`)
6. Submit a pull request

## Testing Guidelines

- Write tests for all new features
- Maintain or improve test coverage
- Use `InMemoryBackend` for test audit backends
- Test both sync and async code paths
- Test error conditions and edge cases

## Code Style Guidelines

- Follow PEP 8
- Use type hints for all public APIs
- Keep functions focused and small
- Prefer composition over inheritance
- Document public APIs with docstrings

## What to Contribute

**Welcome:**
- Bug fixes with tests
- Documentation improvements
- New policy types (with tests)
- Performance improvements (with benchmarks)
- Integration examples

**Not accepting:**
- New orchestration features
- UI components
- Policy DSLs
- Distributed systems features
- Breaking API changes without discussion

## Questions?

Open an issue for discussion before starting major work.
