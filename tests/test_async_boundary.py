"""Tests for async execution boundary."""

import pytest
import asyncio
from execution_boundary import (
    async_boundary,
    BoundaryViolation,
    PolicyFactory,
    InMemoryBackend,
    SQLiteBackend,
    StdoutBackend
)


@pytest.mark.asyncio
async def test_async_boundary_allows_valid_request():
    """Test that valid requests are allowed."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def update_record(data):
        return {"success": True, "data": data}
    
    result = await update_record({"status": "pending", "id": 1})
    assert result["success"] is True
    assert result["data"]["status"] == "pending"
    assert len(backend.records) == 1
    assert backend.records[0].decision.is_allowed


@pytest.mark.asyncio
async def test_async_boundary_blocks_invalid_request():
    """Test that invalid requests are blocked."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def update_record(data):
        return {"success": True, "data": data}
    
    with pytest.raises(BoundaryViolation) as exc_info:
        await update_record({"status": "approved", "id": 1})
    
    assert "BoundaryViolation" in str(exc_info.value)
    assert exc_info.value.decision.is_denied
    assert len(backend.records) == 1
    assert backend.records[0].decision.is_denied


@pytest.mark.asyncio
async def test_policy_composition_and():
    """Test AND policy composition."""
    backend = InMemoryBackend()
    status_policy = PolicyFactory.exact_match("status", "pending")
    amount_policy = PolicyFactory.range_check("amount", max_val=1000)
    combined = status_policy & amount_policy
    
    @async_boundary(policy=combined, audit_backend=backend)
    async def update_record(data):
        return {"success": True}
    
    # Both conditions met - should allow
    result = await update_record({"status": "pending", "amount": 500})
    assert result["success"] is True
    
    # Amount too high - should block
    with pytest.raises(BoundaryViolation):
        await update_record({"status": "pending", "amount": 1500})


@pytest.mark.asyncio
async def test_policy_composition_or():
    """Test OR policy composition."""
    policy1 = PolicyFactory.exact_match("status", "pending")
    policy2 = PolicyFactory.exact_match("status", "draft")
    combined = policy1 | policy2
    
    @async_boundary(policy=combined, audit_backend=StdoutBackend())
    async def update_record(data):
        return {"success": True}
    
    # First condition met
    result = await update_record({"status": "pending"})
    assert result["success"] is True
    
    # Second condition met
    result = await update_record({"status": "draft"})
    assert result["success"] is True
    
    # Neither condition met - should block
    with pytest.raises(BoundaryViolation):
        await update_record({"status": "approved"})


@pytest.mark.asyncio
async def test_policy_composition_not():
    """Test NOT policy composition."""
    policy = PolicyFactory.exact_match("status", "archived")
    inverted = ~policy
    
    @async_boundary(policy=inverted, audit_backend=StdoutBackend())
    async def update_record(data):
        return {"success": True}
    
    # Not archived - should allow
    result = await update_record({"status": "pending"})
    assert result["success"] is True
    
    # Archived - should block
    with pytest.raises(BoundaryViolation):
        await update_record({"status": "archived"})


@pytest.mark.asyncio
async def test_sqlite_audit_backend(tmp_path):
    """Test SQLite audit backend persistence."""
    db_path = tmp_path / "test_audit.db"
    backend = SQLiteBackend(str(db_path))
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def update_record(data):
        return {"success": True}
    
    # Execute allowed request
    await update_record({"status": "pending", "id": 1})
    
    # Execute blocked request
    try:
        await update_record({"status": "approved", "id": 2})
    except BoundaryViolation:
        pass
    
    # Verify audit events were persisted
    cursor = backend.conn.execute("SELECT COUNT(*) FROM audit_events")
    count = cursor.fetchone()[0]
    assert count == 2
    
    # Verify decisions
    cursor = backend.conn.execute("SELECT decision FROM audit_events ORDER BY id")
    decisions = [row[0] for row in cursor.fetchall()]
    assert decisions == ["ALLOWED", "DENIED"]


@pytest.mark.asyncio
async def test_trace_correlation():
    """Test that correlation IDs are preserved."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    correlation_id = "test-corr-123"
    
    @async_boundary(policy=policy, audit_backend=backend, correlation_id=correlation_id)
    async def update_record(data):
        return {"success": True}
    
    try:
        await update_record({"status": "approved"})
    except BoundaryViolation as e:
        assert e.correlation_id == correlation_id
        assert e.context.correlation_id == correlation_id


@pytest.mark.asyncio
async def test_async_function_metadata_preserved():
    """Test that function metadata is preserved by decorator."""
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=StdoutBackend())
    async def update_record(data):
        """Update a record."""
        return {"success": True}
    
    assert update_record.__name__ == "update_record"
    assert "Update a record" in update_record.__doc__


@pytest.mark.asyncio
async def test_range_check_policy():
    """Test range check policy."""
    policy = PolicyFactory.range_check("amount", min_val=10, max_val=100)
    
    @async_boundary(policy=policy, audit_backend=StdoutBackend())
    async def process_payment(data):
        return {"success": True}
    
    # Within range
    result = await process_payment({"amount": 50})
    assert result["success"] is True
    
    # Below minimum
    with pytest.raises(BoundaryViolation):
        await process_payment({"amount": 5})
    
    # Above maximum
    with pytest.raises(BoundaryViolation):
        await process_payment({"amount": 150})


@pytest.mark.asyncio
async def test_regex_match_policy():
    """Test regex match policy."""
    policy = PolicyFactory.regex_match("email", r".*@company\.com$")
    
    @async_boundary(policy=policy, audit_backend=StdoutBackend())
    async def send_email(data):
        return {"success": True}
    
    # Valid email
    result = await send_email({"email": "user@company.com"})
    assert result["success"] is True
    
    # Invalid email
    with pytest.raises(BoundaryViolation):
        await send_email({"email": "user@external.com"})
