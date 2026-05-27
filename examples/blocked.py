"""Example: Blocked execution."""

from execution_boundary import boundary, Policy, BoundaryViolation

# Policy: only allow status="pending"
policy = Policy.exact_match("status", "pending")


@boundary(policy=policy, audit=True)
def update_record(data):
    """Update a database record."""
    print(f"✓ Updating record: {data}")
    return {"success": True, "data": data}


if __name__ == "__main__":
    # This will be BLOCKED
    try:
        result = update_record({"status": "approved", "id": 123})
        print(f"Result: {result}")
    except BoundaryViolation as e:
        print(f"✗ Execution blocked: {e}")
