# LangGraph Integration

**Real async execution boundary with LangGraph agent.**

## What This Proves

1. **Async support** - Decorator works with `async def`
2. **Structured audit events** - SQLite backend, not stdout
3. **Policy composition** - AND/OR/NOT operators
4. **Real refusal propagation** - BoundaryViolation interrupts graph execution
5. **Runtime interception** - Boundary sits between agent and tool call

---

## Run the Demo

```bash
# Install dependencies
pip install -e .
pip install -r requirements.txt

# Run integration example
python examples/langgraph_integration.py
```

**Output:**
```
=== Demo 1: ALLOWED Execution ===
Attempting to update invoice with status='pending'

Result: ✓ Invoice updated: {...}
Error: None

=== Demo 2: BLOCKED Execution ===
Attempting to update invoice with status='approved'

Result: ✗ Action blocked by execution boundary
Error: Policy 'exact_match_status_pending' blocked execution

=== Demo 3: Policy Composition ===
Policy: (status='pending') AND (amount < 1000)

✓ Test 1 (pending + amount<1000): ALLOWED
✗ Test 2 (pending + amount>1000): BLOCKED
```

---

## Check Audit Trail

```bash
sqlite3 langgraph_audit.db 'SELECT * FROM audit_events;'
```

**Structured events:**
```json
{
  "event_type": "boundary_decision",
  "tool": "update_invoice",
  "decision": "DENIED",
  "policy": "exact_match_status_pending",
  "timestamp": "2026-05-27T10:50:00.000Z",
  "trace_id": "a1b2c3d4-...",
  "args": {...},
  "error": "Policy validation failed"
}
```

---

## What This Demonstrates

**To experienced engineers:**
- Async runtime interception ✓
- Composable policy evaluation ✓
- Structured audit events ✓
- Graph interruption ✓
- Refusal propagation ✓
- Believable enforcement topology ✓

**This proves operational depth, not just conceptual framing.**

---

## Architecture

```
LangGraph Agent
    ↓
  agent_node()
    ↓
  update_invoice() ← @async_boundary(policy, audit_backend)
    ↓
  Policy.validate()
    ↓
  ALLOW → db.update() → audit.log(ALLOWED)
  DENY  → BoundaryViolation → audit.log(DENIED) → graph error
```

---

## Next Steps

- Add more policy types (regex, range, custom)
- Add OpenTelemetry spans
- Add policy versioning
- Add context-aware policies
- Add OPA backend integration

See `ROADMAP.md` for full plan.
