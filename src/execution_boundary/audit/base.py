"""Audit backend protocol."""

from typing import Protocol

from ..core import ExecutionContext, PolicyDecision


class AuditBackend(Protocol):
    """
    Protocol for audit backends.
    
    Implementations must provide async record() method.
    """
    
    async def record(self, context: ExecutionContext, decision: PolicyDecision) -> None:
        """
        Record an audit event.
        
        Args:
            context: Execution context
            decision: Policy decision
        """
        ...
