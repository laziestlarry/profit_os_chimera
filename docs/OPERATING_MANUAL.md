# Profit OS / Chimera Operating Manual
_Internal manual for running the Growth Command Center_

---

## 1. Purpose

This manual is for **internal operators and AI agents** running the Profit OS / Chimera engine. It defines:

- The **architecture** of the system.
- The roles of **commander agents and execution bots**.
- The **job lifecycle** from data → decision → execution → evidence.
- The daily, weekly, and monthly **operating rhythms**.
- The **ethics and culture** expected from the AI-based core.

---

## 2. Architecture Overview

### 2.1 Core Components

- **Data Layer**
  - Entities: Company, IncomeStream, KPI, Job, EvidenceRecord.
  - Data sources: Shopify, Fiverr, Stripe, Analytics, CRM, etc.

- **Intelligence Layer**
  - KPI evaluation and anomaly detection.
  - Matching patterns to **plays** (from `plays.yml`).
  - Prioritization of plays based on impact and effort.

- **Execution Layer**
  - Job queue with typed jobs (e.g. `INGEST_METRICS`, `EVALUATE_KPIS`, `SUGGEST_PLAYS`, `EXECUTE_PLAY_*`).
  - Agents (commanders + bots) that own specific job types.

- **Evidence & Reporting Layer**
  - EvidenceRecords tying actions to metrics.
  - Dashboards and narrative reports for human review.

---

## 3. Roles & Agents

### 3.1 Commander Agents

Each commander is defined in `configs/agents.yml` with:
- `id`, `label`
- `handles` (job types they can process)
- `role` (responsibility)
- `libraries` (docs, SOPs)
- `values` (decision principles)

**Commerce Commander (`commerce_commander_ai`)**
- Owns: pricing, bundling, revenue tests.
- Handles jobs:
  - `SUGGEST_PLAYS` (commerce-focused)
  - `PLAN_JOB_QUEUE_FOR_PLAY`
  - `EXECUTE_PLAY_COMMERCE`

**Product Commander (`product_commander_ai`)**
- Owns: catalog, product-market fit, upsell/cross-sell.
- Handles:
  - `EXECUTE_PLAY_PRODUCT`

**Growth Commander (`growth_commander_ai`)**
- Owns: acquisition, campaigns, content, zero-ad strategies.
- Handles:
  - `SUGGEST_PLAYS`
  - `PLAN_JOB_QUEUE_FOR_PLAY`
  - `EXECUTE_PLAY_GROWTH`

**Infrastructure Commander (`infra_commander_ai`)**
- Owns: pipelines, deployment, integrations.
- Handles:
  - `INGEST_METRICS`
  - `TRAIN_AGENT`

**Evidence & Finance Commander (`evidence_commander_ai`)**
- Owns: KPI definitions, evaluation, ROI.
- Handles:
  - `EVALUATE_KPIS`
  - `LOG_EVIDENCE`

### 3.2 Execution Bots

Examples:
- `copy_bot` – copywriting, scripts, messaging.
- `shopify_bot` – changes to products, prices, bundles.
- `fiverr_bot` – gigs, packages, FAQs.
- Others as needed: `email_bot`, `ads_bot`, `support_bot`, etc.

---

## 4. Job Lifecycle

1. **Ingest Metrics**
   - Job: `INGEST_METRICS`
   - Owner: `infra_commander_ai`
   - Inputs: exports or API pull from tools.
   - Output: normalized snapshots for KPIs.

2. **Evaluate KPIs**
   - Job: `EVALUATE_KPIS`
   - Owner: `evidence_commander_ai`
   - Inputs: KPI snapshots + `kpis.yml` thresholds.
   - Output: KPI statuses (OK / WARNING / CRITICAL) and notes.

3. **Suggest Plays**
   - Job: `SUGGEST_PLAYS`
   - Owners: `commerce_commander_ai`, `growth_commander_ai`
   - Inputs: KPI statuses + `plays.yml`.
   - Output: set of **triggered plays** ranked by impact and urgency.

4. **Plan Job Queue**
   - Job: `PLAN_JOB_QUEUE_FOR_PLAY`
   - Owners: commanders based on play owner.
   - Inputs: triggered play.
   - Output: **detailed job queue** using `job_plan` in `plays.yml`.

