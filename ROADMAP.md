# Technical Roadmap

## Current State (v0.1.0)

**What exists:**
- Basic decorator pattern
- Single policy type (exact_match)
- Stdout audit logging
- Sync-only execution

**What this proves:**
- The interface is correct
- The concept is viable
- The problem is real

**What this does NOT prove:**
- Production readiness
- Async agent support
- Composable policy logic
- Structured audit backends

---

## Next: Production Depth (v0.2.0)

**Goal:** One real integration with LangGraph

### Required Features

1. **Async Support**
   ```python
   @boundary(policy=policy, audit=True)
   async def update_record(data):
       return await db.update(data)
   ```

2. **Pluggable Audit Backend**
   ```python
   class AuditBackend(Protocol):
       def log(self, event: AuditEvent) -> None: ...
   
   # Implementations:
   # - NullBackend (default)
   # - StdoutBackend (current behavior)
   # - SQLiteBackend
   # - StructuredLogBackend (JSON lines)
   ```

3. **Structured Audit Events**
   ```python
   @dataclass
   class AuditEvent:
       timestamp: datetime
       function: str
       args: dict
       decision: Literal["ALLOWED", "BLOCKED"]
       policy: str
       correlation_id: str
       error: Optional[str]
   ```

4. **Composable Policies**
   ```python
   policy = Policy.all_of([
       Policy.exact_match("status", "pending"),
       Policy.range_check("amount", max=1000),
       Policy.regex_match("email", r".*@company\.com")
   ])
   ```

5. **LangGraph Integration Test**
   - Real agent graph
   - Database write tool
   - Boundary intercepts tool call
   - Policy evaluation
   - Audit trail
   - Error propagation

---

## Future: Agent-Native Semantics (v0.3.0)

1. **Trust Topology**
   - Policy inheritance across nested agent calls
   - Trust levels between agents
   - Delegation semantics

2. **Context-Aware Policies**
   ```python
   policy = Policy.context_aware(
       lambda ctx: ctx.user.role == "admin" or ctx.data["status"] == "pending"
   )
   ```

3. **Policy Versioning**
   - Immutable policy definitions
   - Version tracking
   - Audit trail for policy changes

4. **Replayability**
   - Deterministic policy evaluation
   - Replay audit logs
   - Verify past decisions

---

## Future: Ecosystem Integration (v0.4.0)

1. **OPA Backend**
   ```python
   policy = Policy.opa(
       url="http://opa:8181/v1/data/agent/allow",
       input_mapper=lambda args: {"action": "update", "resource": args[0]}
   )
   ```

2. **Agent Framework Adapters**
   - LangGraph middleware
   - LangChain tool wrapper
   - AutoGPT plugin
   - CrewAI integration

3. **Observability**
   - OpenTelemetry spans
   - Prometheus metrics
   - Grafana dashboards

---

## Non-Goals

**This library will NOT become:**
- An agent framework
- An orchestration system
- A full policy engine (use OPA for that)
- A prompt optimizer
- A model wrapper

**Focus:** Lightweight, inline validation for agent tool calls.

---

## Contributing

Contributions welcome, especially:
- Async support implementation
- Additional policy types
- Audit backend implementations
- LangGraph integration example
- Test coverage

See `CONTRIBUTING.md` for guidelines.
