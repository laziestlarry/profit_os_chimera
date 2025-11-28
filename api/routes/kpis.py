"""KPI management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database.connection import get_db
from database.models import KPI
from api.schemas import KPICreate, KPIResponse

router = APIRouter()


@router.post("/", response_model=KPIResponse, status_code=201)
async def create_kpi(kpi: KPICreate, db: Session = Depends(get_db)):
    """Record a KPI snapshot."""
    db_kpi = KPI(**kpi.dict())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi


@router.get("/company/{company_id}", response_model=List[KPIResponse])
async def get_company_kpis(
    company_id: str,
    days: Optional[int] = 30,
    db: Session = Depends(get_db)
):
    """Get KPIs for a company."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    kpis = db.query(KPI).filter(
        KPI.company_id == company_id,
        KPI.recorded_at >= cutoff
    ).order_by(KPI.recorded_at.desc()).all()
    return kpis


@router.get("/company/{company_id}/latest", response_model=List[KPIResponse])
async def get_latest_kpis(company_id: str, db: Session = Depends(get_db)):
    """Get latest KPI snapshot for each metric."""
    # Get the most recent KPI for each name
    subquery = db.query(
        KPI.name,
        db.func.max(KPI.recorded_at).label('max_time')
    ).filter(
        KPI.company_id == company_id
    ).group_by(KPI.name).subquery()
    
    kpis = db.query(KPI).join(
        subquery,
        (KPI.name == subquery.c.name) & (KPI.recorded_at == subquery.c.max_time)
    ).filter(KPI.company_id == company_id).all()
    
    return kpis



