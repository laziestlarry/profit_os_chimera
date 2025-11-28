"""Job management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.connection import get_db
from database.models import Job, JobStatus
from api.schemas import JobCreate, JobResponse

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job."""
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/company/{company_id}", response_model=List[JobResponse])
async def get_company_jobs(
    company_id: str,
    status: Optional[JobStatus] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get jobs for a company."""
    query = db.query(Job).filter(Job.company_id == company_id)
    if status:
        query = query.filter(Job.status == status)
    jobs = query.order_by(Job.created_at.desc()).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """Get a specific job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job



