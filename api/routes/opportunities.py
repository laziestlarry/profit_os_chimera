"""Opportunity Hunter routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from database.connection import get_db
from modules.commander_hunter.hunter import OpportunityHunter, IncomeStreamAnalyzer
from api.schemas import CompanyResponse

router = APIRouter()


@router.post("/hunt/{company_id}")
async def hunt_opportunities(
    company_id: str,
    opportunity_types: Optional[List[str]] = None,
    max_results: int = 20,
    db: Session = Depends(get_db)
):
    """Hunt for income opportunities for a company."""
    # Get company profile (would load from database)
    user_profile = {
        "skills": ["AI automation", "Content creation", "E-commerce"],
        "goals": ["Increase revenue", "Diversify income"],
        "time_availability": "flexible"
    }
    
    hunter = OpportunityHunter(user_profile)
    
    # Convert string types to enum if needed
    from modules.commander_hunter.hunter import OpportunityType
    types = [OpportunityType[t.upper()] for t in opportunity_types] if opportunity_types else None
    
    opportunities = hunter.hunt_opportunities(types, max_results)
    
    return {
        "company_id": company_id,
        "opportunities_found": len(opportunities),
        "opportunities": [
            {
                "id": opp.id,
                "type": opp.type.value,
                "title": opp.title,
                "estimated_income": opp.estimated_income,
                "time_commitment": opp.time_commitment,
                "match_score": opp.match_score,
                "auto_apply_ready": opp.auto_apply_ready
            }
            for opp in opportunities
        ]
    }


@router.post("/auto-apply/{company_id}")
async def auto_apply_opportunity(
    company_id: str,
    opportunity_id: str,
    db: Session = Depends(get_db)
):
    """Auto-apply to an opportunity."""
    # In production, would load opportunity from database
    from modules.commander_hunter.hunter import Opportunity, OpportunityType
    
    # Mock opportunity for demo
    opportunity = Opportunity(
        id=opportunity_id,
        type=OpportunityType.FREELANCE,
        title="AI Automation Setup",
        description="Test",
        estimated_income={"min": 97, "max": 597, "unit": "USD/gig"},
        time_commitment="3-7 days",
        skills_required=["AI tools"],
        platform="Fiverr",
        auto_apply_ready=True
    )
    
    user_profile = {"skills": ["AI automation"]}
    hunter = OpportunityHunter(user_profile)
    
    result = hunter.auto_apply(opportunity)
    
    return result


@router.post("/analyze-streams/{company_id}")
async def analyze_income_streams(
    company_id: str,
    streams: List[Dict],
    db: Session = Depends(get_db)
):
    """Analyze current income streams and suggest optimizations."""
    user_profile = {"goals": ["Optimize income"]}
    analyzer = IncomeStreamAnalyzer(user_profile)
    
    analysis = analyzer.analyze_current_streams(streams)
    
    return {
        "company_id": company_id,
        "analysis": analysis
    }

