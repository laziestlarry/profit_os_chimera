"""Configuration loader for Profit OS Chimera - loads YAML configs and instantiates agents."""

from typing import List, Dict, Any
from pathlib import Path
import yaml
from .agents import Agent

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "configs"


def load_yaml(name: str) -> Dict[str, Any]:
    """Load a YAML file from the configs directory."""
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_agents() -> List[Agent]:
    """Load agents from agents.yml and instantiate Agent objects."""
    raw = load_yaml("agents.yml")
    agents_cfg = raw.get("agents", [])
    agents: List[Agent] = []
    
    for cfg in agents_cfg:
        agent = Agent(
            name=cfg["id"],
            capabilities=cfg.get("handles", []),
            metadata=cfg
        )
        agents.append(agent)
    
    return agents


def load_kpis() -> Dict[str, Dict[str, Any]]:
    """Load KPIs from kpis.yml and return as a dictionary."""
    raw = load_yaml("kpis.yml")
    kpis = raw.get("kpis", [])
    return {k["name"]: k for k in kpis}


def load_plays() -> List[Dict[str, Any]]:
    """Load plays from plays.yml and return as a list."""
    raw = load_yaml("plays.yml")
    return raw.get("plays", [])

