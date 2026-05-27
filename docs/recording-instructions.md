# Demo GIF Recording Instructions

## Goal

Create 20-second terminal demo showing:
1. Request → validation → allowed
2. Request → validation → blocked
3. Audit log output

**No narration. No music. No presentation energy.**

Just: terminal, deterministic behavior, obvious enforcement.

---

## Recording Tools

**Option 1: asciinema (Recommended)**
```bash
# Install
brew install asciinema

# Record
asciinema rec demo.cast

# Run demo
./demo-recording.sh

# Stop recording (Ctrl+D)

# Convert to GIF
npm install -g asciicast2gif
asciicast2gif demo.cast demo.gif
```

**Option 2: terminalizer**
```bash
# Install
npm install -g terminalizer

# Record
terminalizer record demo

# Run demo
./demo-recording.sh

# Stop recording (Ctrl+D)

# Render
terminalizer render demo -o demo.gif
```

**Option 3: Kap (macOS)**
- Download: https://getkap.co
- Record terminal window
- Export as GIF
- Optimize with: https://ezgif.com/optimize

**Option 4: Screen Studio (macOS, paid)**
- Record terminal
- Export as GIF
- Built-in optimization

---

## Recording Settings

**Terminal:**
- Font: Monaco or Menlo, 14pt
- Theme: Light background (better for README)
- Size: 80x24 or 100x30
- No transparency

**Timing:**
- Total length: 20-30 seconds
- Pause between examples: 1-2 seconds
- Let output be readable

**Output:**
- Format: GIF
- FPS: 10-15 (not 30, keeps file size small)
- Optimize: Yes (use gifsicle or ezgif.com)
- Max file size: 5MB (GitHub limit: 10MB)

---

## What to Show

**Sequence:**
1. Run `python examples/allowed.py`
   - Show: ALLOWED in audit log
   - Show: Successful execution

2. Run `python examples/blocked.py`
   - Show: BLOCKED in audit log
   - Show: BoundaryViolation raised

3. Run `python examples/audit.py`
   - Show: Multiple attempts
   - Show: Audit trail with ALLOWED/BLOCKED decisions

**Total: ~20 seconds**

---

## What NOT to Show

❌ Narration or explanation
❌ Music or sound effects
❌ Animated transitions
❌ Presentation slides
❌ Code walkthrough
❌ Installation steps

**Just runtime behavior.**

---

## Post-Processing

**Optimize GIF:**
```bash
# Using gifsicle
gifsicle -O3 --colors 256 demo.gif -o demo-optimized.gif

# Or use: https://ezgif.com/optimize
```

**Verify:**
- File size < 5MB
- Readable text
- Smooth playback
- Clear ALLOWED/BLOCKED signals

---

## Add to README

Once recorded:

```markdown
## Demo

![Execution Boundary Demo](docs/demo.gif)

**Shows:**
- Allowed execution (status="pending")
- Blocked execution (status="approved")
- Audit trail for all attempts
```

---

## File Locations

- Recording script: `demo-recording.sh`
- Output GIF: `docs/demo.gif`
- Optimized GIF: `docs/demo.gif` (replace original)

---

## Success Criteria

**Good demo:**
- 20-30 seconds
- Shows allowed + blocked + audit
- Terminal output is readable
- File size < 5MB
- No narration needed

**Bad demo:**
- Too long (>45 seconds)
- Too fast (unreadable)
- Presentation energy
- Narration or music
- File size > 10MB
