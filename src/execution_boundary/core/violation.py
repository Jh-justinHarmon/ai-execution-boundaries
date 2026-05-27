"""Boundary violation exception."""

from dataclasses import dataclass

from .context import ExecutionContext
from .decision import PolicyDecision


@dataclass(frozen=True)
class BoundaryViolation(Exception):
    """
    Raised when execution boundary blocks an action.
    
    Attributes:
        context: Execution context for the blocked action
        decision: Policy decision that blocked execution
    """
    context: ExecutionContext
    decision: PolicyDecision
    
    def __str__(self) -> str:
        return (
            f"BoundaryViolation [{self.context.correlation_id}]: "
            f"policy '{self.decision.policy_name}' denied "
            f"'{self.context.tool_name}' — {self.decision.reason}"
        )
    
    @property
    def correlation_id(self) -> str:
        """Correlation ID for this violation."""
        return self.context.correlation_id
    
    @property
    def tool_name(self) -> str:
        """Name of the tool that was blocked."""
        return self.context.tool_name
    
    @property
    def policy_name(self) -> str:
        """Name of the policy that blocked execution."""
        return self.decision.policy_name
    
    @property
    def reason(self) -> str:
        """Reason for blocking."""
        return self.decision.reason
