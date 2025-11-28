"""Playbook system for Profit OS Chimera - evaluates triggers and generates jobs."""

from typing import Dict, Any, List
from .models import Job
from datetime import datetime
import uuid


def evaluate_triggers(kpi_snapshot: Dict[str, float], play: Dict[str, Any], kpi_definitions: Dict[str, Dict[str, Any]]) -> bool:
    """
    Return True if play should trigger for the given KPI snapshot.
    
    Args:
        kpi_snapshot: Current KPI values (name -> value)
        play: Play definition from plays.yml
        kpi_definitions: KPI definitions from kpis.yml (for targets/thresholds)
    """
    def check_clause(clause: Dict[str, Any]) -> bool:
        name = clause["kpi"]
        relation = clause.get("relation", "absolute")
        operator = clause["operator"]
        value = clause["value"]
        
        actual = kpi_snapshot.get(name)
        if actual is None:
            return False
        
        # Handle ratio_to_target relation
        if relation == "ratio_to_target":
            kpi_def = kpi_definitions.get(name, {})
            target = kpi_def.get("target")
            if target and target > 0:
                metric_val = actual / target
            else:
                return False
        else:
            metric_val = actual
        
        # Evaluate operator
        if operator == "<":
            return metric_val < value
        elif operator == "<=":
            return metric_val <= value
        elif operator == ">":
            return metric_val > value
        elif operator == ">=":
            return metric_val >= value
        elif operator == "==":
            return metric_val == value
        elif operator == "!=":
            return metric_val != value
        
        return False
    
    triggers = play.get("triggers", {})
    all_clauses = triggers.get("all", [])
    any_clauses = triggers.get("any", [])
    
    # All clauses must pass
    if all_clauses and not all(check_clause(c) for c in all_clauses):
        return False
    
    # At least one any clause must pass
    if any_clauses and not any(check_clause(c) for c in any_clauses):
        return False
    
    return True


def generate_jobs_from_plays(
    company_id: str,
    kpi_snapshot: Dict[str, float],
    plays_cfg: List[Dict[str, Any]],
    kpi_definitions: Dict[str, Dict[str, Any]]
) -> List[Job]:
    """
    Given current KPI values, return Jobs for all matching plays.
    
    Args:
        company_id: Company identifier
        kpi_snapshot: Current KPI values
        plays_cfg: List of play definitions from plays.yml
        kpi_definitions: KPI definitions for trigger evaluation
    
    Returns:
        List of Jobs to execute for triggered plays
    """
    jobs: List[Job] = []
    
    for play in plays_cfg:
        if not evaluate_triggers(kpi_snapshot, play, kpi_definitions):
            continue
        
        # Generate jobs from the play's job_plan
        for step in play.get("job_plan", []):
            job = Job(
                id=str(uuid.uuid4()),
                type=step["type"],
                company_id=company_id,
                payload={
                    "play_id": play["id"],
                    "play_name": play.get("name", ""),
                    "handler": step.get("handler"),
                    "params": step.get("params", {}),
                    "created_at": datetime.utcnow().isoformat(),
                },
            )
            jobs.append(job)
    
    return jobs

