"""Orchestrator for Profit OS Chimera - manages job queue and agent routing."""

from typing import List, Dict, Optional
from .models import Job, EvidenceRecord
from .agents import Agent
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates job execution across agents."""
    
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.jobs: Dict[str, Job] = {}
        self.evidence: List[EvidenceRecord] = []
    
    def enqueue(self, job: Job):
        """Add a job to the queue."""
        self.jobs[job.id] = job
        logger.info(f"Job {job.id} ({job.type}) enqueued for company {job.company_id}")
    
    def run_cycle(self) -> List[EvidenceRecord]:
        """
        Run one cycle of the orchestrator.
        Processes all queued jobs and returns evidence records.
        """
        evidence_batch = []
        
        for job in list(self.jobs.values()):
            if job.status != "queued":
                continue
            
            agent = self._select_agent(job)
            if not agent:
                logger.warning(f"No agent found for job type: {job.type}")
                job.status = "failed"
                job.updated_at = datetime.utcnow()
                continue
            
            job.status = "running"
            job.updated_at = datetime.utcnow()
            
            try:
                records = agent.handle(job)
                evidence_batch.extend(records)
                self.evidence.extend(records)
                job.status = "succeeded"
                logger.info(f"Job {job.id} succeeded, produced {len(records)} evidence records")
            except Exception as e:
                job.status = "failed"
                error_record = EvidenceRecord(
                    id=str(uuid.uuid4()),
                    company_id=job.company_id,
                    job_id=job.id,
                    event_type="error",
                    occurred_at=datetime.utcnow(),
                    payload={"error": str(e), "error_type": type(e).__name__}
                )
                evidence_batch.append(error_record)
                self.evidence.append(error_record)
                logger.error(f"Job {job.id} failed: {e}", exc_info=True)
            finally:
                job.updated_at = datetime.utcnow()
        
        return evidence_batch
    
    def _select_agent(self, job: Job) -> Optional[Agent]:
        """Select the appropriate agent for a job type."""
        for agent in self.agents:
            if agent.can_handle(job.type):
                return agent
        return None
    
    def get_job_status(self, job_id: str) -> Optional[Job]:
        """Get the status of a specific job."""
        return self.jobs.get(job_id)
    
    def get_evidence_for_company(self, company_id: str) -> List[EvidenceRecord]:
        """Get all evidence records for a company."""
        return [e for e in self.evidence if e.company_id == company_id]
    
    def get_evidence_for_job(self, job_id: str) -> List[EvidenceRecord]:
        """Get all evidence records for a specific job."""
        return [e for e in self.evidence if e.job_id == job_id]

