# Scope

**This repo is:**
```
Execution-boundary middleware for agent runtimes
```

**Specifically:**
- Async decorator for tool-call validation
- Composable policy evaluation
- Structured audit logging
- Refusal propagation through agent graphs

---

## What This Is

A minimal, focused primitive for runtime enforcement of agent tool calls.

---

## What This Is NOT

- ❌ Provenance platform
- ❌ Operational AI operating system
- ❌ Agent governance framework
- ❌ Runtime ontology engine
- ❌ Cognitive infrastructure stack
- ❌ Full policy engine (use OPA for that)
- ❌ Agent framework (use LangGraph for that)
- ❌ Observability platform (use OpenTelemetry for that)

---

## Integration Focus

**One excellent integration:**
- LangGraph (clean, obvious, operational, reproducible)

**Not:**
- Five half-baked integrations
- Every agent framework
- Every policy engine
- Every audit backend

---

## Success Criteria

**This repo succeeds when:**
- Engineers understand it in < 5 minutes
- The LangGraph integration "just works"
- The operational pain is immediately recognizable
- The implementation is obviously correct
- The scope is clearly bounded

**NOT when:**
- It becomes a category
- It gets 50k stars
- It raises funding
- It becomes a platform

---

## Scope Discipline

**If a feature request doesn't directly support:**
1. Async tool-call validation
2. Policy composition
3. Structured audit logging
4. LangGraph integration

**Then it's out of scope.**

---

## The Narrowing Is The Strength

Focus creates clarity.
Clarity creates adoption.
Adoption creates credibility.
