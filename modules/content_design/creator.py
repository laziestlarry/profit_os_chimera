"""Content & Design Creator - Dashboards, infographics, storyboards."""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class ContentType(str, Enum):
    DASHBOARD = "dashboard"
    INFOGRAPHIC = "infographic"
    STORYBOARD = "storyboard"
    PRESENTATION = "presentation"
    REPORT = "report"
    SOCIAL_CARD = "social_card"


@dataclass
class ContentAsset:
    """Content asset structure."""
    id: str
    type: ContentType
    title: str
    data: Dict  # Content-specific data
    design_spec: Dict
    emotional_tone: str  # "professional", "friendly", "energizing", "calm"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class DashboardBuilder:
    """Builds data dashboards with emotional design."""
    
    def __init__(self, brand_style: Dict):
        self.brand_style = brand_style
    
    def create_dashboard(
        self,
        data: Dict,
        metrics: List[str],
        style: str = "modern"
    ) -> ContentAsset:
        """Create a dashboard visualization."""
        dashboard_spec = {
            "layout": "grid",
            "sections": [
                {
                    "type": "kpi_cards",
                    "metrics": metrics,
                    "style": style
                },
                {
                    "type": "charts",
                    "charts": self._generate_charts(data, metrics)
                },
                {
                    "type": "trends",
                    "time_range": "30d"
                }
            ],
            "color_scheme": self.brand_style.get("colors", ["#6366f1", "#8b5cf6"]),
            "emotional_tone": "professional"
        }
        
        return ContentAsset(
            id=f"dashboard_{datetime.utcnow().timestamp()}",
            type=ContentType.DASHBOARD,
            title="Growth Dashboard",
            data=data,
            design_spec=dashboard_spec,
            emotional_tone="professional"
        )
    
    def _generate_charts(self, data: Dict, metrics: List[str]) -> List[Dict]:
        """Generate chart specifications."""
        charts = []
        for metric in metrics:
            charts.append({
                "type": "line",
                "metric": metric,
                "title": f"{metric.replace('_', ' ').title()} Trend",
                "data_points": data.get(metric, [])
            })
        return charts


class InfographicCreator:
    """Creates infographics with emotional appeal."""
    
    def __init__(self, brand_style: Dict):
        self.brand_style = brand_style
    
    def create_infographic(
        self,
        topic: str,
        data_points: List[Dict],
        style: str = "modern"
    ) -> ContentAsset:
        """Create an infographic."""
        infographic_spec = {
            "layout": "vertical_scroll",
            "sections": [
                {
                    "type": "hero",
                    "title": topic,
                    "subtitle": "Key Insights"
                },
                {
                    "type": "stats",
                    "data_points": data_points
                },
                {
                    "type": "visual_elements",
                    "icons": True,
                    "illustrations": True
                }
            ],
            "color_palette": self.brand_style.get("colors", ["#6366f1", "#8b5cf6", "#ec4899"]),
            "emotional_tone": "energizing"
        }
        
        return ContentAsset(
            id=f"infographic_{datetime.utcnow().timestamp()}",
            type=ContentType.INFOGRAPHIC,
            title=f"{topic} Infographic",
            data={"topic": topic, "data_points": data_points},
            design_spec=infographic_spec,
            emotional_tone="energizing"
        )


class StoryboardBuilder:
    """Creates storyboards for videos and presentations."""
    
    def create_storyboard(
        self,
        story_theme: str,
        scenes: int = 5,
        format: str = "video"
    ) -> ContentAsset:
        """Create a storyboard."""
        storyboard_scenes = []
        
        for i in range(scenes):
            storyboard_scenes.append({
                "scene_number": i + 1,
                "visual": f"Scene {i+1} visual description",
                "script": f"Scene {i+1} script/narration",
                "duration": 5 if format == "video" else None,
                "emotional_tone": self._get_scene_tone(i, scenes)
            })
        
        storyboard_spec = {
            "format": format,
            "theme": story_theme,
            "scenes": storyboard_scenes,
            "total_duration": scenes * 5 if format == "video" else None,
            "style": "engaging"
        }
        
        return ContentAsset(
            id=f"storyboard_{datetime.utcnow().timestamp()}",
            type=ContentType.STORYBOARD,
            title=f"{story_theme} Storyboard",
            data={"theme": story_theme, "scenes": storyboard_scenes},
            design_spec=storyboard_spec,
            emotional_tone="engaging"
        )
    
    def _get_scene_tone(self, index: int, total: int) -> str:
        """Get emotional tone for scene based on position."""
        if index == 0:
            return "hook"
        elif index == total - 1:
            return "call_to_action"
        else:
            return "informative"


class EmotionalContentEnhancer:
    """Adds emotional touch to content."""
    
    def enhance_with_emotion(
        self,
        content: str,
        target_emotion: str = "supportive"
    ) -> str:
        """Enhance content with emotional touch."""
        emotional_additions = {
            "supportive": "I'm here to help you succeed. Let's make this happen together.",
            "energizing": "This is exciting! Let's channel this energy into action.",
            "calm": "Take a deep breath. We've got this, step by step.",
            "professional": "Based on data and best practices, here's the approach.",
            "friendly": "Hey! Let's work through this together. It's going to be great."
        }
        
        addition = emotional_additions.get(target_emotion, "")
        return f"{content}\n\n{addition}"
    
    def add_social_elements(self, content: Dict) -> Dict:
        """Add social connection elements to content."""
        return {
            **content,
            "social_elements": {
                "share_prompt": "Share your thoughts in the comments!",
                "community_call": "Join our community for more insights",
                "collaboration_invite": "Let's collaborate on this"
            }
        }



