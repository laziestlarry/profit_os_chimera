"""Company management routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from database.models import Company
from api.schemas import CompanyCreate, CompanyResponse

router = APIRouter()


@router.post("/", response_model=CompanyResponse, status_code=201)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company."""
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/", response_model=List[CompanyResponse])
async def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all companies."""
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str, db: Session = Depends(get_db)):
    """Get a specific company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company



