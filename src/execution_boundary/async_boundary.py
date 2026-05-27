"""Async execution boundary decorator."""

import asyncio
import functools
from datetime import datetime
from typing import Callable, Any, Optional
from dataclasses import dataclass, asdict
import uuid


@dataclass
class AuditEvent:
    """Structured audit event."""
    event_type: str
    tool: str
    decision: str
    policy: str
    timestamp: str
    trace_id: str
    args: dict
    error: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


class BoundaryViolation(Exception):
    """Raised when execution boundary blocks an action."""
    def __init__(self, message: str, audit_event: AuditEvent):
        super().__init__(message)
        self.audit_event = audit_event


class AuditBackend:
    """Base audit backend."""
    def log(self, event: AuditEvent) -> None:
        raise NotImplementedError


class SQLiteBackend(AuditBackend):
    """SQLite audit backend."""
    def __init__(self, db_path: str = "audit.db"):
        import sqlite3
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                tool TEXT NOT NULL,
                decision TEXT NOT NULL,
                policy TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                trace_id TEXT NOT NULL,
                args TEXT NOT NULL,
                error TEXT
            )
        """)
        self.conn.commit()
    
    def log(self, event: AuditEvent) -> None:
        import json
        self.conn.execute("""
            INSERT INTO audit_events 
            (event_type, tool, decision, policy, timestamp, trace_id, args, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_type,
            event.tool,
            event.decision,
            event.policy,
            event.timestamp,
            event.trace_id,
            json.dumps(event.args),
            event.error
        ))
        self.conn.commit()


class StdoutBackend(AuditBackend):
    """Stdout audit backend."""
    def log(self, event: AuditEvent) -> None:
        import json
        print(f"[AUDIT] {json.dumps(event.to_dict())}")


class ComposablePolicy:
    """Composable policy with AND/OR/NOT operators."""
    
    def __init__(self, name: str, validator: Callable):
        self.name = name
        self.validator = validator
    
    async def validate(self, *args, **kwargs) -> bool:
        result = self.validator(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result
    
    def __and__(self, other):
        """AND operator."""
        async def combined(*args, **kwargs):
            return await self.validate(*args, **kwargs) and await other.validate(*args, **kwargs)
        return ComposablePolicy(f"{self.name}_AND_{other.name}", combined)
    
    def __or__(self, other):
        """OR operator."""
        async def combined(*args, **kwargs):
            return await self.validate(*args, **kwargs) or await other.validate(*args, **kwargs)
        return ComposablePolicy(f"{self.name}_OR_{other.name}", combined)
    
    def __invert__(self):
        """NOT operator."""
        async def inverted(*args, **kwargs):
            return not await self.validate(*args, **kwargs)
        return ComposablePolicy(f"NOT_{self.name}", inverted)


def async_boundary(
    policy: ComposablePolicy,
    audit_backend: Optional[AuditBackend] = None,
    trace_id: Optional[str] = None
):
    """
    Async execution boundary decorator.
    
    Args:
        policy: ComposablePolicy with validate() method
        audit_backend: Backend for audit logging (default: StdoutBackend)
        trace_id: Optional trace ID for correlation
    
    Returns:
        Decorated async function that validates before executing
        
    Raises:
        BoundaryViolation: When policy validation fails
    """
    if audit_backend is None:
        audit_backend = StdoutBackend()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            current_trace_id = trace_id or str(uuid.uuid4())
            
            # Validate against policy
            is_valid = await policy.validate(*args, **kwargs)
            
            # Create audit event
            event = AuditEvent(
                event_type="boundary_decision",
                tool=func.__name__,
                decision="ALLOWED" if is_valid else "DENIED",
                policy=policy.name,
                timestamp=datetime.utcnow().isoformat(),
                trace_id=current_trace_id,
                args={"args": str(args), "kwargs": str(kwargs)},
                error=None if is_valid else "Policy validation failed"
            )
            
            # Log audit event
            audit_backend.log(event)
            
            # Block if invalid
            if not is_valid:
                raise BoundaryViolation(
                    f"Policy '{policy.name}' blocked execution of {func.__name__}",
                    audit_event=event
                )
            
            # Execute if valid
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Policy factory helpers
class PolicyFactory:
    """Factory for creating common policies."""
    
    @staticmethod
    def exact_match(field: str, value: Any) -> ComposablePolicy:
        """Policy that requires exact field match."""
        def validator(data, *args, **kwargs):
            if isinstance(data, dict):
                return data.get(field) == value
            return False
        return ComposablePolicy(f"exact_match_{field}_{value}", validator)
    
    @staticmethod
    def range_check(field: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> ComposablePolicy:
        """Policy that checks numeric range."""
        def validator(data, *args, **kwargs):
            if not isinstance(data, dict):
                return False
            val = data.get(field)
            if val is None:
                return False
            if min_val is not None and val < min_val:
                return False
            if max_val is not None and val > max_val:
                return False
            return True
        return ComposablePolicy(f"range_{field}_{min_val}_{max_val}", validator)
    
    @staticmethod
    def regex_match(field: str, pattern: str) -> ComposablePolicy:
        """Policy that matches regex pattern."""
        import re
        compiled = re.compile(pattern)
        def validator(data, *args, **kwargs):
            if not isinstance(data, dict):
                return False
            val = data.get(field)
            if val is None:
                return False
            return bool(compiled.match(str(val)))
        return ComposablePolicy(f"regex_{field}", validator)
