# Profit OS Chimera v0.1.0 Enhanced
**AI-Powered Growth Operating System with Enhanced Modules**

A Chimera-style growth engine that turns scattered data, ideas, and experiments into a structured, repeatable system for revenue and valuation growth.

**NEW in v0.1.0:**
- ✅ Lazy Larry Personal Assistant (multi-layer profiling, chatbot)
- ✅ Commander Opportunity Hunter (income streams, freelance, remote jobs)
- ✅ Social Media Automation Module (productizable)
- ✅ AI Business Intelligence (trends, partnerships, funding)
- ✅ Content & Design Creator (dashboards, infographics, storyboards)
- ✅ Automation Workflows (minimize human work)

---

## What This Is

Profit OS Chimera is an **AI-powered growth operating system** that:

- Ingests key metrics (revenue, traffic, funnels, retention, CAC, satisfaction)
- Evaluates performance against clear KPIs and thresholds
- Triggers curated "growth plays" based on actual numbers
- Orchestrates a queue of concrete tasks for your team or automation stack
- Logs evidence and builds proof of what truly moves revenue and valuation

**It's not "just dashboards"** – it's a **BI + Operations + Growth brain** that tells you what to do next.

---

## Quick Start

### Installation

```bash
# Clone or navigate to the profit_os_chimera directory
cd profit_os_chimera

# Install dependencies
pip install -r requirements.txt
```

### Run a Demo Cycle

```bash
# Run the demo cycle to see the system in action
python services/bi_cli.py --mode demo

# Or with custom company info
python services/bi_cli.py --mode demo --company-id my-company --company-name "My Company"
```

### Expected Output

The demo cycle will:
1. Load agents, KPIs, and plays from YAML configs
2. Evaluate a sample KPI snapshot
3. Trigger matching growth plays
4. Generate jobs for execution
5. Run the orchestrator
6. Display evidence records

---

## Architecture

### Core Components

- **Data Layer** (`core/models.py`, `database/models.py`)
  - Company, KPI, Job, EvidenceRecord entities
  - SQLAlchemy ORM with PostgreSQL support

- **Intelligence Layer** (`core/playbooks.py`)
  - KPI evaluation and play triggering logic

- **Execution Layer** (`core/orchestrator.py`, `core/agents.py`)
  - Job queue management and agent routing

- **API Layer** (`api/`)
  - FastAPI REST API with 11 route modules
  - Swagger/ReDoc documentation

- **Enhanced Modules** (`modules/`)
  - Lazy Larry Personal Assistant
  - Commander Opportunity Hunter
  - Social Media Automation
  - AI Business Intelligence
  - Content & Design Creator
  - Automation Workflows

- **Configuration** (`configs/`)
  - `agents.yml` – 16 agents (commanders + bots)
  - `kpis.yml` – 19 KPIs including new metrics
  - `plays.yml` – 12 growth plays including enhanced plays

### Directory Structure

```
profit_os_chimera/
├── core/                 # Core Python modules
│   ├── models.py        # Data models
│   ├── agents.py        # Agent system
│   ├── orchestrator.py  # Job orchestration
│   ├── playbooks.py     # Play evaluation logic
│   └── config_loader.py # YAML config loader
├── configs/             # YAML configuration files
│   ├── agents.yml       # Agent definitions
│   ├── kpis.yml         # KPI definitions
│   └── plays.yml        # Growth plays
├── services/            # Service scripts
│   └── bi_cli.py        # CLI for running cycles
├── docs/                # Documentation
│   ├── PRODUCTIZED_OFFER.md
│   ├── OPERATING_MANUAL.md
│   ├── ProfitOS_OnePager.md
│   ├── ProfitOS_DiscoveryScript.md
│   ├── FIVERR_GIG_AI_YOUTUBE_AUTOMATION.md
│   └── SHOPIFY_ZEN_CALM_STARTER_PACK.md
├── training/            # Training data (future)
│   └── agents/
├── evidence/            # Evidence logs (future)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## Usage

### Running Growth Cycles

```python
from core.config_loader import load_agents, load_plays, load_kpis
from core.orchestrator import Orchestrator
from core.models import Job
from core.playbooks import generate_jobs_from_plays
import uuid

# Load configuration
agents = load_agents()
kpi_definitions = load_kpis()
plays_cfg = load_plays()

# Initialize orchestrator
orch = Orchestrator(agents)

# Your KPI snapshot (from data ingestion)
kpi_snapshot = {
    "revenue_total_30d": 5000.0,
    "cr_main_funnel": 0.04,
    "sessions_main_30d": 800,
    # ... more KPIs
}

