"""Evidence records routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database.connection import get_db
from database.models import EvidenceRecord
from api.schemas import EvidenceCreate, EvidenceResponse

router = APIRouter()


@router.post("/", response_model=EvidenceResponse, status_code=201)
async def create_evidence(evidence: EvidenceCreate, db: Session = Depends(get_db)):
    """Create an evidence record."""
    db_evidence = EvidenceRecord(**evidence.dict())
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence


@router.get("/company/{company_id}", response_model=List[EvidenceResponse])
async def get_company_evidence(
    company_id: str,
    days: Optional[int] = 30,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get evidence records for a company."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    evidence = db.query(EvidenceRecord).filter(
        EvidenceRecord.company_id == company_id,
        EvidenceRecord.occurred_at >= cutoff
    ).order_by(EvidenceRecord.occurred_at.desc()).limit(limit).all()
    return evidence


@router.get("/{evidence_id}", response_model=EvidenceResponse)
async def get_evidence(evidence_id: str, db: Session = Depends(get_db)):
    """Get a specific evidence record."""
    evidence = db.query(EvidenceRecord).filter(EvidenceRecord.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence



