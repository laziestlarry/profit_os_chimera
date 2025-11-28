"""Core data models for Profit OS Chimera."""

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional
from datetime import datetime
import uuid

Status = Literal["queued", "running", "succeeded", "failed"]


@dataclass
class Company:
    """Represents a company/client in the Profit OS system."""
    id: str
    name: str
    industry: str
    size: str  # e.g., "solo", "smb", "mid", "enterprise"
    metadata: Dict = field(default_factory=dict)


@dataclass
class KPI:
    """Key Performance Indicator with status evaluation."""
    name: str
    value: float
    target: Optional[float] = None
    status: Optional[Literal["ok", "warning", "critical"]] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class Job:
    """A single unit of work in the Profit OS system."""
    id: str
    type: str
    company_id: str
    payload: Dict
    status: Status = "queued"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Ensure timestamps are timezone-aware if needed."""
        if isinstance(self.created_at, str):
            # Handle ISO string format if needed
            pass


@dataclass
class EvidenceRecord:
    """Records evidence of actions and their outcomes."""
    id: str
    company_id: str
    job_id: str
    event_type: str
    occurred_at: datetime
    payload: Dict

    def __post_init__(self):
        """Ensure timestamps are timezone-aware if needed."""
        if isinstance(self.occurred_at, str):
            # Handle ISO string format if needed
            pass

