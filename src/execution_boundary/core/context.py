"""Execution context for boundary enforcement."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import uuid


@dataclass(frozen=True)
class ExecutionContext:
    """
    Context for a single boundary enforcement decision.
    
    Attributes:
        correlation_id: Unique identifier for this execution
        timestamp: UTC timestamp when execution was initiated
        tool_name: Name of the tool/function being executed
        execution_id: Unique identifier for this specific execution
        parent_execution_id: Optional parent execution ID for nested calls
        metadata: Additional context metadata
    """
    correlation_id: str
    timestamp: datetime
    tool_name: str
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_execution_id: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create(
        cls,
        tool_name: str,
        correlation_id: Optional[str] = None,
        parent_execution_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None
    ) -> "ExecutionContext":
        """Create a new execution context with defaults."""
        return cls(
            correlation_id=correlation_id or str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            tool_name=tool_name,
            parent_execution_id=parent_execution_id,
            metadata=metadata or {}
        )
