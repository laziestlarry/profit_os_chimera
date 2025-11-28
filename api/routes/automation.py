"""Automation workflows routes."""

from fastapi import APIRouter, Depends
from typing import List, Dict, Optional
from modules.automation.workflows import AutomationEngine, AutomationType

router = APIRouter()

# Global automation engine instance
automation_engine = AutomationEngine()


@router.post("/audit-processes")
async def audit_manual_processes(processes: List[Dict]):
    """Audit processes to identify automation opportunities."""
    opportunities = automation_engine.audit_manual_processes(processes)
    
    return {
        "opportunities_found": len(opportunities),
        "opportunities": opportunities
    }


@router.post("/create-workflow")
async def create_workflow(
    name: str,
    type: str,
    trigger: Dict,
    steps: List[Dict],
    schedule: Optional[str] = None
):
    """Create an automation workflow."""
    automation_type = AutomationType[type.upper()] if type.upper() in AutomationType.__members__ else AutomationType.CONTENT_CREATION
    
    workflow = automation_engine.create_workflow(
        name=name,
        type=automation_type,
        trigger=trigger,
        steps=steps,
        schedule=schedule
    )
    
    return {
        "workflow_id": workflow.id,
        "name": workflow.name,
        "status": "created"
    }


@router.post("/minimize-manual-work")
async def minimize_manual_work(current_work: Dict):
    """Identify and implement automations to minimize manual work."""
    result = automation_engine.minimize_manual_work(current_work)
    
    return result


@router.post("/setup-recurring")
async def setup_recurring_automations(workflow_ids: List[str]):
    """Setup recurring automated tasks."""
    workflows = [w for w in automation_engine.workflows if w.id in workflow_ids]
    result = automation_engine.setup_recurring_automations(workflows)
    
    return result

