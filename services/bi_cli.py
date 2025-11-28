"""Profit OS Chimera CLI - Run growth cycles and manage the command center."""

import sys
from pathlib import Path
import logging
from datetime import datetime
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.config_loader import load_agents, load_plays, load_kpis
from core.orchestrator import Orchestrator
from core.models import Job, Company
from core.playbooks import generate_jobs_from_plays

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_cycle(company_id: str = "demo-company", company_name: str = "Demo Company"):
    """
    Run a demo cycle of the Profit OS system.
    
    Args:
        company_id: Company identifier
        company_name: Company name
    """
    logger.info("=" * 60)
    logger.info("Profit OS Chimera - Growth Cycle")
    logger.info("=" * 60)
    
    # Load configuration
    logger.info("Loading agents, KPIs, and plays...")
    agents = load_agents()
    kpi_definitions = load_kpis()
    plays_cfg = load_plays()
    
    logger.info(f"Loaded {len(agents)} agents, {len(kpi_definitions)} KPIs, {len(plays_cfg)} plays")
    
    # Initialize orchestrator
    orch = Orchestrator(agents)
    
    # Example KPI snapshot (normally computed from data ingestion)
    # This simulates a company with low traffic, decent conversion, no Fiverr orders yet
    kpi_snapshot = {
        "revenue_total_30d": 3200.0,
        "cr_main_funnel": 0.04,  # 4% - below target of 5%
        "sessions_main_30d": 800,  # Good traffic
        "cac_paid": 45.0,  # High CAC
        "retention_60d": 0.22,  # Below target
        "nps": 35.0,
        "aov": 45.0,
        "fiverr_impressions_7d": 50,  # Low visibility
        "fiverr_orders_30d": 0,  # No orders yet
        "shopify_sessions_30d": 150,  # Low traffic
        "shopify_orders_30d": 2,  # Few orders
    }
    
    logger.info("\nCurrent KPI Snapshot:")
    for kpi_name, value in kpi_snapshot.items():
        kpi_def = kpi_definitions.get(kpi_name, {})
        target = kpi_def.get("target") or kpi_def.get("min_healthy")
        status = "✓" if target and value >= target else "⚠"
        logger.info(f"  {status} {kpi_name}: {value} (target: {target})")
    
    # Step 1: Evaluate KPIs
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Evaluating KPIs...")
    kpi_eval_job = Job(
        id=str(uuid.uuid4()),
        type="EVALUATE_KPIS",
        company_id=company_id,
        payload={
            "kpis": kpi_snapshot,
            "kpi_definitions": kpi_definitions
        },
    )
    orch.enqueue(kpi_eval_job)
    
    # Step 2: Generate jobs from triggered plays
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Evaluating play triggers...")
    jobs_for_plays = generate_jobs_from_plays(
        company_id, kpi_snapshot, plays_cfg, kpi_definitions
    )
    
    logger.info(f"Triggered {len(jobs_for_plays)} jobs from plays")
    for job in jobs_for_plays:
        play_name = job.payload.get("play_name", "Unknown")
        logger.info(f"  → {job.type} for play: {play_name}")
        orch.enqueue(job)
    
    # Step 3: Run the orchestrator
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Executing jobs...")
    evidence = orch.run_cycle()
    
    # Step 4: Display results
    logger.info("\n" + "=" * 60)
    logger.info("Step 4: Results & Evidence")
    logger.info("=" * 60)
    
    logger.info(f"\nTotal evidence records: {len(evidence)}")
    for rec in evidence:
        logger.info(f"\n  Event: {rec.event_type}")
        logger.info(f"  Time: {rec.occurred_at}")
        logger.info(f"  Payload: {rec.payload}")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Cycle Summary")
    logger.info("=" * 60)
    
    job_statuses = {}
    for job in orch.jobs.values():
        status = job.status
        job_statuses[status] = job_statuses.get(status, 0) + 1
    
    for status, count in job_statuses.items():
        logger.info(f"  {status}: {count}")
    
    return orch, evidence


def ingest_metrics_cycle(company_id: str, metrics_source: str, metrics_data: dict):
    """
    Run a cycle starting with metric ingestion.
    
    Args:
        company_id: Company identifier
        metrics_source: Source of metrics (e.g., "shopify", "fiverr", "manual")
        metrics_data: Dictionary of KPI name -> value
    """
    logger.info(f"Ingesting metrics from {metrics_source}...")
    
    agents = load_agents()
    orch = Orchestrator(agents)
    
    # Ingest metrics job
    ingest_job = Job(
        id=str(uuid.uuid4()),
        type="INGEST_METRICS",
        company_id=company_id,
        payload={
            "source": metrics_source,
            "metrics": metrics_data
        }
    )
    orch.enqueue(ingest_job)
    orch.run_cycle()
    
    # Then evaluate and suggest plays
    kpi_definitions = load_kpis()
    plays_cfg = load_plays()
    
    jobs_for_plays = generate_jobs_from_plays(
        company_id, metrics_data, plays_cfg, kpi_definitions
    )
    
    for job in jobs_for_plays:
        orch.enqueue(job)
    
    evidence = orch.run_cycle()
    return orch, evidence


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Profit OS Chimera CLI")
    parser.add_argument(
        "--mode",
        choices=["demo", "ingest"],
        default="demo",
        help="Run mode: demo or ingest"
    )
    parser.add_argument(
        "--company-id",
        default="demo-company",
        help="Company identifier"
    )
    parser.add_argument(
        "--company-name",
        default="Demo Company",
        help="Company name"
    )
    
    args = parser.parse_args()
    
    if args.mode == "demo":
        demo_cycle(args.company_id, args.company_name)
    elif args.mode == "ingest":
        # Example: you would pass real metrics here
        print("Ingest mode - pass metrics via API or file")
        print("Example: python bi_cli.py --mode ingest --company-id my-company --metrics-file metrics.json")

