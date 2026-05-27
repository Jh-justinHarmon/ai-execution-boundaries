"""Execution boundary decorator."""

import json
from datetime import datetime
from typing import Callable, Any


class BoundaryViolation(Exception):
    """Raised when execution boundary blocks an action."""
    pass


def boundary(policy: Any, audit: bool = True) -> Callable:
    """
    Validates actions before execution.
    
    Args:
        policy: Policy object with validate() method
        audit: Whether to log attempts (default: True)
    
    Returns:
        Decorated function that validates before executing
        
    Raises:
        BoundaryViolation: When policy validation fails
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Validate against policy
            is_valid = policy.validate(*args, **kwargs)
            
            # Audit attempt
            if audit:
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "function": func.__name__,
                    "args": str(args),
                    "kwargs": str(kwargs),
                    "decision": "ALLOWED" if is_valid else "BLOCKED",
                    "policy": policy.__class__.__name__
                }
                print(f"[AUDIT] {json.dumps(log_entry)}")
            
            # Block if invalid
            if not is_valid:
                raise BoundaryViolation(
                    f"Policy '{policy.__class__.__name__}' blocked execution of {func.__name__}"
                )
            
            # Execute if valid
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
