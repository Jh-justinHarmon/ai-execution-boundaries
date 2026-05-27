# Comparison Diagram Concept

## Without Execution Boundaries

```
┌─────────────────────────────────────┐
│ Prompt: "Only update pending"      │
└─────────────┬───────────────────────┘
              │
              ▼
       ┌──────────────┐
       │  LLM Agent   │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  Database    │
       │  UPDATE      │
       └──────────────┘
              │
              ▼
    ✗ Wrong records updated
    ✗ No validation
    ✗ No audit trail
    ✗ Silent failure
```

## With Execution Boundaries

```
┌─────────────────────────────────────┐
│ Prompt: "Only update pending"      │
└─────────────┬───────────────────────┘
              │
              ▼
       ┌──────────────┐
       │  LLM Agent   │
       └──────┬───────┘
              │
              ▼
    ╔═════════════════════════╗
    ║  EXECUTION BOUNDARY     ║
    ║                         ║
    ║  @boundary(             ║
    ║    policy=exact_match(  ║
    ║      "status",          ║
    ║      "pending"          ║
    ║    )                    ║
    ║  )                      ║
    ╚═════════╦═══════════════╝
              │
              │ Validates:
              │ status == "pending"?
              │
     ┌────────┴────────┐
     │                 │
     ▼                 ▼
✓ ALLOWED        ✗ BLOCKED
status="pending" status="approved"
     │                 │
     ▼                 │
┌──────────┐           │
│ Database │           │
│ UPDATE   │           │
└──────────┘           │
     │                 │
     ▼                 ▼
✓ Correct        ✗ BoundaryViolation
✓ Audited        ✗ Error raised
                 ✓ Audited
```

## Key Difference

**Without boundaries:** Prompt suggests, agent interprets, failures are silent

**With boundaries:** Policy enforces, validation blocks, failures are explicit
