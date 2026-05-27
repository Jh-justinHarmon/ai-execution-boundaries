"""SQLite audit backend."""

import json
import sqlite3
from typing import Optional

from ..core import ExecutionContext, PolicyDecision


class SQLiteBackend:
    """
    SQLite audit backend for persistent storage.
    
    Args:
        db_path: Path to SQLite database file
    """
    
    def __init__(self, db_path: str = "audit.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correlation_id TEXT NOT NULL,
                execution_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                policy_name TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                evaluated_at TEXT NOT NULL,
                parent_execution_id TEXT,
                metadata TEXT
            )
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_correlation_id 
            ON audit_events(correlation_id)
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_decision 
            ON audit_events(decision)
        """)
        self.conn.commit()
    
    async def record(self, context: ExecutionContext, decision: PolicyDecision) -> None:
        """Record audit event to SQLite."""
        self.conn.execute("""
            INSERT INTO audit_events 
            (correlation_id, execution_id, tool_name, policy_name, decision, 
             reason, timestamp, evaluated_at, parent_execution_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            context.correlation_id,
            context.execution_id,
            context.tool_name,
            decision.policy_name,
            "ALLOWED" if decision.is_allowed else "DENIED",
            decision.reason,
            context.timestamp.isoformat(),
            decision.evaluated_at.isoformat(),
            context.parent_execution_id,
            json.dumps({**context.metadata, **decision.metadata})
        ))
        self.conn.commit()
    
    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
