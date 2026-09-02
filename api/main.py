# api/main.py
"""
FastAPI Application Entry Point.
Mounts API routers, WebSocket streaming endpoints, and static UI assets.
Uses modern FastAPI lifespan event management.
"""

import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure project root is in sys.path when running `python api/main.py` directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes import (
    auth,
    session,
    onboarding,
    lesson,
    quiz,
    progress,
    model,
    final_exam
)
from db.storage import init_database_sync
from backend.model_manager import model_manager

STATIC_DIR = ROOT_DIR / "ui" / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database_sync()
    print("[Server] Database verified. Prompt Tutor API ready on port 8000.")
    yield
    # Shutdown
    print("[Server] Prompt Tutor API shutdown complete.")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Adaptive Multi-Agent Prompt Engineering Tutor API",
        description="Backend API for research-grade Intelligent Tutoring System.",
        version="2.0.0",
        lifespan=lifespan
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API Routers under /api/v1
    api_prefix = "/api/v1"
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(session.router, prefix=api_prefix)
    app.include_router(onboarding.router, prefix=api_prefix)
    app.include_router(lesson.router, prefix=api_prefix)
    app.include_router(quiz.router, prefix=api_prefix)
    app.include_router(progress.router, prefix=api_prefix)
    app.include_router(model.router, prefix=api_prefix)
    app.include_router(final_exam.router, prefix=api_prefix)

    # WebSocket Streaming Endpoint
    @app.websocket("/ws/{session_id}")
    async def websocket_endpoint(websocket: WebSocket, session_id: str):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                async for chunk in model_manager.stream_async(data):
                    await websocket.send_text(chunk)
                await websocket.send_text("[[STREAM_END]]")
        except WebSocketDisconnect:
            pass

    # Static Assets & SPA Fallback
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/")
        async def serve_spa_root():
            index_path = STATIC_DIR / "index.html"
            if index_path.exists():
                return FileResponse(str(index_path))
            return {"message": "Prompt Tutor API running. Static UI loading..."}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8000))
    print(f"🚀 Starting PromptTutor AI server at: http://localhost:{port}")
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)
