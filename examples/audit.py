"""Example: Audit trail."""

from execution_boundary import boundary, Policy, BoundaryViolation

policy = Policy.exact_match("status", "pending")


@boundary(policy=policy, audit=True)
def update_record(data):
    """Update a database record."""
    return {"success": True, "data": data}


if __name__ == "__main__":
    print("=== Execution Boundary Audit Log ===\n")
    
    # Attempt 1: ALLOWED
    print("Attempt 1: status='pending'")
    try:
        update_record({"status": "pending", "id": 1})
    except BoundaryViolation:
        pass
    
    print()
    
    # Attempt 2: BLOCKED
    print("Attempt 2: status='approved'")
    try:
        update_record({"status": "approved", "id": 2})
    except BoundaryViolation:
        pass
    
    print()
    
    # Attempt 3: BLOCKED
    print("Attempt 3: status='rejected'")
    try:
        update_record({"status": "rejected", "id": 3})
    except BoundaryViolation:
        pass
    
    print("\n=== All attempts logged ===")
