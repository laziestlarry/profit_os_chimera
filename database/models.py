"""SQLAlchemy database models for Profit OS Chimera."""

from sqlalchemy import Column, String, Float, Integer, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database.connection import Base
import uuid


class JobStatus(str, enum.Enum):
    """Job status enumeration."""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class KPIStatus(str, enum.Enum):
    """KPI status enumeration."""
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class Company(Base):
    """Company model."""
    __tablename__ = "companies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    industry = Column(String)
    size = Column(String)  # solo, smb, mid, enterprise
    meta_data = Column(JSON, default=dict)  # Renamed from metadata (reserved in SQLAlchemy)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    kpis = relationship("KPI", back_populates="company", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")
    evidence = relationship("EvidenceRecord", back_populates="company", cascade="all, delete-orphan")


class KPI(Base):
    """KPI snapshot model."""
    __tablename__ = "kpis"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    target = Column(Float)
    status = Column(Enum(KPIStatus), default=KPIStatus.UNKNOWN)
    meta_data = Column(JSON, default=dict)  # Renamed from metadata
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    company = relationship("Company", back_populates="kpis")


class Job(Base):
    """Job model."""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    payload = Column(JSON, default=dict)
    status = Column(Enum(JobStatus), default=JobStatus.QUEUED, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    evidence = relationship("EvidenceRecord", back_populates="job")


class EvidenceRecord(Base):
    """Evidence record model."""
    __tablename__ = "evidence_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSON, default=dict)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    company = relationship("Company", back_populates="evidence")
    job = relationship("Job", back_populates="evidence")

