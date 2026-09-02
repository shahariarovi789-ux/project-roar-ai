#!/usr/bin/env python3
# scripts/create_db.py
"""
Database Initialization Script.
Creates all 8 relational tables defined in db/schema.sql.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from db.storage import init_database_sync

if __name__ == "__main__":
    print("[Init] Initializing SQLite database...")
    init_database_sync()
    print("[Init] Database initialization complete.")
