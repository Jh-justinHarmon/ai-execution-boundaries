"""Null audit backend (zero-cost no-op)."""

from ..core import ExecutionContext, PolicyDecision


class NullBackend:
    """
    Zero-cost no-op audit backend.
    
    Use when audit logging is not required.
    This is the default backend for minimal overhead.
    """
    
    async def record(self, context: ExecutionContext, decision: PolicyDecision) -> None:
        """No-op record implementation."""
        pass
