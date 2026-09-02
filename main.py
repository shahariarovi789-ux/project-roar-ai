#!/usr/bin/env python3
# main.py
"""
PromptTutor AI — Main Application Launcher
Runs the FastAPI server and serves the Odysseus-style desktop interface.
"""

import sys
import os
from pathlib import Path

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import uvicorn
from api.main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", os.getenv("APP_PORT", 8000)))
    is_prod = os.getenv("ENV", "development").lower() == "production"
    print("\n" + "=" * 60)
    print("🎓 PromptTutor AI — Adaptive Intelligent Tutoring System")
    print(f"🚀 Server running on port: {port} (ENV: {'production' if is_prod else 'development'})")
    print("=" * 60 + "\n")
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=not is_prod)
