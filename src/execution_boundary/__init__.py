"""Execution boundaries for AI agents with write access."""

from .boundary import boundary, BoundaryViolation
from .policy import Policy

# Async support
from .async_boundary import (
    async_boundary,
    AuditEvent,
    AuditBackend,
    SQLiteBackend,
    StdoutBackend,
    ComposablePolicy,
    PolicyFactory
)

__version__ = "0.2.0"
__all__ = [
    # Sync
    "boundary",
    "BoundaryViolation",
    "Policy",
    # Async
    "async_boundary",
    "AuditEvent",
    "AuditBackend",
    "SQLiteBackend",
    "StdoutBackend",
    "ComposablePolicy",
    "PolicyFactory"
]
