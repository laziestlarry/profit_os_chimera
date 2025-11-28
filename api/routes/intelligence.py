"""AI Business Intelligence routes."""

from fastapi import APIRouter, Depends
from typing import List, Optional, Dict
from modules.ai_intelligence.intelligence import (
    AITrendAnalyzer,
    PartnershipFinder,
    FundingScout,
    ResourceFinder
)

router = APIRouter()


@router.post("/detect-trends")
async def detect_trends(
    categories: Optional[List[str]] = None,
    limit: int = 10,
    business_profile: Optional[Dict] = None
):
    """Detect relevant business trends."""
    if business_profile is None:
        business_profile = {"industry": "AI automation", "stage": "growth"}
    
    analyzer = AITrendAnalyzer(business_profile)
    
    # Convert string categories to enum
    from modules.ai_intelligence.intelligence import TrendCategory
    trend_categories = [TrendCategory[c.upper()] for c in categories] if categories else None
    
    trends = analyzer.detect_trends(trend_categories, limit)
    
    return {
        "trends_found": len(trends),
        "trends": [
            {
                "id": t.id,
                "category": t.category.value,
                "title": t.title,
                "impact_level": t.impact_level,
                "relevance_score": t.relevance_score,
                "actionable_insights": t.actionable_insights
            }
            for t in trends
        ]
    }


@router.post("/analyze-competition")
async def analyze_competition(niche: str, business_profile: Optional[Dict] = None):
    """Analyze competition in a niche."""
    if business_profile is None:
        business_profile = {"industry": "AI automation"}
    
    analyzer = AITrendAnalyzer(business_profile)
    analysis = analyzer.analyze_competition(niche)
    
    return analysis


@router.post("/find-partnerships")
async def find_partnerships(
    partner_types: Optional[List[str]] = None,
    limit: int = 10,
    business_profile: Optional[Dict] = None
):
    """Find partnership opportunities."""
    if business_profile is None:
        business_profile = {"services": ["AI automation", "Growth consulting"]}
    
    finder = PartnershipFinder(business_profile)
    partnerships = finder.find_partnerships(partner_types, limit)
    
    return {
        "partnerships_found": len(partnerships),
        "partnerships": [
            {
                "id": p.id,
                "partner_name": p.partner_name,
                "partner_type": p.partner_type,
                "synergy_score": p.synergy_score,
                "potential_value": p.potential_value
            }
            for p in partnerships
        ]
    }


@router.post("/scout-funding")
async def scout_funding(
    types: Optional[List[str]] = None,
    limit: int = 10,
    business_profile: Optional[Dict] = None
):
    """Scout funding opportunities."""
    if business_profile is None:
        business_profile = {"stage": "growth", "revenue": 5000}
    
    scout = FundingScout(business_profile)
    opportunities = scout.find_funding_opportunities(types, limit)
    
    return {
        "opportunities_found": len(opportunities),
        "opportunities": [
            {
                "id": f.id,
                "type": f.type,
                "name": f.name,
                "amount_range": f.amount_range,
                "match_score": f.match_score,
                "deadline": f.deadline.isoformat() if f.deadline else None
            }
            for f in opportunities
        ]
    }


@router.get("/resources/{category}")
async def find_resources(category: str):
    """Find available resources in a category."""
    finder = ResourceFinder()
    resources = finder.find_resources(category)
    
    return {
        "category": category,
        "resources": resources
    }

