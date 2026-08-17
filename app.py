"""
VeriTrust AI — Enterprise AI Governance & Risk Intelligence Platform
Streamlit Web Application for Instant 1-Click Live Deployment (Modus Challenge Assignment 7)
Candidate: Vanshika Aggarwal
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
import asyncio
from datetime import datetime

# Add root and backend to python path for seamless imports
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

# Import Core Governance Engine
from backend.database.db_manager import (
    init_db, save_use_case, save_full_assessment,
    get_all_use_cases, get_assessment_details, query_knowledge_base,
    delete_use_case
)
from backend.engine.scoring_matrix import compute_deterministic_scores, DIMENSION_METADATA
from backend.engine.research_retriever import retrieve_governance_evidence
from backend.engine.ai_synthesis import synthesize_governance_assessment

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="VeriTrust AI — Enterprise AI Governance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Executive Theme CSS
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Top Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .header-sub {
        color: #94a3b8;
        font-size: 0.95rem;
    }
    .badge-modus {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid #38bdf8;
        color: #38bdf8;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #131d31 !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }

    /* Custom Risk Badges */
    .risk-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        text-align: center;
    }
    .risk-critical { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; }
    .risk-high { background: rgba(249, 115, 22, 0.2); border: 1px solid #f97316; color: #fb923c; }
    .risk-medium { background: rgba(234, 179, 8, 0.2); border: 1px solid #eab308; color: #fde047; }
    .risk-low { background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; }

    /* Custom Cards */
    .gov-card {
        background: #131d31;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .gov-card h4 {
        color: #38bdf8;
        margin-bottom: 8px;
    }
    .gov-card p {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0f172a;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 6px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #04121d !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Database and Pre-seeded Records
@st.cache_resource
def setup_database():
    init_db()
    # Check if empty, seed default cases
    existing = get_all_use_cases()
    if not existing:
        preseeded = [
            {
                "name": "Algorithmic Credit Underwriting & Risk Scoring",
                "industry": "BFSI / Financial Services",
                "purpose": "Automated ML model that evaluates creditworthiness and determines credit card limits and loan interest rates for individual banking customers.",
                "autonomy_level": "Human-on-the-Loop",
                "data_types": ["PII", "Financial", "Credit History", "Protected Attributes"],
                "affected_population": 250000,
                "impact_tier": "High"
            },
            {
                "name": "Automated Video Interview & Resume Screening AI",
                "industry": "HR & Employment",
                "purpose": "Computer vision and NLP pipeline that screens candidate resumes and evaluates facial micro-expressions during video interviews to score job applicant suitability.",
                "autonomy_level": "Fully Autonomous",
                "data_types": ["PII", "Biometric", "Video Audio", "Employment History"],
                "affected_population": 75000,
                "impact_tier": "High"
            },
            {
                "name": "Diagnostic Radiography Assistance AI",
                "industry": "Healthcare & Life Sciences",
                "purpose": "Deep learning diagnostic tool that scans chest X-rays and mammograms to highlight potential malignant nodules for radiologists.",
                "autonomy_level": "Human-in-the-Loop",
                "data_types": ["Medical", "PII", "Imaging Data"],
                "affected_population": 150000,
                "impact_tier": "Critical"
            },
            {
                "name": "Predictive Jet Engine Maintenance AI",
                "industry": "Aviation & Aerospace",
                "purpose": "IoT sensor telemetry analyzer predicting turbine blade fatigue and scheduling preventative aircraft engine maintenance.",
                "autonomy_level": "Advisory / Decision Support",
                "data_types": ["Telemetry Data", "Sensor Logs"],
                "affected_population": 500000,
                "impact_tier": "Critical"
            }
        ]
        for uc in preseeded:
            uid = save_use_case(
                name=uc["name"], industry=uc["industry"], purpose=uc["purpose"],
                autonomy_level=uc["autonomy_level"], data_types=uc["data_types"],
                affected_population=uc["affected_population"], impact_tier=uc["impact_tier"],
                is_preseeded=True
            )
            scores = compute_deterministic_scores(
                industry=uc["industry"], purpose=uc["purpose"],
                autonomy_level=uc["autonomy_level"], data_types=uc["data_types"],
                affected_population=uc["affected_population"], impact_tier=uc["impact_tier"]
            )
            sources = asyncio.run(retrieve_governance_evidence(uc["name"], uc["industry"], uc["purpose"]))
            synth = asyncio.run(synthesize_governance_assessment(
                uc["name"], uc["industry"], uc["purpose"], uc["autonomy_level"],
                uc["data_types"], scores, sources
            ))
            save_full_assessment(
                use_case_id=uid,
                overall_score=scores["overall_risk_score"],
                risk_level=scores["risk_level"],
                eu_ai_act=scores["eu_ai_act_category"],
                summary=synth["executive_summary"],
                dimensions=synth["dimension_assessments"],
                sources=sources
            )

setup_database()

# Header Banner
st.markdown("""
<div class="header-banner">
    <span class="badge-modus">Modus Enterprise AI Build Challenge • Assignment 7</span>
    <div class="header-title">VeriTrust AI — Enterprise AI Governance & Risk Intelligence</div>
    <div class="header-sub">
        Deterministic 10-Dimension Risk Scoring Matrix • 6-Tier Legal & Regulatory Citations • Dynamic "Surprise Record" Ingestion
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Info & Candidate Profile
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.markdown("### 🛡️ Governance Platform")
    st.markdown("**Candidate:** Vanshika Aggarwal")
    st.markdown("**Assignment:** Assignment 7 (AI Governance)")
    st.markdown("**Target Domains:** BFSI, Healthcare, HR, Aviation")
    st.markdown("---")
    
    st.markdown("### 🔗 Official Submission Links")
    st.markdown("- [GitHub Repository](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance)")
    st.markdown("- [Architecture Diagram](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/ARCHITECTURE_DIAGRAM.md)")
    st.markdown("- [Technical Documentation](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/TECHNICAL_DOCUMENTATION.md)")
    st.markdown("- [Database Data Model](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/DATABASE_DATA_MODEL.md)")
    st.markdown("---")
    st.caption("100% Free & Open-Source Software • Zero Paid API Dependencies")

