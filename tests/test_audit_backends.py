"""Tests for audit backends."""

import pytest
import asyncio
from pathlib import Path

from execution_boundary.core import ExecutionContext, PolicyDecision
from execution_boundary.audit import (
    NullBackend,
    InMemoryBackend,
    SQLiteBackend,
    StdoutBackend
)


@pytest.mark.asyncio
async def test_null_backend_no_op():
    """Test NullBackend is truly no-op."""
    backend = NullBackend()
    ctx = ExecutionContext.create(tool_name="test")
    decision = PolicyDecision.allow(
        policy_name="test_policy",
        correlation_id=ctx.correlation_id
    )
    
    # Should not raise, should not store anything
    await backend.record(ctx, decision)


@pytest.mark.asyncio
async def test_in_memory_backend_stores_records():
    """Test InMemoryBackend stores audit records."""
    backend = InMemoryBackend()
    ctx = ExecutionContext.create(tool_name="test")
    decision = PolicyDecision.allow(
        policy_name="test_policy",
        correlation_id=ctx.correlation_id
    )
    
    await backend.record(ctx, decision)
    
    assert len(backend.records) == 1
    assert backend.records[0].context.tool_name == "test"
    assert backend.records[0].decision.is_allowed


@pytest.mark.asyncio
async def test_in_memory_backend_find_by_correlation_id():
    """Test InMemoryBackend correlation ID lookup."""
    backend = InMemoryBackend()
    
    ctx1 = ExecutionContext.create(tool_name="tool1", correlation_id="corr-1")
    ctx2 = ExecutionContext.create(tool_name="tool2", correlation_id="corr-2")
    
    decision1 = PolicyDecision.allow("policy1", "corr-1")
    decision2 = PolicyDecision.allow("policy2", "corr-2")
    
    await backend.record(ctx1, decision1)
    await backend.record(ctx2, decision2)
    
    found = backend.find_by_correlation_id("corr-1")
    assert len(found) == 1
    assert found[0].context.tool_name == "tool1"


@pytest.mark.asyncio
async def test_in_memory_backend_find_allowed_denied():
    """Test InMemoryBackend filtering by decision."""
    backend = InMemoryBackend()
    
    ctx1 = ExecutionContext.create(tool_name="tool1")
    ctx2 = ExecutionContext.create(tool_name="tool2")
    
    decision_allow = PolicyDecision.allow("policy", ctx1.correlation_id)
    decision_deny = PolicyDecision.deny("policy", ctx2.correlation_id, "test")
    
    await backend.record(ctx1, decision_allow)
    await backend.record(ctx2, decision_deny)
    
    allowed = backend.find_allowed()
    denied = backend.find_denied()
    
    assert len(allowed) == 1
    assert len(denied) == 1
    assert allowed[0].decision.is_allowed
    assert denied[0].decision.is_denied


@pytest.mark.asyncio
async def test_in_memory_backend_concurrent_writes():
    """Test InMemoryBackend thread safety."""
    backend = InMemoryBackend()
    
    async def write_record(i: int):
        ctx = ExecutionContext.create(tool_name=f"tool_{i}")
        decision = PolicyDecision.allow(f"policy_{i}", ctx.correlation_id)
        await backend.record(ctx, decision)
    
    # Write 100 records concurrently
    await asyncio.gather(*[write_record(i) for i in range(100)])
    
    assert len(backend.records) == 100
    # All correlation IDs should be unique
    correlation_ids = {r.context.correlation_id for r in backend.records}
    assert len(correlation_ids) == 100


@pytest.mark.asyncio
async def test_sqlite_backend_persistence(tmp_path):
    """Test SQLiteBackend persists records."""
    db_path = tmp_path / "test.db"
    backend = SQLiteBackend(str(db_path))
    
    ctx = ExecutionContext.create(tool_name="test_tool")
    decision = PolicyDecision.allow("test_policy", ctx.correlation_id)
    
    await backend.record(ctx, decision)
    
    # Verify record was written
    cursor = backend.conn.execute(
        "SELECT tool_name, decision FROM audit_events"
    )
    row = cursor.fetchone()
    
    assert row[0] == "test_tool"
    assert row[1] == "ALLOWED"
    
    backend.close()


@pytest.mark.asyncio
async def test_sqlite_backend_indexes(tmp_path):
    """Test SQLiteBackend creates indexes."""
    db_path = tmp_path / "test.db"
    backend = SQLiteBackend(str(db_path))
    
    # Check indexes exist
    cursor = backend.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    )
    indexes = {row[0] for row in cursor.fetchall()}
    
    assert "idx_correlation_id" in indexes
    assert "idx_decision" in indexes
    
    backend.close()


@pytest.mark.asyncio
async def test_in_memory_backend_clear():
    """Test InMemoryBackend clear() method."""
    backend = InMemoryBackend()
    
    ctx = ExecutionContext.create(tool_name="test")
    decision = PolicyDecision.allow("policy", ctx.correlation_id)
    
    await backend.record(ctx, decision)
    assert len(backend.records) == 1
    
    backend.clear()
    assert len(backend.records) == 0
