"""Stdout audit backend."""

import json
import sys

from ..core import ExecutionContext, PolicyDecision


class StdoutBackend:
    """
    Stdout audit backend for development/debugging.
    
    Writes NDJSON audit records to stdout.
    """
    
    async def record(self, context: ExecutionContext, decision: PolicyDecision) -> None:
        """Write audit event to stdout as NDJSON."""
        record = {
            "correlation_id": context.correlation_id,
            "execution_id": context.execution_id,
            "tool_name": context.tool_name,
            "policy_name": decision.policy_name,
            "decision": "ALLOWED" if decision.is_allowed else "DENIED",
            "reason": decision.reason,
            "timestamp": context.timestamp.isoformat(),
            "evaluated_at": decision.evaluated_at.isoformat(),
            "parent_execution_id": context.parent_execution_id,
        }
        print(json.dumps(record), file=sys.stdout, flush=True)
