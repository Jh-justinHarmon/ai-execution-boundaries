"""In-memory audit backend for testing."""

import asyncio
from dataclasses import dataclass
from typing import List

from ..core import ExecutionContext, PolicyDecision


@dataclass(frozen=True)
class AuditRecord:
    """Single audit record."""
    context: ExecutionContext
    decision: PolicyDecision


class InMemoryBackend:
    """
    In-memory audit backend for testing.
    
    Thread-safe storage of audit records.
    Queryable for test assertions.
    """
    
    def __init__(self) -> None:
        self._records: List[AuditRecord] = []
        self._lock = asyncio.Lock()
    
    async def record(self, context: ExecutionContext, decision: PolicyDecision) -> None:
        """Record audit event in memory."""
        async with self._lock:
            self._records.append(AuditRecord(context=context, decision=decision))
    
    @property
    def records(self) -> List[AuditRecord]:
        """Get all recorded audit events."""
        return list(self._records)
    
    def clear(self) -> None:
        """Clear all records."""
        self._records.clear()
    
    def find_by_correlation_id(self, correlation_id: str) -> List[AuditRecord]:
        """Find records by correlation ID."""
        return [r for r in self._records if r.context.correlation_id == correlation_id]
    
    def find_allowed(self) -> List[AuditRecord]:
        """Find all allowed decisions."""
        return [r for r in self._records if r.decision.is_allowed]
    
    def find_denied(self) -> List[AuditRecord]:
        """Find all denied decisions."""
        return [r for r in self._records if r.decision.is_denied]
