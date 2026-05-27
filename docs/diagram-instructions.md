# Diagram Export Instructions

## Use Excalidraw (https://excalidraw.com)

### Left Side (Prompt-Only)

1. **Boxes (light gray):**
   - "Prompt"
   - "LLM Agent"
   - "Database Write"
   - "Silent Failure" (red accent)

2. **Arrows:** Simple downward arrows

3. **Labels (red text):**
   - ✗ No validation
   - ✗ No enforcement
   - ✗ No audit trail
   - ✗ Wrong records updated

4. **Bottom label:** "Behavioral suggestion"

---

### Right Side (Governed Execution)

1. **Boxes (light gray):**
   - "Prompt"
   - "LLM Agent"

2. **EXECUTION BOUNDARY (large, green accent, thick border):**
   - Title: "EXECUTION BOUNDARY"
   - Bullet points:
     - • Policy Validation
     - • Authorization
     - • Audit Logging
     - • Refusal Logic

3. **Split arrows:**
   - Left: "ALLOWED" → "Database Write"
   - Right: "BLOCKED"

4. **Labels (green text):**
   - Left path:
     - ✓ Validated
     - ✓ Audited
     - ✓ Replayable
   - Right path:
     - Execution blocked
     - Audit logged
     - Error raised

5. **Bottom label:** "Deterministic enforcement"

---

## Export Settings

- Format: PNG
- Background: White
- Resolution: 2x (high DPI)
- Filename: `execution-boundary-comparison.png`
- Save to: `docs/`

---

## Visual Style

- Clean spacing
- Dark text on white
- Red accents (left side)
- Green accents (right side)
- Large "EXECUTION BOUNDARY" box (visually dominant)
- Minimal words
- No code snippets