# Generate jobs from triggered plays
jobs = generate_jobs_from_plays(
    company_id="my-company",
    kpi_snapshot=kpi_snapshot,
    plays_cfg=plays_cfg,
    kpi_definitions=kpi_definitions
)

# Enqueue and run
for job in jobs:
    orch.enqueue(job)

evidence = orch.run_cycle()
```

### Adding Custom KPIs

Edit `configs/kpis.yml`:

```yaml
kpis:
  - name: my_custom_kpi
    label: "My Custom KPI"
    unit: "count"
    category: "custom"
    dimension: "company"
    target: 100
    warning_ratio_below: 0.8
    critical_ratio_below: 0.5
    description: "Description of my KPI"
```

### Adding Custom Plays

Edit `configs/plays.yml`:

```yaml
plays:
  - id: my_custom_play
    name: "My Custom Play"
    owner_agent: growth_commander_ai
    intent: "What this play does"
    triggers:
      all:
        - kpi: "my_custom_kpi"
          relation: "absolute"
          operator: "<"
          value: 50
    impact_hypothesis: "Expected impact"
    job_plan:
      - type: "EXECUTE_PLAY_GROWTH"
        handler: "copy_bot"
        params:
          action: "do_something"
```

---

## Revenue Assets Included

### Immediate Revenue Assets

1. **Fiverr Gig**
   - **File:** `docs/FIVERR_GIG_AI_YOUTUBE_AUTOMATION.md`
   - **Offer:** AI-Powered YouTube Automation & Content System Setup
   - **Packages:** Starter ($97), Pro ($297), Empire ($597)
   - **Status:** Ready to publish

2. **Shopify Product**
   - **File:** `docs/SHOPIFY_ZEN_CALM_STARTER_PACK.md`
   - **Offer:** Zen Calm Starter Pack – 3-Piece Digital Wall Art Collection
   - **Price:** $29.99 (bundle)
   - **Status:** Ready to publish

### Productizable Modules (New Revenue Streams)

3. **Social Media Automation System**
   - **File:** `docs/PRODUCT_SOCIAL_AUTOMATION.md`
   - **Pricing:** $97-$497/month SaaS
   - **Potential:** $24,520/month at scale
   - **Status:** Core complete, ready to productize

4. **Lazy Larry Personal Assistant**
   - **File:** `docs/PRODUCT_LAZY_LARRY_ASSISTANT.md`
   - **Pricing:** $49-$149 desktop, $19-$49/month SaaS
   - **Potential:** $30,750 one-time + $6,250/month
   - **Status:** Core complete, needs desktop wrapper

5. **Opportunity Hunter Service**
   - **File:** `docs/PRODUCT_OPPORTUNITY_HUNTER.md`
   - **Pricing:** $97-$497/month
   - **Potential:** $49,040/month at scale
   - **Status:** Core complete, ready to launch

---

## Documentation

- **Productized Offer:** `docs/PRODUCTIZED_OFFER.md` – Client-facing offer document
- **Operating Manual:** `docs/OPERATING_MANUAL.md` – Internal operations guide
- **Sales Materials:** 
  - `docs/ProfitOS_OnePager.md` – 1-page sales sheet
  - `docs/ProfitOS_DiscoveryScript.md` – Discovery call script

---

## Next Steps

1. **Test the System**
   ```bash
   python services/bi_cli.py --mode demo
   ```

2. **Customize for Your Business**
   - Edit `configs/kpis.yml` with your KPIs
   - Edit `configs/plays.yml` with your growth plays
   - Adjust `configs/agents.yml` as needed

3. **Publish Revenue Assets**
   - Use `docs/FIVERR_GIG_AI_YOUTUBE_AUTOMATION.md` to create your Fiverr gig
   - Use `docs/SHOPIFY_ZEN_CALM_STARTER_PACK.md` to create your Shopify product

4. **Integrate Real Data**
   - Connect to your analytics tools (Shopify, Fiverr, Stripe, etc.)
   - Set up data ingestion jobs
   - Run regular growth cycles

---

## Contributing

This is a Profit OS system for AutonomaX / ProPulse / Lazy Larry ecosystem. For internal use and client deployments.

---

## License

Internal use for AutonomaX / ProPulse. White-label licensing available for agencies (see PRODUCTIZED_OFFER.md).

---

## Support

For questions or support:
- Review `docs/OPERATING_MANUAL.md`
- Check configuration files in `configs/`
- Run demo cycles to understand the flow

---

**by AutonomaX / ProPulse – powered by Lazy Larry**

# profit_os_chimera
