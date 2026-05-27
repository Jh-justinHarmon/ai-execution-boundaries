"""Async execution boundary decorator."""

import asyncio
import functools
from typing import Callable, Any, Optional

from .core import ExecutionContext, PolicyDecision, BoundaryViolation
from .audit import NullBackend


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
    audit_backend: Optional[Any] = None,
    correlation_id: Optional[str] = None,
    parent_execution_id: Optional[str] = None
):
    """
    Async execution boundary decorator.
    
    Args:
        policy: ComposablePolicy with validate() method
        audit_backend: Backend for audit logging (default: NullBackend)
        correlation_id: Optional correlation ID for tracing
        parent_execution_id: Optional parent execution ID for nested calls
    
    Returns:
        Decorated async function that validates before executing
        
    Raises:
        BoundaryViolation: When policy validation fails
    """
    if audit_backend is None:
        audit_backend = NullBackend()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Create execution context
            context = ExecutionContext.create(
                tool_name=func.__name__,
                correlation_id=correlation_id,
                parent_execution_id=parent_execution_id,
                metadata={"args": str(args), "kwargs": str(kwargs)}
            )
            
            # Validate against policy
            is_valid = await policy.validate(*args, **kwargs)
            
            # Create policy decision
            if is_valid:
                decision = PolicyDecision.allow(
                    policy_name=policy.name,
                    correlation_id=context.correlation_id,
                    reason="Policy evaluation passed"
                )
            else:
                decision = PolicyDecision.deny(
                    policy_name=policy.name,
                    correlation_id=context.correlation_id,
                    reason="Policy validation failed"
                )
            
            # Record audit event
            await audit_backend.record(context, decision)
            
            # Block if invalid
            if not is_valid:
                raise BoundaryViolation(context=context, decision=decision)
            
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
