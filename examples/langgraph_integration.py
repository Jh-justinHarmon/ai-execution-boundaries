"""LangGraph integration example with async execution boundaries."""

import asyncio
from typing import TypedDict, Annotated, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from execution_boundary import (
    async_boundary,
    PolicyFactory,
    SQLiteBackend,
    BoundaryViolation
)


# Define agent state
class AgentState(TypedDict):
    messages: List[str]
    invoice_status: str
    error: str  # Will be empty string instead of None for Python 3.9 compatibility


# Simulated database
class InvoiceDB:
    def __init__(self):
        self.invoices = {
            1: {"id": 1, "status": "pending", "amount": 500},
            2: {"id": 2, "status": "approved", "amount": 1000},
        }
    
    async def update(self, invoice_id: int, status: str):
        """Update invoice status."""
        await asyncio.sleep(0.1)  # Simulate DB latency
        if invoice_id in self.invoices:
            self.invoices[invoice_id]["status"] = status
            return {"success": True, "invoice": self.invoices[invoice_id]}
        return {"success": False, "error": "Invoice not found"}


# Initialize database and audit backend
db = InvoiceDB()
audit_backend = SQLiteBackend("langgraph_audit.db")


# Define policy: only allow updates to "pending" invoices
policy = PolicyFactory.exact_match("status", "pending")


# Tool with execution boundary
@async_boundary(policy=policy, audit_backend=audit_backend)
async def update_invoice(data: dict) -> dict:
    """Update invoice status - protected by execution boundary."""
    invoice_id = data.get("id")
    new_status = data.get("new_status")
    return await db.update(invoice_id, new_status)


# Agent node that attempts tool call
async def agent_node(state: AgentState) -> AgentState:
    """Agent decides to update an invoice."""
    messages = state["messages"]
    invoice_status = state["invoice_status"]
    
    # Agent attempts to update invoice
    try:
        result = await update_invoice({
            "id": 1,
            "status": invoice_status,  # Current status
            "new_status": "approved"
        })
        
        return {
            **state,
            "messages": messages + [f"✓ Invoice updated: {result}"],
            "error": None
        }
    
    except BoundaryViolation as e:
        # Boundary blocked the action
        return {
            **state,
            "messages": messages + [f"✗ Action blocked by execution boundary"],
            "error": str(e)
        }


# Build graph
def build_graph():
    """Build LangGraph with execution boundary."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    
    # Add edges
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    return workflow.compile()


# Demo execution
async def demo_allowed():
    """Demo: Allowed execution (status='pending')."""
    print("\n=== Demo 1: ALLOWED Execution ===")
    print("Attempting to update invoice with status='pending'\n")
    
    graph = build_graph()
    result = await graph.ainvoke({
        "messages": ["Agent starting..."],
        "invoice_status": "pending",
        "error": None
    })
    
    print(f"Result: {result['messages'][-1]}")
    print(f"Error: {result['error']}")


async def demo_blocked():
    """Demo: Blocked execution (status='approved')."""
    print("\n=== Demo 2: BLOCKED Execution ===")
    print("Attempting to update invoice with status='approved'\n")
    
    graph = build_graph()
    result = await graph.ainvoke({
        "messages": ["Agent starting..."],
        "invoice_status": "approved",
        "error": None
    })
    
    print(f"Result: {result['messages'][-1]}")
    print(f"Error: {result['error']}")


async def demo_policy_composition():
    """Demo: Composable policies with AND/OR."""
    print("\n=== Demo 3: Policy Composition ===")
    print("Policy: (status='pending') AND (amount < 1000)\n")
    
    # Compose policies
    status_policy = PolicyFactory.exact_match("status", "pending")
    amount_policy = PolicyFactory.range_check("amount", max_val=1000)
    combined_policy = status_policy & amount_policy
    
    @async_boundary(policy=combined_policy, audit_backend=audit_backend)
    async def update_with_limit(data: dict) -> dict:
        return await db.update(data["id"], data["new_status"])
    
    # Test 1: Both conditions met
    try:
        result = await update_with_limit({
            "id": 1,
            "status": "pending",
            "amount": 500,
            "new_status": "approved"
        })
        print(f"✓ Test 1 (pending + amount<1000): ALLOWED")
    except BoundaryViolation:
        print(f"✗ Test 1 (pending + amount<1000): BLOCKED")
    
    # Test 2: Amount too high
    try:
        result = await update_with_limit({
            "id": 2,
            "status": "pending",
            "amount": 1500,
            "new_status": "approved"
        })
        print(f"✓ Test 2 (pending + amount>1000): ALLOWED")
    except BoundaryViolation:
        print(f"✗ Test 2 (pending + amount>1000): BLOCKED")


async def main():
    """Run all demos."""
    await demo_allowed()
    await demo_blocked()
    await demo_policy_composition()
    
    print("\n=== Audit Trail ===")
    print("Check 'langgraph_audit.db' for structured audit events")
    print("\nQuery example:")
    print("  sqlite3 langgraph_audit.db 'SELECT * FROM audit_events;'")


if __name__ == "__main__":
    asyncio.run(main())
