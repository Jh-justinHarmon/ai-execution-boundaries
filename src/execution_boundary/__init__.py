"""Execution boundaries for AI agents with write access."""

from .boundary import boundary
from .policy import Policy
from .async_boundary import async_boundary, ComposablePolicy, PolicyFactory

# Core primitives
from .core import ExecutionContext, PolicyDecision, BoundaryViolation

# Audit backends
from .audit import (
    AuditBackend,
    NullBackend,
    InMemoryBackend,
    SQLiteBackend,
    StdoutBackend
)

__version__ = "0.2.0"
__all__ = [
    # Decorators
    "boundary",
    "async_boundary",
    # Core
    "ExecutionContext",
    "PolicyDecision",
    "BoundaryViolation",
    # Policy
    "Policy",
    "ComposablePolicy",
    "PolicyFactory",
    # Audit
    "AuditBackend",
    "NullBackend",
    "InMemoryBackend",
    "SQLiteBackend",
    "StdoutBackend",
]
