"""FastAPI main application for Profit OS Chimera."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.routes import kpis, plays, jobs, evidence, companies, cycles
from api.routes import lazy_larry, opportunities, social, intelligence, content, automation
from database.connection import init_db, get_db
from core.config_loader import load_agents, load_kpis, load_plays

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    # Startup
    logger.info("Initializing Profit OS Chimera API v0.1.0")
    init_db()
    logger.info("Database initialized")
    
    # Load configs
    try:
        agents = load_agents()
        kpi_defs = load_kpis()
        plays_cfg = load_plays()
        logger.info(f"Loaded {len(agents)} agents, {len(kpi_defs)} KPIs, {len(plays_cfg)} plays")
    except Exception as e:
        logger.warning(f"Config loading warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Profit OS Chimera API")


app = FastAPI(
    title="Profit OS Chimera API",
    description="AI-Powered Growth Operating System - Production API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(kpis.router, prefix="/api/v1/kpis", tags=["KPIs"])
app.include_router(plays.router, prefix="/api/v1/plays", tags=["Plays"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(evidence.router, prefix="/api/v1/evidence", tags=["Evidence"])
app.include_router(cycles.router, prefix="/api/v1/cycles", tags=["Growth Cycles"])
app.include_router(lazy_larry.router, prefix="/api/v1/lazy-larry", tags=["Lazy Larry Assistant"])
app.include_router(opportunities.router, prefix="/api/v1/opportunities", tags=["Opportunity Hunter"])
app.include_router(social.router, prefix="/api/v1/social", tags=["Social Media Automation"])
app.include_router(intelligence.router, prefix="/api/v1/intelligence", tags=["AI Business Intelligence"])
app.include_router(content.router, prefix="/api/v1/content", tags=["Content & Design"])
app.include_router(automation.router, prefix="/api/v1/automation", tags=["Automation Workflows"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Profit OS Chimera API",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "Profit OS Chimera"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

