"""Agent system for Profit OS Chimera - Commander agents and execution bots."""

from typing import Dict, Any, List, Optional
from .models import Job, EvidenceRecord
from datetime import datetime
import uuid


class Agent:
    """Base agent class that handles specific job types."""
    
    def __init__(self, name: str, capabilities: List[str], metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.capabilities = set(capabilities)
        self.metadata = metadata or {}
    
    def can_handle(self, job_type: str) -> bool:
        """Check if this agent can handle a specific job type."""
        return job_type in self.capabilities
    
    def handle(self, job: Job) -> List[EvidenceRecord]:
        """
        Process a job and return evidence records.
        Override in subclasses or extend with LLM calls for real logic.
        """
        if job.type == "EVALUATE_KPIS":
            return self._handle_evaluate_kpis(job)
        elif job.type == "SUGGEST_PLAYS":
            return self._handle_suggest_plays(job)
        elif job.type == "INGEST_METRICS":
            return self._handle_ingest_metrics(job)
        elif job.type == "LOG_EVIDENCE":
            return self._handle_log_evidence(job)
        elif job.type.startswith("EXECUTE_PLAY_"):
            return self._handle_execute_play(job)
        elif job.type == "PLAN_JOB_QUEUE_FOR_PLAY":
            return self._handle_plan_job_queue(job)
        elif job.type == "TRAIN_AGENT":
            return self._handle_train_agent(job)
        else:
            return []
    
    def _handle_evaluate_kpis(self, job: Job) -> List[EvidenceRecord]:
        """Evaluate KPIs and determine status."""
        kpis = job.payload.get("kpis", {})
        kpi_defs = job.payload.get("kpi_definitions", {})
        
        evaluations = []
        for kpi_name, value in kpis.items():
            kpi_def = kpi_defs.get(kpi_name, {})
            target = kpi_def.get("target")
            warning_ratio = kpi_def.get("warning_ratio_below", 0.8)
            critical_ratio = kpi_def.get("critical_ratio_below", 0.5)
            
            status = "ok"
            if target:
                ratio = value / target if target > 0 else 0
                if ratio < critical_ratio:
                    status = "critical"
                elif ratio < warning_ratio:
                    status = "warning"
            
            evaluations.append({
                "kpi": kpi_name,
                "value": value,
                "target": target,
                "status": status
            })
        
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="kpi_evaluated",
            occurred_at=datetime.utcnow(),
            payload={"evaluations": evaluations}
        )]
    
    def _handle_suggest_plays(self, job: Job) -> List[EvidenceRecord]:
        """Suggest growth plays based on KPI status."""
        # This would normally use playbook logic
        # For now, return a placeholder
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="plays_suggested",
            occurred_at=datetime.utcnow(),
            payload={
                "plays": job.payload.get("suggested_plays", []),
                "rationale": "Based on KPI evaluation and playbook triggers"
            }
        )]
    
    def _handle_ingest_metrics(self, job: Job) -> List[EvidenceRecord]:
        """Ingest metrics from data sources."""
        source = job.payload.get("source", "unknown")
        metrics = job.payload.get("metrics", {})
        
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="metrics_ingested",
            occurred_at=datetime.utcnow(),
            payload={
                "source": source,
                "metrics_count": len(metrics),
                "metrics": metrics
            }
        )]
    
    def _handle_log_evidence(self, job: Job) -> List[EvidenceRecord]:
        """Log evidence of an action or outcome."""
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type=job.payload.get("event_type", "evidence_logged"),
            occurred_at=datetime.utcnow(),
            payload=job.payload.get("evidence_data", {})
        )]
    
    def _handle_execute_play(self, job: Job) -> List[EvidenceRecord]:
        """Execute a growth play."""
        play_id = job.payload.get("play_id", "unknown")
        handler = job.payload.get("handler", "unknown")
        params = job.payload.get("params", {})
        
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="play_executed",
            occurred_at=datetime.utcnow(),
            payload={
                "play_id": play_id,
                "handler": handler,
                "params": params,
                "status": "completed"
            }
        )]
    
    def _handle_plan_job_queue(self, job: Job) -> List[EvidenceRecord]:
        """Plan a job queue for a specific play."""
        play_id = job.payload.get("play_id", "unknown")
        
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="job_queue_planned",
            occurred_at=datetime.utcnow(),
            payload={
                "play_id": play_id,
                "jobs_planned": job.payload.get("job_count", 0)
            }
        )]
    
    def _handle_train_agent(self, job: Job) -> List[EvidenceRecord]:
        """Train an agent with new scenarios."""
        agent_id = job.payload.get("agent_id", "unknown")
        
        return [EvidenceRecord(
            id=str(uuid.uuid4()),
            company_id=job.company_id,
            job_id=job.id,
            event_type="agent_trained",
            occurred_at=datetime.utcnow(),
            payload={
                "agent_id": agent_id,
                "training_scenarios": job.payload.get("scenarios_count", 0)
            }
        )]

