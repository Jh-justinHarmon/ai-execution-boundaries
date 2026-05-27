"""Policy decision primitives."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass(frozen=True)
class PolicyDecision:
    """
    Result of a policy evaluation.
    
    Attributes:
        allowed: Whether the execution is allowed
        policy_name: Name of the policy that made the decision
        reason: Human-readable reason for the decision
        correlation_id: Correlation ID from the execution context
        evaluated_at: UTC timestamp when policy was evaluated
        metadata: Additional decision metadata
    """
    allowed: bool
    policy_name: str
    reason: str
    correlation_id: str
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_allowed(self) -> bool:
        """Whether execution is allowed."""
        return self.allowed
    
    @property
    def is_denied(self) -> bool:
        """Whether execution is denied."""
        return not self.allowed
    
    @classmethod
    def allow(
        cls,
        policy_name: str,
        correlation_id: str,
        reason: str = "Policy evaluation passed",
        metadata: Optional[dict[str, Any]] = None
    ) -> "PolicyDecision":
        """Create an ALLOW decision."""
        return cls(
            allowed=True,
            policy_name=policy_name,
            reason=reason,
            correlation_id=correlation_id,
            metadata=metadata or {}
        )
    
    @classmethod
    def deny(
        cls,
        policy_name: str,
        correlation_id: str,
        reason: str,
        metadata: Optional[dict[str, Any]] = None
    ) -> "PolicyDecision":
        """Create a DENY decision."""
        return cls(
            allowed=False,
            policy_name=policy_name,
            reason=reason,
            correlation_id=correlation_id,
            metadata=metadata or {}
        )
