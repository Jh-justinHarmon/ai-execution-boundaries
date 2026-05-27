#!/bin/bash
# Terminal demo script

echo "=== AI Execution Boundaries Demo ==="
echo ""
echo "1. ALLOWED execution (status='pending'):"
python examples/allowed.py
echo ""
echo "---"
echo ""
echo "2. BLOCKED execution (status='approved'):"
python examples/blocked.py
echo ""
echo "---"
echo ""
echo "3. Full audit trail:"
python examples/audit.py
