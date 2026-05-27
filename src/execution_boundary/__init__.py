"""Execution boundaries for AI agents with write access."""

from .boundary import boundary, BoundaryViolation
from .policy import Policy

__version__ = "0.1.0"
__all__ = ["boundary", "BoundaryViolation", "Policy"]
