"""Streamlit dashboard for Profit OS Chimera."""

import streamlit as st
import requests
from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Profit OS Chimera",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Profit OS Chimera - Growth Command Center")
st.markdown("AI-Powered Growth Operating System")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Companies", "KPIs", "Plays", "Jobs", "Evidence", "Run Cycle"]
)

# API Helper
def api_get(endpoint: str):
    """Make GET request to API."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def api_post(endpoint: str, data: dict):
    """Make POST request to API."""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


# Dashboard Page
if page == "Dashboard":
    st.header("Overview Dashboard")
    
    # Health check
    health = api_get("/api/health")
    if health:
        st.success(f"✅ API Status: {health.get('status', 'unknown')}")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    companies = api_get("/api/v1/companies/")
    if companies:
        col1.metric("Companies", len(companies))
    
    # Recent activity
    st.subheader("Recent Activity")
    st.info("Dashboard view - connect to real data for live metrics")


# Companies Page
elif page == "Companies":
    st.header("Companies")
    
    # Create new company
    with st.expander("Create New Company"):
        with st.form("create_company"):
            name = st.text_input("Company Name")
            industry = st.text_input("Industry")
            size = st.selectbox("Size", ["solo", "smb", "mid", "enterprise"])
            
            if st.form_submit_button("Create Company"):
                result = api_post("/api/v1/companies/", {
                    "name": name,
                    "industry": industry,
                    "size": size
                })
                if result:
                    st.success(f"Company created: {result.get('id')}")
                    st.rerun()
    
    # List companies
    companies = api_get("/api/v1/companies/")
    if companies:
        df = pd.DataFrame(companies)
        st.dataframe(df, use_container_width=True)


# KPIs Page
elif page == "KPIs":
    st.header("Key Performance Indicators")
    
    companies = api_get("/api/v1/companies/")
    if companies:
        company_id = st.selectbox("Select Company", [c["id"] for c in companies])
        
        if company_id:
            kpis = api_get(f"/api/v1/kpis/company/{company_id}/latest")
            if kpis:
                st.subheader("Latest KPI Snapshot")
                
                # Create metrics display
                cols = st.columns(3)
                for i, kpi in enumerate(kpis[:9]):
                    with cols[i % 3]:
                        status_emoji = {"ok": "✅", "warning": "⚠️", "critical": "🔴", "unknown": "❓"}
                        st.metric(
                            kpi["name"],
                            f"{kpi['value']:.2f}",
                            delta=f"Target: {kpi.get('target', 'N/A')}"
                        )
                        st.caption(f"Status: {status_emoji.get(kpi['status'], '❓')} {kpi['status']}")


# Plays Page
elif page == "Plays":
    st.header("Growth Plays")
    
    plays = api_get("/api/v1/plays/")
    if plays:
        st.subheader(f"Available Plays ({len(plays)})")
        
        for play in plays:
            with st.expander(f"{play.get('name', 'Unknown')} - {play.get('intent', '')}"):
                st.write(f"**ID:** {play.get('id')}")
                st.write(f"**Owner:** {play.get('owner_agent')}")
                st.write(f"**Impact:** {play.get('impact_hypothesis', 'N/A')}")


# Jobs Page
elif page == "Jobs":
    st.header("Job Queue")
    
    companies = api_get("/api/v1/companies/")
    if companies:
        company_id = st.selectbox("Select Company", [c["id"] for c in companies], key="jobs_company")
        
        if company_id:
            jobs = api_get(f"/api/v1/jobs/company/{company_id}")
            if jobs:
                df = pd.DataFrame(jobs)
                st.dataframe(df, use_container_width=True)


# Evidence Page
elif page == "Evidence":
    st.header("Evidence Records")
    
    companies = api_get("/api/v1/companies/")
    if companies:
        company_id = st.selectbox("Select Company", [c["id"] for c in companies], key="evidence_company")
        
        if company_id:
            evidence = api_get(f"/api/v1/evidence/company/{company_id}")
            if evidence:
                st.subheader(f"Evidence Records ({len(evidence)})")
                for ev in evidence[:20]:  # Show last 20
                    with st.expander(f"{ev['event_type']} - {ev['occurred_at']}"):
                        st.json(ev['payload'])


# Run Cycle Page
elif page == "Run Cycle":
    st.header("Run Growth Cycle")
    
    companies = api_get("/api/v1/companies/")
    if companies:
        company_id = st.selectbox("Select Company", [c["id"] for c in companies], key="cycle_company")
        
        if company_id:
            st.subheader("KPI Snapshot")
            st.info("Enter current KPI values to trigger growth plays")
            
            # Get KPI definitions
            kpi_defs = {}  # Would load from config
            
            kpi_snapshot = {}
            col1, col2 = st.columns(2)
            
            with col1:
                kpi_snapshot["revenue_total_30d"] = st.number_input("Revenue (30d)", value=5000.0)
                kpi_snapshot["cr_main_funnel"] = st.number_input("Conversion Rate", value=0.05, format="%.3f")
                kpi_snapshot["sessions_main_30d"] = st.number_input("Sessions (30d)", value=500)
                kpi_snapshot["cac_paid"] = st.number_input("CAC (Paid)", value=30.0)
            
            with col2:
                kpi_snapshot["retention_60d"] = st.number_input("Retention (60d)", value=0.35, format="%.2f")
                kpi_snapshot["fiverr_orders_30d"] = st.number_input("Fiverr Orders (30d)", value=0)
                kpi_snapshot["shopify_orders_30d"] = st.number_input("Shopify Orders (30d)", value=0)
            
            if st.button("Run Growth Cycle", type="primary"):
                with st.spinner("Running cycle..."):
                    result = api_post("/api/v1/cycles/run", {
                        "company_id": company_id,
                        "kpi_snapshot": kpi_snapshot
                    })
                    
                    if result:
                        st.success("Cycle completed!")
                        st.json(result)



