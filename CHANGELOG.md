# Changelog

## [0.2.0] - 2026-05-27

### Added
- Async execution boundary support
- Structured audit backends (SQLite, InMemory, Stdout, Null)
- Policy composition operators (AND, OR, NOT)
- ExecutionContext and PolicyDecision dataclasses
- Correlation ID tracking
- LangGraph integration example
- Comprehensive test suite
- GitHub Actions CI
- Type hints and py.typed marker

### Changed
- Refactored audit logging to use pluggable backends
- Improved error context in BoundaryViolation
- UTC-aware timestamps throughout

### Fixed
- Function metadata preservation with functools.wraps
- Async cancellation propagation

## [0.1.0] - 2026-05-25

### Added
- Initial release
- Basic boundary decorator
- Exact match policy
- Simple audit logging
