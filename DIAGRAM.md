# Execution Boundary Architecture

## Prompt-Only Execution (Behavioral Suggestion)

```
       ┌─────────────┐
       │   Prompt    │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │  LLM Agent  │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │  Database   │
       │    Write    │
       └──────┬──────┘
              │
              ▼
         Silent Failure

    ✗ No validation
    ✗ No enforcement
    ✗ No audit trail
    ✗ Wrong records updated
```

**Behavioral suggestion**

---

## Governed Execution (Deterministic Enforcement)

```
       ┌─────────────┐
       │   Prompt    │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │  LLM Agent  │
       └──────┬──────┘
              │
              ▼
    ╔═══════════════════════╗
    ║                       ║
    ║  EXECUTION BOUNDARY   ║
    ║                       ║
    ║  • Policy Validation  ║
    ║  • Authorization      ║
    ║  • Audit Logging      ║
    ║  • Refusal Logic      ║
    ║                       ║
    ╚═══════╦═══════════════╝
            │
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
 ALLOWED          BLOCKED
    │                │
    ▼                │
┌──────────┐         │
│ Database │         │
│  Write   │         │
└────┬─────┘         │
     │               │
     ▼               ▼
✓ Validated    Execution blocked
✓ Audited      Audit logged
✓ Replayable   Error raised
```

**Deterministic enforcement**

---

## Key Difference

**Prompt-only:** Agent interprets constraints → Silent failures

**Execution boundary:** Policy enforces constraints → Explicit blocking