# Main Navigation Tabs
tab_dash, tab_eval, tab_audit, tab_kb, tab_arch = st.tabs([
    "📊 Executive Dashboard",
    "⚡ Dynamic 'Surprise Record' Test",
    "🔍 10-Dimension Audit Breakdown",
    "📚 6-Tier Regulatory Knowledge Base",
    "🏛️ System Architecture & Schema"
])

# -------------------------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
with tab_dash:
    cases = get_all_use_cases()
    total_cases = len(cases)
    high_critical = sum(1 for c in cases if c.get("risk_level") in ["High Risk", "Critical Risk"])
    avg_score = round(sum(c.get("overall_risk_score", 0.0) for c in cases) / total_cases, 1) if total_cases > 0 else 0.0

    # Top KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Assessed Systems", total_cases, "+100% Audited")
    with col2:
        st.metric("High / Critical Risk", f"{high_critical} ({round(high_critical/total_cases*100, 1)}%)", "Strict Oversight")
    with col3:
        st.metric("6-Tier Citations Indexed", "15 Canonical", "Tier 1 - Tier 6")
    with col4:
        st.metric("Avg Portfolio Risk Score", f"{avg_score} / 100", "Calibrated")

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("### 📋 Evaluated AI Systems Registry")
        if cases:
            table_data = []
            for c in cases:
                table_data.append({
                    "ID": c["id"],
                    "AI System Name": c["name"],
                    "Industry": c["industry"],
                    "Autonomy Level": c["autonomy_level"],
                    "Risk Score": f"{c.get('overall_risk_score', 'N/A')}/100",
                    "Risk Tier": c.get("risk_level", "Pending"),
                    "EU AI Act Category": c.get("eu_ai_act_category", "N/A")
                })
            df_cases = pd.DataFrame(table_data)
            st.dataframe(df_cases, use_container_width=True, hide_index=True)
        else:
            st.info("No AI systems in registry. Submit a use case in the Evaluator tab.")

    with col_right:
        st.markdown("### 🎯 10-Dimension Risk Framework Areas")
        st.markdown("""
        1. **Data Lineage & Quality** (Weight: 1.0)
        2. **Privacy & Data Protection** (Weight: 1.2 • GDPR Art. 35)
        3. **Bias, Fairness & Equity** (Weight: 1.3 • Title VII 80% Rule)
        4. **Human Oversight** (Weight: 1.4 • EU AI Act Art. 14)
        5. **Explainability & Transparency** (Weight: 1.1 • ECOA Adverse Action)
        6. **Cybersecurity & Model Robustness** (Weight: 1.2 • SOC 2 CC6.1)
        7. **Decision Impact & Severity** (Weight: 1.5 • Safety Critical)
        8. **Regulatory Exposure** (Weight: 1.4 • Global Compliance)
        9. **Model Reliability & Drift** (Weight: 1.0 • Grounding)
        10. **Continuous Monitoring** (Weight: 1.0 • SIEM / Telemetry)
        """)

