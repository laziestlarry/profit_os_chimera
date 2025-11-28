"""Growth cycle execution routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Company, Job, EvidenceRecord
from api.schemas import CycleRequest, CycleResponse
from core.config_loader import load_agents, load_plays, load_kpis
from core.orchestrator import Orchestrator
from core.playbooks import generate_jobs_from_plays
from core.models import Job as CoreJob
import uuid

router = APIRouter()


@router.post("/run", response_model=CycleResponse)
async def run_growth_cycle(cycle: CycleRequest, db: Session = Depends(get_db)):
    """Run a complete growth cycle for a company."""
    # Verify company exists
    company = db.query(Company).filter(Company.id == cycle.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Load configuration
    agents = load_agents()
    plays_cfg = load_plays()
    kpi_definitions = load_kpis()
    
    # Create orchestrator
    orch = Orchestrator(agents)
    
    # Generate jobs from triggered plays
    jobs = generate_jobs_from_plays(
        cycle.company_id,
        cycle.kpi_snapshot,
        plays_cfg,
        kpi_definitions
    )
    
    # Convert core jobs to database jobs and enqueue
    triggered_plays = set()
    for job in jobs:
        triggered_plays.add(job.payload.get("play_name", "unknown"))
        
        # Save to database
        db_job = Job(
            id=job.id,
            company_id=job.company_id,
            type=job.type,
            payload=job.payload,
            status=job.status.value
        )
        db.add(db_job)
        orch.enqueue(job)
    
    db.commit()
    
    # Run orchestrator
    evidence = orch.run_cycle()
    
    # Save evidence to database
    for ev in evidence:
        db_evidence = EvidenceRecord(
            id=ev.id,
            company_id=ev.company_id,
            job_id=ev.job_id,
            event_type=ev.event_type,
            payload=ev.payload
        )
        db.add(db_evidence)
    
    db.commit()
    
    return CycleResponse(
        cycle_id=str(uuid.uuid4()),
        company_id=cycle.company_id,
        jobs_created=len(jobs),
        plays_triggered=list(triggered_plays),
        evidence_count=len(evidence),
        status="completed"
    )



