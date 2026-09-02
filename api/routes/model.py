# api/routes/model.py
"""
Model Configuration & Real Provider Validation Endpoints.
Dedicated live authentication for:
1. Ollama Cloud Web API & Local Daemon (with live model fetching)
2. OpenRouter Cloud API (with live auth verification)
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from db.models import ModelSwitchRequest
from api.middleware import get_current_user_id
from agents.hardware_scout import HardwareScout
from backend.model_manager import model_manager
from db.storage import log_analytics_event

router = APIRouter(prefix="/model", tags=["Model & Hardware"])


class ValidateOllamaRequest(BaseModel):
    host: str = "https://api.ollama.com"
    api_key: Optional[str] = None


class ValidateOpenRouterRequest(BaseModel):
    api_key: str


@router.get("/hardware-scan")
async def scan_hardware():
    """Scans host device specifications and returns LLM model recommendation."""
    profile = HardwareScout.scan_device()
    return profile.to_dict()


@router.get("/info")
async def get_model_info():
    """Returns current active model, endpoint host, and provider state."""
    return model_manager.get_provider_info()


@router.post("/validate-ollama")
async def validate_ollama_key(req: ValidateOllamaRequest):
    """Verifies Ollama API key against Ollama Cloud / Local daemon and retrieves models."""
    return await model_manager.validate_and_fetch_ollama_models(
        host=req.host,
        api_key=req.api_key
    )


@router.post("/validate-openrouter")
async def validate_openrouter(req: ValidateOpenRouterRequest):
    """Verifies OpenRouter API key against OpenRouter auth endpoint."""
    return await model_manager.validate_openrouter_key(api_key=req.api_key)


@router.post("/test-connection")
async def test_model_connection(req: ModelSwitchRequest):
    """Executes a real test API call to verify authentication and latency before saving."""
    return await model_manager.test_connection(
        backend=req.backend,
        model_name=req.model,
        api_key=req.api_key,
        ollama_host=req.ollama_host,
        base_url=req.base_url
    )


@router.post("/switch")
async def switch_model(req: ModelSwitchRequest, user_id: str = Depends(get_current_user_id)):
    """Switches active model and provider across the tutoring system."""
    model_manager.switch_model(
        backend=req.backend,
        model_name=req.model,
        api_key=req.api_key,
        ollama_host=req.ollama_host,
        base_url=req.base_url
    )
    await log_analytics_event(user_id, "model_switched", {
        "backend": req.backend,
        "model": req.model,
        "host": req.ollama_host
    })
    return {
        "success": True,
        "active_backend": model_manager.backend,
        "active_model": model_manager.current_model,
        "active_host": model_manager.ollama_host
    }
