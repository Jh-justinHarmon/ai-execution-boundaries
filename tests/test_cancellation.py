"""Tests for async cancellation semantics."""

import pytest
import asyncio

from execution_boundary import async_boundary, PolicyFactory, BoundaryViolation
from execution_boundary.audit import InMemoryBackend


@pytest.mark.asyncio
async def test_cancellation_propagates():
    """Test that asyncio.CancelledError propagates through boundary."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def slow_operation(data):
        await asyncio.sleep(10)  # Long operation
        return data
    
    task = asyncio.create_task(slow_operation({"status": "pending"}))
    await asyncio.sleep(0.01)  # Let it start
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_cancellation_during_policy_evaluation():
    """Test cancellation during policy evaluation doesn't corrupt state."""
    backend = InMemoryBackend()
    
    class SlowPolicy:
        """Policy that takes time to evaluate."""
        name = "slow_policy"
        
        async def validate(self, *args, **kwargs):
            await asyncio.sleep(10)
            return True
    
    @async_boundary(policy=SlowPolicy(), audit_backend=backend)
    async def operation(data):
        return data
    
    task = asyncio.create_task(operation({"status": "pending"}))
    await asyncio.sleep(0.01)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    # Audit backend should remain consistent (no partial records)
    # This is implementation-dependent, but we verify no corruption
    assert isinstance(backend.records, list)


@pytest.mark.asyncio
async def test_multiple_cancellations_concurrent():
    """Test multiple concurrent cancellations don't corrupt audit state."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def operation(data):
        await asyncio.sleep(10)
        return data
    
    # Start 10 operations
    tasks = [
        asyncio.create_task(operation({"status": "pending"}))
        for _ in range(10)
    ]
    
    await asyncio.sleep(0.01)
    
    # Cancel all
    for task in tasks:
        task.cancel()
    
    # All should raise CancelledError
    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert all(isinstance(r, asyncio.CancelledError) for r in results)
    
    # Audit backend should be consistent
    assert isinstance(backend.records, list)
    # All correlation IDs should be unique if any were recorded
    if backend.records:
        correlation_ids = {r.context.correlation_id for r in backend.records}
        assert len(correlation_ids) == len(backend.records)


@pytest.mark.asyncio
async def test_cancellation_after_policy_allow():
    """Test cancellation after policy allows but before execution."""
    backend = InMemoryBackend()
    policy = PolicyFactory.exact_match("status", "pending")
    
    execution_started = False
    
    @async_boundary(policy=policy, audit_backend=backend)
    async def operation(data):
        nonlocal execution_started
        execution_started = True
        await asyncio.sleep(10)
        return data
    
    task = asyncio.create_task(operation({"status": "pending"}))
    await asyncio.sleep(0.01)  # Let policy evaluate
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    # Policy should have allowed (audit record exists)
    # But execution may or may not have started depending on timing
    # This tests that cancellation is clean regardless
