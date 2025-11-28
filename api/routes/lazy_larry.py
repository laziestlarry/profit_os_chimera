"""Lazy Larry Personal Assistant routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional
from database.connection import get_db
from modules.lazy_larry.assistant import LazyLarryAssistant, LazyLarryProfile, LazyLarryChatbot
from api.schemas import CompanyResponse

router = APIRouter()

# In-memory storage for profiles (use database in production)
_profiles: Dict[str, LazyLarryProfile] = {}
_assistants: Dict[str, LazyLarryAssistant] = {}
_chatbots: Dict[str, LazyLarryChatbot] = {}


@router.post("/profile/{company_id}")
async def create_profile(company_id: str, profile_data: Dict):
    """Create or update Lazy Larry profile for a company."""
    profile = LazyLarryProfile(user_id=company_id)
    
    # Update layers from profile_data
    for layer, data in profile_data.get("layers", {}).items():
        profile.update_layer(layer, data)
    
    profile.preferences = profile_data.get("preferences", {})
    
    _profiles[company_id] = profile
    _assistants[company_id] = LazyLarryAssistant(profile)
    _chatbots[company_id] = LazyLarryChatbot(_assistants[company_id])
    
    return {
        "status": "success",
        "company_id": company_id,
        "profile_created": True
    }


@router.post("/chat/{company_id}")
async def chat(company_id: str, message: Dict):
    """Chat with Lazy Larry assistant."""
    if company_id not in _chatbots:
        raise HTTPException(status_code=404, detail="Profile not found. Create profile first.")
    
    chatbot = _chatbots[company_id]
    response = chatbot.chat(message.get("message", ""))
    
    return response


@router.get("/profile/{company_id}")
async def get_profile(company_id: str):
    """Get Lazy Larry profile."""
    if company_id not in _profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile = _profiles[company_id]
    return {
        "company_id": company_id,
        "profile": profile.layers,
        "preferences": profile.preferences
    }


@router.post("/assist/{company_id}")
async def request_assistance(company_id: str, request: Dict):
    """Request assistance from Lazy Larry."""
    if company_id not in _assistants:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    assistant = _assistants[company_id]
    query = request.get("query", "")
    context = request.get("context", {})
    
    response = assistant.process_query(query, context)
    
    return response



