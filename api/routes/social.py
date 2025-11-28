"""Social Media Automation routes."""

from fastapi import APIRouter, Depends
from typing import List, Optional, Dict
from modules.social_automation.automator import SocialMediaAutomator, ContentCalendar, Platform

router = APIRouter()


@router.post("/create-content")
async def create_social_content(
    platforms: List[str],
    content_theme: str,
    count: int = 7
):
    """Create batch of social media content."""
    user_profile = {"brand": "Lazy Larry"}
    brand_voice = {
        "tone": "calm, helpful, slightly playful",
        "colors": ["#6366f1", "#8b5cf6"]
    }
    
    automator = SocialMediaAutomator(user_profile, brand_voice)
    
    # Convert string platforms to enum
    platform_enums = [Platform[p.upper()] for p in platforms if p.upper() in Platform.__members__]
    
    posts = automator.create_content_batch(platform_enums, content_theme, count)
    
    return {
        "posts_created": len(posts),
        "posts": [
            {
                "id": post.id,
                "platform": post.platform.value,
                "content_type": post.content_type,
                "scheduled_time": post.scheduled_time.isoformat(),
                "content_preview": str(post.content)[:100]
            }
            for post in posts
        ]
    }


@router.post("/schedule")
async def schedule_posts(posts: List[Dict]):
    """Schedule social media posts."""
    from modules.social_automation.automator import SocialPost, Platform
    
    # Convert dicts to SocialPost objects
    social_posts = []
    for p in posts:
        post = SocialPost(
            id=p.get("id", ""),
            platform=Platform[p.get("platform", "instagram").upper()],
            content_type=p.get("content_type", "text"),
            content=p.get("content", {}),
            scheduled_time=p.get("scheduled_time")
        )
        social_posts.append(post)
    
    user_profile = {}
    brand_voice = {}
    automator = SocialMediaAutomator(user_profile, brand_voice)
    
    result = automator.schedule_posts(social_posts)
    
    return result


@router.post("/analyze-performance")
async def analyze_social_performance(posts: List[Dict]):
    """Analyze social media performance."""
    from modules.social_automation.automator import SocialPost, Platform
    
    social_posts = []
    for p in posts:
        post = SocialPost(
            id=p.get("id", ""),
            platform=Platform[p.get("platform", "instagram").upper()],
            content_type=p.get("content_type", "text"),
            content=p.get("content", {}),
            scheduled_time=p.get("scheduled_time"),
            status=p.get("status", "scheduled"),
            performance_metrics=p.get("performance_metrics")
        )
        social_posts.append(post)
    
    user_profile = {}
    brand_voice = {}
    automator = SocialMediaAutomator(user_profile, brand_voice)
    
    analysis = automator.analyze_performance(social_posts)
    
    return analysis


@router.post("/content-calendar")
async def generate_content_calendar(
    start_date: str,
    weeks: int = 4,
    themes: Optional[List[str]] = None
):
    """Generate content calendar."""
    from datetime import datetime
    
    calendar_gen = ContentCalendar()
    start = datetime.fromisoformat(start_date)
    
    calendar = calendar_gen.generate_calendar(start, weeks, themes)
    
    return {
        "calendar": calendar,
        "weeks": weeks,
        "start_date": start_date
    }

