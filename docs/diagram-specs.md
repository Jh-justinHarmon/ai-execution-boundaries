# Infrastructure Diagram Specifications

## Topology

**Three swim lanes:**
1. LLM Agent Runtime (top)
2. Execution Boundary (middle, visually dominant)
3. Data Plane (bottom)

**Core flow:**
```
tool_call 
→ policy_eval() 
→ ALLOW or DENY 
→ db.execute() or BoundaryViolationError 
→ audit_log.append()
```

---

## Visual Hierarchy

**Primary focus:** Execution Boundary container
- Thickest border (3px)
- Distinct background color
- Largest vertical space
- Central position

**Secondary elements:** Runtime and Data Plane
- Thinner borders (1px)
- Neutral background
- Supporting context

---

## Typography

**Font family:** 
- Primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Fallback: system-ui, sans-serif

**Font sizes:**
- Container titles: 16px, weight 600
- Node labels: 14px, weight 400
- Edge labels: 12px, weight 400

**Text color:**
- Primary: #333333
- Secondary: #666666
- Success: #2e7d32
- Error: #c62828

---

## Color Palette

**Execution Boundary:**
- Background: #e8f5e9 (light green)
- Border: #2e7d32 (dark green)
- Emphasis: This is the enforcement layer

**Runtime/Data Plane:**
- Background: #f5f5f5 (light gray)
- Border: #666666 (medium gray)
- De-emphasized: Supporting context

**Nodes:**
- Background: #ffffff (white)
- Border: #333333 (dark gray)

**Arrows:**
- Default: #666666 (medium gray)
- ALLOW path: #2e7d32 (green)
- DENY path: #c62828 (red)

---

## Spacing & Layout

**Container padding:** 20px
**Node spacing:** 40px vertical, 20px horizontal
**Arrow labels:** 5px offset from path
**Border radius:** 4px (subtle rounding)

---

## Edge Labels

- "invoke" (Runtime → Boundary)
- "ALLOW" (Decision → Audit)
- "DENY" (Decision → Violation)
- No labels on internal boundary flows

---

## Export Settings

**SVG:**
- Width: 800px
- Height: 600px
- ViewBox: 0 0 800 600
- Background: white

**PNG:**
- Resolution: 2x (1600x1200)
- Format: PNG-24
- Background: white
- Compression: optimized

**Excalidraw:**
- Export as JSON
- Include all elements
- Preserve styling

---

## Visual References

**Similar to:**
- OPA policy evaluation diagrams
- Envoy filter chain diagrams
- Vault authentication flow
- Kubernetes admission controller
- OpenTelemetry span flow

**NOT similar to:**
- Tutorial flowcharts
- Marketing graphics
- Educational diagrams
- Startup pitch decks

---

## README Embed

```markdown
## Architecture

![Execution Boundary Topology](docs/execution-boundary-topology.svg)

**Flow:**
1. Agent invokes tool call
2. Execution boundary evaluates policy
3. Decision: ALLOW or DENY
4. Audit logger records attempt
5. Database executes (if allowed) or raises BoundaryViolation (if denied)
```

---

## Figma Layout Specification

**Artboard:** 800x600px

**Layers:**
1. Background (white)
2. Data Plane container
3. Execution Boundary container (bring to front)
4. Runtime container
5. Nodes (all on top)
6. Arrows (below nodes, above containers)
7. Labels (top layer)

**Components:**
- Container: Auto-layout, padding 20px
- Node: Rectangle, corner radius 4px
- Arrow: Line with triangle end
- Label: Text, auto-size

---

## Key Principle

> The execution boundary must visually dominate the composition.

This communicates:
**"All actions must traverse the enforcement layer before execution."**
