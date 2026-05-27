# Next 2-3 Weeks: Hardening Only

**Goal:** Make the LangGraph integration production-ready.

---

## Week 1: Tests + Typing

### Tests
- [ ] Unit tests for `async_boundary`
- [ ] Unit tests for `ComposablePolicy`
- [ ] Unit tests for `SQLiteBackend`
- [ ] Integration test: LangGraph + boundary
- [ ] Integration test: Policy composition
- [ ] Integration test: Refusal propagation

### Typing
- [ ] Full type hints in all modules
- [ ] mypy compliance
- [ ] Protocol definitions for backends
- [ ] Typed policy interfaces

### CI
- [ ] GitHub Actions workflow
- [ ] Run tests on push
- [ ] Type checking
- [ ] Coverage reporting

---

## Week 2: API Cleanup + Documentation

### API Cleanup
- [ ] Consistent naming conventions
- [ ] Clear error messages
- [ ] Better docstrings
- [ ] Examples in docstrings

### Async Reliability
- [ ] Timeout handling
- [ ] Cancellation support
- [ ] Error context preservation
- [ ] Trace correlation IDs

### Documentation
- [ ] API reference
- [ ] LangGraph integration guide
- [ ] Policy composition examples
- [ ] Audit backend guide

---

## Week 3: Polish + Publishing

### Refusal Propagation
- [ ] Consistent error types
- [ ] Structured error context
- [ ] Graph interruption semantics
- [ ] Error recovery patterns

### Publishing
- [ ] Short blog post: "Why prompts failed for write authorization"
- [ ] Short blog post: "Tool-call audit semantics"
- [ ] Demo GIF (if not done)
- [ ] README polish

---

## Success Criteria

**By end of week 3:**
- All tests passing
- mypy clean
- LangGraph integration is production-ready
- Documentation is clear
- One blog post published

**NOT:**
- Five new features
- Three new integrations
- Category expansion
- Framework ambitions
