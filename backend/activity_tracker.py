# backend/activity_tracker.py
"""
Agent Activity Tracker.
Records real-time agent execution events, thoughts, tool calls, and LLM telemetry.
"""

from typing import List, Dict, Any
from datetime import datetime
import time


class ActivityTracker:
    def __init__(self, max_history: int = 50):
        self.events: List[Dict[str, Any]] = []
        self.max_history = max_history

    def log(self, agent_name: str, action: str, details: str = "", status: str = "running"):
        event = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "action": action,
            "details": details,
            "status": status,  # "running", "success", "error", "info"
            "time_ms": round(time.time() * 1000)
        }
        self.events.append(event)
        if len(self.events) > self.max_history:
            self.events.pop(0)
        print(f"[{event['timestamp']}][{agent_name}] {action} - {details} ({status})")

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.events[-limit:]

    def clear(self):
        self.events.clear()


activity_tracker = ActivityTracker()
