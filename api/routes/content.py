"""Content & Design routes."""

from fastapi import APIRouter, Depends
from typing import List, Dict, Optional
from modules.content_design.creator import (
    DashboardBuilder,
    InfographicCreator,
    StoryboardBuilder,
    EmotionalContentEnhancer
)

router = APIRouter()


@router.post("/dashboard")
async def create_dashboard(
    data: Dict,
    metrics: List[str],
    style: str = "modern",
    brand_style: Optional[Dict] = None
):
    """Create a dashboard visualization."""
    if brand_style is None:
        brand_style = {"colors": ["#6366f1", "#8b5cf6"]}
    
    builder = DashboardBuilder(brand_style)
    dashboard = builder.create_dashboard(data, metrics, style)
    
    return {
        "dashboard_id": dashboard.id,
        "title": dashboard.title,
        "design_spec": dashboard.design_spec,
        "emotional_tone": dashboard.emotional_tone
    }


@router.post("/infographic")
async def create_infographic(
    topic: str,
    data_points: List[Dict],
    style: str = "modern",
    brand_style: Optional[Dict] = None
):
    """Create an infographic."""
    if brand_style is None:
        brand_style = {"colors": ["#6366f1", "#8b5cf6", "#ec4899"]}
    
    creator = InfographicCreator(brand_style)
    infographic = creator.create_infographic(topic, data_points, style)
    
    return {
        "infographic_id": infographic.id,
        "title": infographic.title,
        "design_spec": infographic.design_spec,
        "emotional_tone": infographic.emotional_tone
    }


@router.post("/storyboard")
async def create_storyboard(
    story_theme: str,
    scenes: int = 5,
    format: str = "video",
    brand_style: Optional[Dict] = None
):
    """Create a storyboard."""
    if brand_style is None:
        brand_style = {}
    
    builder = StoryboardBuilder(brand_style)
    storyboard = builder.create_storyboard(story_theme, scenes, format)
    
    return {
        "storyboard_id": storyboard.id,
        "title": storyboard.title,
        "design_spec": storyboard.design_spec,
        "emotional_tone": storyboard.emotional_tone
    }


@router.post("/enhance-emotion")
async def enhance_with_emotion(
    content: str,
    target_emotion: str = "supportive"
):
    """Enhance content with emotional touch."""
    enhancer = EmotionalContentEnhancer()
    enhanced = enhancer.enhance_with_emotion(content, target_emotion)
    
    return {
        "original": content,
        "enhanced": enhanced,
        "emotion": target_emotion
    }


@router.post("/add-social-elements")
async def add_social_elements(content: Dict):
    """Add social connection elements to content."""
    enhancer = EmotionalContentEnhancer()
    enhanced = enhancer.add_social_elements(content)
    
    return enhanced



