"""Example: Allowed execution."""

from execution_boundary import boundary, Policy

# Policy: only allow status="pending"
policy = Policy.exact_match("status", "pending")


@boundary(policy=policy, audit=True)
def update_record(data):
    """Update a database record."""
    print(f"✓ Updating record: {data}")
    return {"success": True, "data": data}


if __name__ == "__main__":
    # This will be ALLOWED
    result = update_record({"status": "pending", "id": 123})
    print(f"Result: {result}")
