"""Growth plays routes."""

from fastapi import APIRouter, Depends
from typing import List, Dict
from core.config_loader import load_plays, load_kpis
from api.schemas import KPISnapshot

router = APIRouter()


@router.get("/", response_model=List[Dict])
async def list_plays():
    """List all available growth plays."""
    plays = load_plays()
    return plays


@router.post("/evaluate")
async def evaluate_plays(snapshot: KPISnapshot):
    """Evaluate which plays should trigger for given KPI snapshot."""
    from core.playbooks import evaluate_triggers, generate_jobs_from_plays
    
    plays_cfg = load_plays()
    kpi_definitions = load_kpis()
    
    triggered_plays = []
    for play in plays_cfg:
        if evaluate_triggers(snapshot.kpis, play, kpi_definitions):
            triggered_plays.append({
                "id": play["id"],
                "name": play["name"],
                "intent": play.get("intent", ""),
                "impact_hypothesis": play.get("impact_hypothesis", "")
            })
    
    return {
        "triggered_plays": triggered_plays,
        "total_plays": len(plays_cfg),
        "triggered_count": len(triggered_plays)
    }



