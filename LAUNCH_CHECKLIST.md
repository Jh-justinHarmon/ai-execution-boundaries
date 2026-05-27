# Launch Checklist — Internal Reference

**DO NOT include this file in the public repo.**

---

## Pre-Launch (Before Pushing to GitHub)

### Critical Path

- [ ] **Create the comparison diagram** (before/after)
  - Use Excalidraw or draw.io
  - Export as PNG
  - Place in `diagrams/execution-boundary-comparison.png`
  - This is THE most important visual

- [ ] **Test the examples locally**
  ```bash
  cd ~/Desktop/ai-execution-boundaries
  make run
  ```
  - Verify all 3 examples execute
  - Check audit log is created
  - Confirm error messages are clear

- [ ] **Remove POSITIONING.md and LAUNCH_CHECKLIST.md**
  - These are internal strategy docs
  - Do NOT push to public repo

- [ ] **Add to .gitignore**
  ```
  POSITIONING.md
  LAUNCH_CHECKLIST.md
  ```

### Optional (Can Add Later)

- [ ] Add tests (pytest suite)
- [ ] Add CI/CD (GitHub Actions)
- [ ] Add more examples (LangChain integration)
- [ ] Add system architecture diagram

---

## Launch Day

### 1. Initialize Git

```bash
cd ~/Desktop/ai-execution-boundaries
git init
git add .
git commit -m "Initial commit: Execution boundaries for AI agents"
```

### 2. Create GitHub Repo

- Go to github.com/new
- **Name:** `ai-execution-boundaries`
- **Description:** "Governance layer for AI agents - validate, authorize, and audit actions before execution"
- **Public**
- **Do NOT** initialize with README (you have one)

### 3. Push to GitHub

```bash
git remote add origin git@github.com:Jh-justinHarmon/ai-execution-boundaries.git
git branch -M main
git push -u origin main
```

### 4. Pin to Profile

- Go to your GitHub profile
- Pin `ai-execution-boundaries` repo
- Unpin tutorial repos

### 5. Update GitHub Profile README

Add to your profile README:

```markdown
## Featured Work

**[ai-execution-boundaries](https://github.com/Jh-justinHarmon/ai-execution-boundaries)**  
Governance layer for AI agents. Prompts can suggest behavior. Execution boundaries enforce behavior.
```

---

## Week 1 Actions

### Day 1-2: Social Proof

**LinkedIn Post:**

```
Prompts are not governance.

AI agents get write access with only prompts as constraints.

Agent interprets "pending_review" as close enough to "pending" 
→ updates anyway 
→ no error 
→ failure discovered downstream.

Prompts guide. They don't enforce.

Execution boundaries enforce.

I built a library that validates, authorizes, and audits AI agent 
actions before they execute.

[Link to repo]

#AI #AgentSystems #Governance
```

**Twitter/X Thread:**

```
1/ Prompts are not governance.

Here's the problem with giving AI agents write access to production systems:

2/ Current approach:
prompt = "Only update status='pending' records"

Agent interprets "pending_review" as close enough
→ updates anyway
→ no validation
→ silent failure

3/ Prompts guide probabilistic systems.
They don't enforce constraints.

This is a category error.

4/ Solution: Execution boundaries

@boundary(policy=exact_match("status", "pending"))
def update_record(data):
    return db.update(data)

Now: "pending" ✓ executes
"pending_review" ✗ blocked at boundary

5/ Built a library for this:
[Link to repo]

Validates before execution.
Audits all attempts.
Deterministic enforcement.

Not another agent framework.
A missing infrastructure primitive.
```

### Day 3-4: Community Engagement

**Hacker News:**

- Submit as "Show HN: Execution Boundaries for AI Agents"
- Best time: Tuesday-Thursday, 8-10am PT
- Be ready to respond to comments with technical depth

**Reddit:**

- r/MachineLearning (if allowed)
- r/LangChain
- r/LocalLLaMA

### Day 5-7: Upstream Contribution

**Target repos:**
- LangGraph (add example of execution boundaries)
- Langfuse (integration example)
- promptfoo (governance example)

**Contribution:**
- Open issue: "Example: Using execution boundaries with [framework]"
- Submit PR with example code
- Link back to your repo in the example

---

## Week 2-4 Actions

### Content Strategy

**Blog post:** "Prompts Are Not Governance"
- Expand the docs/prompts-are-not-governance.md
- Publish to personal blog or Medium
- Submit to Hacker News
- Cross-post to dev.to

**Podcast pitch:** MLOps Community
- Subject: "Execution boundaries for AI agents"
- Pitch: "I've built governance infrastructure for AI agents and documented where current approaches fail"

### Technical Depth

**Add:**
- Tests (pytest suite)
- CI/CD (GitHub Actions)
- More examples (LangChain, LlamaIndex integration)
- Performance benchmarks

---

## Success Metrics (Week 1)

**NOT:**
- Star count (vanity metric)

**IS:**
- Engineers from target companies engaging (comments, issues)
- "Oh, this person sees the problem differently" reactions
- Quality of discussion (technical depth, not hype)
- Upstream contributions acknowledged

---

## Strategic Discipline

**Resist:**
- Adding orchestration features
- Expanding into agent framework
- Building a platform
- Feature creep

**Maintain:**
- Aggressive narrowness
- One concept, one primitive
- Missing infrastructure primitive positioning
- "This is not a framework" clarity

---

## Phase Transitions

**Phase 1 (Months 1-2):** Establish the phrase
- "Prompts are not governance" becomes recognizable
- Associated with you

**Phase 2 (Months 2-4):** Establish the primitive
- Execution boundaries as a concept
- Small, sharp, composable

**Phase 3 (Months 4-12):** Establish the worldview
- Operational architecture for probabilistic systems
- Then 8825 becomes legible

---

## Remember

This repo is a **precision instrument for category formation**.

The goal is **identity compression**, not star count.

The viral core is the **comparison diagram** (before/after).

The positioning is **missing infrastructure primitive**, not framework.

The long-term play is **operational architecture for probabilistic systems**.