# -------------------------------------------------------------
# TAB 2: DYNAMIC "SURPRISE RECORD" EVALUATOR
# -------------------------------------------------------------
with tab_eval:
    st.markdown("### ⚡ Live Dynamic AI System Evaluation ('Surprise Record' Test)")
    st.markdown("Input any novel AI use case to compute immediate, deterministic 10-dimension risk scores, statutory citations, and mitigation controls.")

    # Preset selector buttons
    st.markdown("**Quick-Load Scenario Presets:**")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    
    selected_preset = None
    if p_col1.button("💳 BFSI Credit Underwriting"):
        selected_preset = {
            "name": "Automated SME Credit Line AI",
            "industry": "BFSI / Financial Services",
            "purpose": "Evaluates small business banking data and ledger transactions to approve line-of-credit limits automatically.",
            "autonomy": "Human-on-the-Loop",
            "data": ["Financial", "PII", "Protected Attributes"],
            "pop": 85000,
            "impact": "High"
        }
    if p_col2.button("🏥 Diagnostic Ultrasound AI"):
        selected_preset = {
            "name": "Cardiac Ultrasound Analysis AI",
            "industry": "Healthcare & Life Sciences",
            "purpose": "Computer vision model analyzing live echocardiograms to flag left ventricular ejection fraction anomalies.",
            "autonomy": "Human-in-the-Loop",
            "data": ["Medical", "PII", "Imaging Data"],
            "pop": 120000,
            "impact": "Critical"
        }
    if p_col3.button("👥 HR Sentiment & Video Screen"):
        selected_preset = {
            "name": "Candidate Video Micro-Expression Rater",
            "industry": "HR & Employment",
            "purpose": "NLP and facial analysis scoring applicant emotional stability during remote interview recordings.",
            "autonomy": "Fully Autonomous",
            "data": ["Biometric", "PII", "Video Audio"],
            "pop": 45000,
            "impact": "High"
        }
    if p_col4.button("✈️ Drone Flight Navigation AI"):
        selected_preset = {
            "name": "Autonomous Logistics Delivery UAV",
            "industry": "Aviation & Aerospace",
            "purpose": "Vision-based collision avoidance and autonomous path planning for commercial urban delivery drones.",
            "autonomy": "Fully Autonomous",
            "data": ["Telemetry Data", "Sensor Logs", "Video Audio"],
            "pop": 350000,
            "impact": "Critical"
        }

    # Evaluation Form
    with st.form("surprise_eval_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_name = st.text_input("AI System Name", value=selected_preset["name"] if selected_preset else "Predictive Patient Readmission AI")
            f_industry = st.selectbox(
                "Industry / Operational Sector",
                ["Healthcare & Life Sciences", "BFSI / Financial Services", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"],
                index=0 if not selected_preset else (["Healthcare & Life Sciences", "BFSI / Financial Services", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"].index(selected_preset["industry"]) if selected_preset["industry"] in ["Healthcare & Life Sciences", "BFSI / Financial Services", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"] else 0)
            )
            f_autonomy = st.selectbox(
                "Autonomy & Human Oversight Level",
                ["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"],
                index=2 if not selected_preset else (["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"].index(selected_preset["autonomy"]) if selected_preset["autonomy"] in ["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"] else 2)
            )

        with col_f2:
            f_data = st.multiselect(
                "Processed Data Classifications",
                ["PII", "Financial", "Medical", "Biometric", "Protected Attributes", "Telemetry Data", "Sensor Logs", "Video Audio", "Employment History"],
                default=selected_preset["data"] if selected_preset else ["Medical", "PII"]
            )
            f_pop = st.slider("Estimated Affected Population Scale", min_value=100, max_value=1000000, value=selected_preset["pop"] if selected_preset else 50000, step=5000)
            f_impact = st.select_slider("Operational Decision Impact Tier", options=["Low", "Medium", "High", "Critical"], value=selected_preset["impact"] if selected_preset else "High")

        f_purpose = st.text_area(
            "System Purpose & Functional Description",
            value=selected_preset["purpose"] if selected_preset else "Automated EHR analysis identifying hospitalized patients at high risk of 30-day readmission to trigger preemptive nursing interventions."
        )

        submit_btn = st.form_submit_button("🚀 Execute Deterministic 10-Dimension Risk & Evidence Assessment", use_container_width=True)

    if submit_btn:
        with st.spinner("Processing 10-Dimension Scoring Matrix & 6-Tier Evidence Retrieval..."):
            # 1. Save Use Case
            uid = save_use_case(
                name=f_name, industry=f_industry, purpose=f_purpose,
                autonomy_level=f_autonomy, data_types=f_data,
                affected_population=f_pop, impact_tier=f_impact,
                is_preseeded=False
            )
            # 2. Compute Deterministic Scores
            scores = compute_deterministic_scores(
                industry=f_industry, purpose=f_purpose,
                autonomy_level=f_autonomy, data_types=f_data,
                affected_population=f_pop, impact_tier=f_impact
            )
            # 3. Retrieve Evidence
            sources = asyncio.run(retrieve_governance_evidence(f_name, f_industry, f_purpose))
            # 4. Synthesize Findings
            synth = asyncio.run(synthesize_governance_assessment(
                f_name, f_industry, f_purpose, f_autonomy, f_data, scores, sources
            ))
            # 5. Persist
            aid = save_full_assessment(
                use_case_id=uid,
                overall_score=scores["overall_risk_score"],
                risk_level=scores["risk_level"],
                eu_ai_act=scores["eu_ai_act_category"],
                summary=synth["executive_summary"],
                dimensions=synth["dimension_assessments"],
                sources=sources
            )

            st.success(f"✅ Evaluation Complete! Record Persisted (Assessment ID #{aid})")

            # Display Results Banner
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                st.metric("Overall Governance Risk Score", f"{scores['overall_risk_score']}/100")
            with r_col2:
                st.metric("Assessed Risk Tier", scores["risk_level"])
            with r_col3:
                st.metric("EU AI Act Classification", scores["eu_ai_act_category"])

            st.info(f"**Executive Synthesis:** {synth['executive_summary']}")

            # Dimension Breakdown
            st.markdown("#### 📊 10-Dimension Risk Breakdown")
            dim_cols = st.columns(2)
            for idx, (k, d) in enumerate(scores["dimensions"].items()):
                c = dim_cols[idx % 2]
                with c:
                    st.markdown(f"**{d['dimension_name']}** ({d['risk_score']}/100 — *{d['risk_level']} Risk*)")
                    st.progress(d["risk_score"] / 100.0)

# -------------------------------------------------------------
# TAB 3: 10-DIMENSION AUDIT BREAKDOWN
# -------------------------------------------------------------
with tab_audit:
    st.markdown("### 🔍 Granular 10-Dimension Governance & Compliance Dossier")
    cases = get_all_use_cases()
    if cases:
        case_options = {f"{c['name']} (#{c['id']})": c['assessment_id'] for c in cases if c.get('assessment_id')}
        selected_case_name = st.selectbox("Select Assessed AI System to Inspect:", list(case_options.keys()))
        
        if selected_case_name:
            aid = case_options[selected_case_name]
            details = get_assessment_details(aid)

            if details:
                st.markdown(f"### Assessment Dossier: **{details['use_case_name']}**")
                st.markdown(f"**Industry:** {details['industry']} | **Autonomy:** {details['autonomy_level']} | **Affected Population:** {details['affected_population']:,}")
                st.markdown(f"**Overall Score:** `{details['overall_risk_score']}/100` | **Risk Tier:** `{details['risk_level']}` | **EU AI Act:** `{details['eu_ai_act_category']}`")
                st.markdown(f"> *{details['executive_summary']}*")
                st.markdown("---")

                # Show 10 Dimensions Accordion
                st.markdown("#### 🛡️ Detailed Dimension Findings & Mitigating Engineering Controls")
                for dim in details["dimensions"]:
                    with st.expander(f"📌 {dim['dimension_name']} — Score: {dim['risk_score']}/100 ({dim['risk_level']})"):
                        st.markdown(f"**Statutory Audit Findings:** {dim['findings']}")
                        st.markdown(f"**Regulatory Impact & Liability:** `{dim['regulatory_impact']}`")
                        st.markdown("**Mandatory Mitigating Controls:**")
                        for ctrl in dim["mitigating_controls"]:
                            st.markdown(f"- ✅ {ctrl}")

                # Show Cited Evidence
                st.markdown("#### 📜 Cited 6-Tier Regulatory & Legal Sources")
                for src in details["sources"]:
                    st.markdown(f"""
                    <div class="gov-card">
                        <span class="badge-modus">[{src['source_tier']}] {src['author_entity']} ({src.get('jurisdiction', 'Global')})</span>
                        <h4>{src['title']}</h4>
                        <p>{src['citation_text']}</p>
                        {f'<a href="{src["url"]}" target="_blank" style="color:#38bdf8; font-size:0.85rem;">🔗 Access Statutory Reference</a>' if src.get('url') else ''}
                    </div>
                    """, unsafe_allow_html=True)

                # Export Report JSON
                st.markdown("---")
                json_str = json.dumps(details, indent=2)
                st.download_button(
                    label="📥 Export Full Compliance Audit Dossier (JSON)",
                    data=json_str,
                    file_name=f"audit_report_{details['use_case_name'].replace(' ', '_').lower()}.json",
                    mime="application/json"
                )

# -------------------------------------------------------------
# TAB 4: 6-TIER REGULATORY KNOWLEDGE BASE
# -------------------------------------------------------------
with tab_kb:
    st.markdown("### 📚 6-Tier Regulatory & Legal Knowledge Repository")
    st.markdown("Search verified statutory articles, regulatory enforcement guidance, and international consensus standards.")

    kb_search = st.text_input("🔍 Search Knowledge Base by Statute, Topic, or Authority (e.g., 'EU AI Act', 'NIST', 'Bias', 'GDPR')", "")
    tier_filter = st.selectbox("Filter by Source Tier:", ["All Tiers", "Law / Regulation", "Regulatory Guidance", "Industry Standard", "Research", "Vendor Information", "General Web Content"])
    
    selected_tier = None if tier_filter == "All Tiers" else tier_filter
    kb_results = query_knowledge_base(kb_search, selected_tier)

    st.markdown(f"**Showing {len(kb_results)} Verified References:**")
    for item in kb_results:
        st.markdown(f"""
        <div class="gov-card">
            <span class="badge-modus">[{item['source_tier']}] {item['author_entity']} • {item['jurisdiction']} ({item['pub_date']})</span>
            <h4>{item['title']}</h4>
            <p>{item['summary_content']}</p>
            {f'<a href="{item["url"]}" target="_blank" style="color:#38bdf8; font-size:0.85rem;">🔗 Official Authority Document</a>' if item.get('url') else ''}
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 5: SYSTEM ARCHITECTURE & DATA MODEL
# -------------------------------------------------------------
with tab_arch:
    st.markdown("### 🏛️ System Architecture & Normalized Data Model")
    
    st.markdown("#### 1. 5-Layer Enterprise Architecture")
    st.markdown("""
    - **Layer 1 (UI / Presentation)**: React 18 / Streamlit Executive Interface with real-time gauges.
    - **Layer 2 (API Gateway)**: FastAPI async endpoints (`/api/assess`, `/api/use-cases`, `/api/sources`).
    - **Layer 3 (Deterministic AI Intelligence)**: Weighted 10-dimension risk scoring matrix + 6-tier reliability weighting.
    - **Layer 4 (Persistence Layer)**: SQLite3 ACID relational database (`governance_app.db`) with 5 normalized tables.
    - **Layer 5 (External Research Layer)**: 6-Tier statutory legal citation engine.
    """)

    st.markdown("#### 2. Relational Database Schema (3NF Normalized)")
    st.code("""
    USE_CASES (id, name, industry, purpose, autonomy_level, data_types, affected_population, impact_tier)
      └── ASSESSMENTS (id, use_case_id, overall_risk_score, risk_level, eu_ai_act_category, executive_summary)
            ├── DIMENSION_ASSESSMENTS (id, assessment_id, dimension_key, risk_score, findings, controls) [1:10]
            └── EVIDENCE_SOURCES (id, assessment_id, source_tier, title, author_entity, citation_text, url)
    KNOWLEDGE_BASE (id, source_tier, title, author_entity, jurisdiction, summary_content, key_rules)
    """, language="sql")

    st.markdown("#### 3. Free & Open Source License Verification")
    st.markdown("- **Python 3.10+** (PSFL) • **FastAPI** (MIT) • **Streamlit** (Apache 2.0) • **SQLite3** (Public Domain) • **React** (MIT)")
