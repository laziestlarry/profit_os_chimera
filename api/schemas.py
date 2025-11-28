"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class KPIStatus(str, Enum):
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None
    meta_data: Optional[Dict] = {}  # Renamed from metadata


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# KPI Schemas
class KPICreate(BaseModel):
    company_id: str
    name: str
    value: float
    target: Optional[float] = None
    status: Optional[KPIStatus] = KPIStatus.UNKNOWN
    metadata: Optional[Dict] = {}


class KPIResponse(BaseModel):
    id: str
    company_id: str
    name: str
    value: float
    target: Optional[float] = None
    status: KPIStatus
    metadata: Dict
    recorded_at: datetime
    
    class Config:
        from_attributes = True


class KPISnapshot(BaseModel):
    """KPI snapshot for play evaluation."""
    kpis: Dict[str, float] = Field(..., description="KPI name to value mapping")


# Job Schemas
class JobCreate(BaseModel):
    company_id: str
    type: str
    payload: Dict = {}


class JobResponse(BaseModel):
    id: str
    company_id: str
    type: str
    payload: Dict
    status: JobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Evidence Schemas
class EvidenceCreate(BaseModel):
    company_id: str
    job_id: Optional[str] = None
    event_type: str
    payload: Dict = {}


class EvidenceResponse(BaseModel):
    id: str
    company_id: str
    job_id: Optional[str] = None
    event_type: str
    payload: Dict
    occurred_at: datetime
    
    class Config:
        from_attributes = True


# Cycle Schemas
class CycleRequest(BaseModel):
    company_id: str
    kpi_snapshot: Dict[str, float]


class CycleResponse(BaseModel):
    cycle_id: str
    company_id: str
    jobs_created: int
    plays_triggered: List[str]
    evidence_count: int
    status: str