5. **Execute Plays**
   - Jobs: `EXECUTE_PLAY_COMMERCE`, `EXECUTE_PLAY_GROWTH`, `EXECUTE_PLAY_PRODUCT`, etc.
   - Owners: execution bots (e.g. `copy_bot`, `shopify_bot`, `fiverr_bot`).
   - Inputs: step parameters (channel, action, constraints).
   - Output: actual changes implemented or assets created.

6. **Log Evidence**
   - Job: `LOG_EVIDENCE`
   - Owner: `evidence_commander_ai`
   - Inputs: actions performed + metrics after a defined delay.
   - Output: `EvidenceRecord` with correlation_id linking to play and jobs.

7. **Review & Decide Next Cycle**
   - Human + Commanders review evidence, decide:
     - Continue / scale / pause specific plays.
     - Adjust KPIs or thresholds.
     - Add new plays to library.

---

## 5. Configuration Surfaces

### 5.1 `configs/kpis.yml`
- Defines each KPI, its label, target, and thresholds.
- Edited when:
  - New business line launches.
  - Targets or definitions change.

### 5.2 `configs/plays.yml`
- Defines plays, triggers, and job plans.
- Edited when:
  - A new pattern is discovered.
  - A play repeatedly fails or is superseded.

### 5.3 `configs/agents.yml`
- Defines commanders and bots.
- Edited when:
  - New capabilities or tools are added.
  - Responsibilities are reassigned.

**Rule:** All changes must be logged with:
- Reason for change.
- Expected effect.
- Date and owner.

---

## 6. Operating Rhythms

### 6.1 Daily
- Ensure data ingestion jobs completed successfully.
- Check for any **CRITICAL** KPI statuses.
- Validate that no job queue is stuck in `running` for too long.

### 6.2 Weekly
- Run a full cycle:
  - Evaluate KPIs.
  - Trigger and prioritize plays.
  - Approve top 1–3 plays to execute.
- Review last week's EvidenceRecords:
  - What improved?
  - What didn't move?
  - Plays to continue/stop.

### 6.3 Monthly
- Adjust KPI targets based on new baselines.
- Add/remove plays based on performance.
- Capture at least one **case study** summarizing:
  - Problems, plays attempted, results.

---

## 7. Ethics, Culture & Constraints

The AI-based core must operate under explicit principles:

1. **Truth over Narrative**
   - Never hide or distort metrics to make results look better.
   - Always show the real impact of plays, even if negative.

2. **Sustainable Growth**
   - Avoid strategies that damage brand trust or compliance.
   - Optimize for **long-term value**, not just short-term spikes.

3. **Data Minimization**
   - Only ingest data needed for growth decisions.
   - Respect privacy and access scopes defined by the client.

4. **Transparency**
   - Every recommendation and play should be explainable:
     - Why was it triggered?
     - Which metrics support it?

5. **Collaborative Intelligence**
   - The system supports human decision-makers.
   - Humans can override any recommendation.

---

## 8. Failure Modes & Recovery

### 8.1 Data Gaps
**Symptom:** KPIs not updating or weird spikes.
**Action:**
- Run diagnostic on `INGEST_METRICS` jobs.
- Temporarily mark affected KPIs as `unknown` and avoid plays that depend on them.

### 8.2 Job Queue Overload
**Symptom:** Too many jobs, nothing gets done.
**Action:**
- Apply a **priority filter**:
  - Financial impact first, minimal effort wins.
  - Limit active plays per cycle (e.g. max 3 at a time).

### 8.3 Repeatedly Failing Plays
**Symptom:** Same play triggers but never moves the needle.
**Action:**
- Mark play as "under review".
- Analyze EvidenceRecords.
- Either:
  - Adjust the play's trigger conditions.
  - Redesign the play.
  - Retire it.

---

## 9. Versioning & Improvement

- Maintain a simple **changelog** for:
  - `kpis.yml`
  - `plays.yml`
  - `agents.yml`
- Tag versions when:
  - A new major experiment cycle begins.
  - A big architecture change is introduced.

Over time, this becomes a **knowledge base of growth strategies** and an asset in itself.

---

## 10. Onboarding a New Client

Checklist:
1. Create a client-specific config set (copy base configs).
2. Map their business model, channels, and funnels.
3. Fill in KPI targets and thresholds.
4. Tailor or create plays that reflect their reality.
5. Run a first "silent" cycle to test data and logic.
6. Present the first cycle results and recommended plays to the client.
7. Decide and run the first live plays.

This closes the loop between **Profit OS as software** and **Profit OS as a strategic growth partner**.

---

**by AutonomaX / ProPulse – powered by Lazy Larry**

