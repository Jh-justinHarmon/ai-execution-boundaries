"""Tests for core primitives."""

import pytest
from datetime import datetime, timezone

from execution_boundary.core import ExecutionContext, PolicyDecision, BoundaryViolation


def test_execution_context_creation():
    """Test ExecutionContext creation with defaults."""
    ctx = ExecutionContext.create(tool_name="test_tool")
    
    assert ctx.tool_name == "test_tool"
    assert ctx.correlation_id is not None
    assert ctx.execution_id is not None
    assert isinstance(ctx.timestamp, datetime)
    assert ctx.timestamp.tzinfo == timezone.utc
    assert ctx.parent_execution_id is None
    assert ctx.metadata == {}


def test_execution_context_with_parent():
    """Test ExecutionContext with parent execution ID."""
    parent_id = "parent-123"
    ctx = ExecutionContext.create(
        tool_name="child_tool",
        parent_execution_id=parent_id
    )
    
    assert ctx.parent_execution_id == parent_id


def test_execution_context_with_metadata():
    """Test ExecutionContext with custom metadata."""
    metadata = {"user_id": "user-123", "request_id": "req-456"}
    ctx = ExecutionContext.create(
        tool_name="test_tool",
        metadata=metadata
    )
    
    assert ctx.metadata == metadata


def test_policy_decision_allow():
    """Test PolicyDecision.allow() factory."""
    decision = PolicyDecision.allow(
        policy_name="test_policy",
        correlation_id="corr-123"
    )
    
    assert decision.is_allowed is True
    assert decision.is_denied is False
    assert decision.policy_name == "test_policy"
    assert decision.correlation_id == "corr-123"
    assert isinstance(decision.evaluated_at, datetime)
    assert decision.evaluated_at.tzinfo == timezone.utc


def test_policy_decision_deny():
    """Test PolicyDecision.deny() factory."""
    decision = PolicyDecision.deny(
        policy_name="test_policy",
        correlation_id="corr-123",
        reason="Invalid status"
    )
    
    assert decision.is_allowed is False
    assert decision.is_denied is True
    assert decision.reason == "Invalid status"


def test_boundary_violation_properties():
    """Test BoundaryViolation property accessors."""
    ctx = ExecutionContext.create(tool_name="test_tool")
    decision = PolicyDecision.deny(
        policy_name="test_policy",
        correlation_id=ctx.correlation_id,
        reason="Test denial"
    )
    
    violation = BoundaryViolation(context=ctx, decision=decision)
    
    assert violation.correlation_id == ctx.correlation_id
    assert violation.tool_name == "test_tool"
    assert violation.policy_name == "test_policy"
    assert violation.reason == "Test denial"


def test_boundary_violation_string_representation():
    """Test BoundaryViolation string formatting."""
    ctx = ExecutionContext.create(tool_name="update_record")
    decision = PolicyDecision.deny(
        policy_name="status_check",
        correlation_id=ctx.correlation_id,
        reason="Status must be pending"
    )
    
    violation = BoundaryViolation(context=ctx, decision=decision)
    error_str = str(violation)
    
    assert "BoundaryViolation" in error_str
    assert ctx.correlation_id in error_str
    assert "status_check" in error_str
    assert "update_record" in error_str
    assert "Status must be pending" in error_str
