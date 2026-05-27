#!/bin/bash
# Demo recording script for execution boundaries
# Shows: allowed → blocked → audit log

clear

echo "=== Execution Boundary Demo ==="
echo ""
sleep 1

echo "$ python examples/allowed.py"
echo ""
sleep 0.5

python examples/allowed.py
echo ""
sleep 2

echo "---"
echo ""
sleep 1

echo "$ python examples/blocked.py"
echo ""
sleep 0.5

python examples/blocked.py
echo ""
sleep 2

echo "---"
echo ""
sleep 1

echo "$ python examples/audit.py"
echo ""
sleep 0.5

python examples/audit.py
echo ""
sleep 1

echo ""
echo "=== Demo Complete ==="
