"""
VeriTrust AI — Enterprise AI Governance & Risk Intelligence Platform
Pixel-Perfect Full-Stack Web Application (Replicating Localhost React Dashboard)
Candidate: Vanshika Aggarwal • Modus Enterprise AI Challenge (Assignment 7)
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
import asyncio
import time

# Ensure backend modules can be imported
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from backend.database.db_manager import (
    init_db, save_use_case, save_full_assessment,
    get_all_use_cases, get_assessment_details, query_knowledge_base,
    delete_use_case
)
from backend.engine.scoring_matrix import compute_deterministic_scores, DIMENSION_METADATA
from backend.engine.research_retriever import retrieve_governance_evidence
from backend.engine.ai_synthesis import synthesize_governance_assessment

# Page Configuration - Hide default sidebar completely
st.set_page_config(
    page_title="VeriTrust AI — Enterprise AI Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "active_view" not in st.session_state:
    st.session_state.active_view = "dashboard"
if "selected_assessment_id" not in st.session_state:
    st.session_state.selected_assessment_id = None
if "eval_animating" not in st.session_state:
    st.session_state.eval_animating = False

# Database Setup & Pre-seeding
@st.cache_resource
def setup_database():
    init_db()
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

# Comprehensive CSS Injection matching exact React UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* 1. COMPLETELY HIDE STREAMLIT SIDEBAR & CHROME */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarCollapsedControl"],
    #MainMenu, 
    footer,
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. Global Dark Background with subtle mesh */
    .stApp {
        background-color: #0a0e17 !important;
        background-image: 
            radial-gradient(ellipse at 15% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
            radial-gradient(ellipse at 85% 100%, rgba(16, 185, 129, 0.08) 0%, transparent 45%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1440px !important;
    }

    /* 3. Sleek Navbar Header */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 14px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-tagline {
        font-size: 0.75rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    /* 4. Top Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #111827 0%, #1e1b4b 60%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 14px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .hero-badge {
        display: inline-block;
        padding: 4px 14px;
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid #38bdf8;
        color: #38bdf8;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .hero-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* 5. Custom Metric Cards */
    .metric-card {
        background: #131c2e;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.9rem;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 4px;
    }
    .metric-footer {
        font-size: 0.75rem;
        color: #10b981;
        font-weight: 600;
    }

    /* 6. Section Titles */
    .sec-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 24px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* 7. Badges */
    .badge-critical {
        background: rgba(244, 63, 94, 0.2);
        color: #fda4af;
        border: 1px solid rgba(244, 63, 94, 0.5);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-high {
        background: rgba(245, 158, 11, 0.2);
        color: #fcd34d;
        border: 1px solid rgba(245, 158, 11, 0.5);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-medium {
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.5);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-low {
        background: rgba(16, 185, 129, 0.2);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.5);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 8. Card Panels */
    .card-panel {
        background: #131c2e;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }

    /* 9. Buttons */
    div.stButton > button {
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
    }

    /* Universal Streamlit Form Inputs */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    textarea {
        background-color: #1a243a !important;
        border-color: rgba(255, 255, 255, 0.16) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TOP NAVBAR WITH NAVIGATION BUTTONS (Matching React UI)
# -------------------------------------------------------------
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2.5, 1.3, 1.5, 1.4])

with nav_col1:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:1.8rem;">🛡️</span>
        <div>
            <div class="brand-title">VeriTrust AI</div>
            <div class="brand-tagline"><span class="status-dot"></span> Deterministic Governance Engine Active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    if st.button("📊 Executive Dashboard", use_container_width=True, type="primary" if st.session_state.active_view == "dashboard" else "secondary"):
        st.session_state.active_view = "dashboard"
        st.rerun()

with nav_col3:
    if st.button("⚡ Dynamic 'Surprise Record' Test", use_container_width=True, type="primary" if st.session_state.active_view == "assess" else "secondary"):
        st.session_state.active_view = "assess"
        st.rerun()

with nav_col4:
    if st.button("📚 6-Tier Knowledge Base", use_container_width=True, type="primary" if st.session_state.active_view == "knowledge" else "secondary"):
        st.session_state.active_view = "knowledge"
        st.rerun()

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
if st.session_state.active_view == "dashboard":
    cases = get_all_use_cases()
    total_cases = len(cases)
    high_critical = sum(1 for c in cases if c.get("risk_level") in ["High Risk", "Critical Risk"])
    avg_score = round(sum(c.get("overall_risk_score", 0.0) for c in cases) / total_cases, 1) if total_cases > 0 else 0.0
    high_ratio = round((high_critical / total_cases * 100), 1) if total_cases > 0 else 0.0

    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-badge">Modus Enterprise AI Build Challenge • Assignment 7</span>
        <div class="hero-title">Enterprise AI Governance & Risk Intelligence Platform</div>
        <div class="hero-desc">
            Deterministic 10-Dimension Risk Scoring Matrix • 6-Tier Legal & Regulatory Citations • Dynamic "Surprise Record" Ingestion
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Key Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Assessed Systems</div>
            <div class="metric-value">{total_cases}</div>
            <div class="metric-footer">● 100% Audited</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High / Critical Risk</div>
            <div class="metric-value" style="color:#f43f5e;">{high_critical} <span style="font-size:1rem; color:#fda4af;">({high_ratio}%)</span></div>
            <div class="metric-footer" style="color:#fda4af;">Strict Regulatory Oversight</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">6-Tier Citations Indexed</div>
            <div class="metric-value" style="color:#10b981;">15 <span style="font-size:1rem; color:#6ee7b7;">Statutes</span></div>
            <div class="metric-footer">Tier 1 Law to Tier 6 Web</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Portfolio Risk Score</div>
            <div class="metric-value" style="color:#fbbf24;">{avg_score} <span style="font-size:1rem; color:#fde047;">/ 100</span></div>
            <div class="metric-footer" style="color:#fde047;">Mathematically Calibrated</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # 2-Column Split: Evaluated Systems Table vs 10 Governance Areas Card
    col_table, col_dimensions = st.columns([1.3, 1])

    with col_table:
        st.markdown('<div class="sec-title">📋 Evaluated AI Systems Registry</div>', unsafe_allow_html=True)
        
        for c in cases:
            risk_badge_class = "badge-critical" if c.get("risk_level") == "Critical Risk" else ("badge-high" if c.get("risk_level") == "High Risk" else "badge-low")
            
            with st.container():
                st.markdown(f"""
                <div class="card-panel" style="padding: 16px 20px; margin-bottom: 12px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <div>
                            <span style="color:#38bdf8; font-weight:700; font-size:1.05rem;">{c['name']}</span>
                            <span style="color:#94a3b8; font-size:0.8rem; margin-left:8px;">({c['industry']})</span>
                        </div>
                        <span class="{risk_badge_class}">{c.get('risk_level', 'Pending')} • {c.get('overall_risk_score', 'N/A')}/100</span>
                    </div>
                    <div style="color:#cbd5e1; font-size:0.85rem; margin-bottom:10px; line-height:1.4;">{c['purpose']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:0.75rem; color:#94a3b8; font-family:'JetBrains Mono';">Autonomy: {c['autonomy_level']} • Impact: {c['impact_tier']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Inspect Button for this use case
                if c.get("assessment_id"):
                    if st.button(f"🔍 Inspect Full 10-Dim Audit & Citations for '{c['name'][:30]}...'", key=f"inspect_{c['id']}"):
                        st.session_state.selected_assessment_id = c["assessment_id"]
                        st.session_state.active_view = "detail"
                        st.rerun()

    with col_dimensions:
        st.markdown('<div class="sec-title">🎯 10 Mandatory Governance Areas</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-panel">
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">1. Data Lineage & Quality</span>
                    <span style="color:#38bdf8;">Weight: 1.0</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#38bdf8; width:75%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">2. Privacy & Data Protection (GDPR Art. 35)</span>
                    <span style="color:#38bdf8;">Weight: 1.2</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#818cf8; width:80%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">3. Bias, Fairness & Equity (Title VII 80% Rule)</span>
                    <span style="color:#f43f5e;">Weight: 1.3</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#f43f5e; width:85%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">4. Human Oversight (EU AI Act Art. 14)</span>
                    <span style="color:#f43f5e;">Weight: 1.4</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#f43f5e; width:90%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">5. Explainability & Transparency (ECOA 12 CFR)</span>
                    <span style="color:#38bdf8;">Weight: 1.1</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#38bdf8; width:80%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">6. Cybersecurity & Model Robustness</span>
                    <span style="color:#38bdf8;">Weight: 1.2</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#818cf8; width:70%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">7. Decision Impact & Harm Severity</span>
                    <span style="color:#f43f5e;">Weight: 1.5</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#f43f5e; width:88%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">8. Regulatory Exposure & Liability</span>
                    <span style="color:#f43f5e;">Weight: 1.4</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#f43f5e; width:92%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">9. Model Reliability & Drift Risk</span>
                    <span style="color:#38bdf8;">Weight: 1.0</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#38bdf8; width:65%; height:6px; border-radius:4px;"></div></div>
            </div>
            <div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                    <span style="font-weight:600; color:#f8fafc;">10. Continuous Monitoring & Auditability</span>
                    <span style="color:#38bdf8;">Weight: 1.0</span>
                </div>
                <div style="background:#1e293b; border-radius:4px; height:6px;"><div style="background:#10b981; width:70%; height:6px; border-radius:4px;"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# VIEW 2: DYNAMIC "SURPRISE RECORD" EVALUATOR
# -------------------------------------------------------------
elif st.session_state.active_view == "assess":
    st.markdown('<div class="sec-title">⚡ Dynamic AI Governance Assessment ("Surprise Record" Ingestion)</div>', unsafe_allow_html=True)
    st.markdown("Input any novel, un-seeded AI use case to evaluate against the 10-dimension risk scoring matrix and retrieve 6-tier legal evidence.")

    # Quick scenario presets
    st.markdown("**Quick-Load Scenario Presets:**")
    p1, p2, p3, p4 = st.columns(4)
    
    preset = {}
    if p1.button("💳 BFSI Algorithmic Credit", use_container_width=True):
        st.session_state.preset_data = {
            "name": "Automated Commercial Line-of-Credit Underwriter",
            "industry": "BFSI / Financial Services",
            "purpose": "Automated machine learning model that analyzes banking cash flows, credit histories, and tax returns to issue commercial loans.",
            "autonomy": "Human-on-the-Loop",
            "data": ["Financial", "PII", "Protected Attributes"],
            "pop": 85000,
            "impact": "High"
        }
    if p2.button("🏥 Diagnostic Radiology AI", use_container_width=True):
        st.session_state.preset_data = {
            "name": "Chest CT Oncology Detection System",
            "industry": "Healthcare & Life Sciences",
            "purpose": "Deep learning convolutional network that detects early-stage pulmonary nodules on chest CT scans and generates radiologist alerts.",
            "autonomy": "Human-in-the-Loop",
            "data": ["Medical", "PII", "Imaging Data"],
            "pop": 120000,
            "impact": "Critical"
        }
    if p3.button("👥 HR Video Screening AI", use_container_width=True):
        st.session_state.preset_data = {
            "name": "Automated Video Micro-Expression Screening",
            "industry": "HR & Employment",
            "purpose": "Computer vision and speech analysis system assessing candidate micro-expressions, speech pacing, and resume compatibility to rank job applicants.",
            "autonomy": "Fully Autonomous",
            "data": ["Biometric", "PII", "Video Audio", "Employment History"],
            "pop": 60000,
            "impact": "High"
        }
    if p4.button("✈️ Predictive Turbine Maintenance", use_container_width=True):
        st.session_state.preset_data = {
            "name": "Commercial Jet Engine Fatigue Forecaster",
            "industry": "Aviation & Aerospace",
            "purpose": "IoT telemetry analytics analyzing turbine blade vibration and temperature sensors during commercial flights to schedule preventative overhauls.",
            "autonomy": "Advisory / Decision Support",
            "data": ["Telemetry Data", "Sensor Logs"],
            "pop": 450000,
            "impact": "Critical"
        }

    preset = st.session_state.get("preset_data", {})

    # Ingestion Form
    with st.form("dynamic_eval_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            in_name = st.text_input("AI System / Application Name", value=preset.get("name", "Biometric Workplace Access & Mood Monitor"))
            in_industry = st.selectbox(
                "Operational Sector / Industry",
                ["BFSI / Financial Services", "Healthcare & Life Sciences", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"],
                index=0 if not preset else (["BFSI / Financial Services", "Healthcare & Life Sciences", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"].index(preset["industry"]) if preset["industry"] in ["BFSI / Financial Services", "Healthcare & Life Sciences", "HR & Employment", "Aviation & Aerospace", "Retail & Commerce", "Public Sector / Government"] else 0)
            )
            in_autonomy = st.selectbox(
                "Autonomy & Human Oversight Level",
                ["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"],
                index=2 if not preset else (["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"].index(preset["autonomy"]) if preset["autonomy"] in ["Advisory / Decision Support", "Human-in-the-Loop", "Human-on-the-Loop", "Fully Autonomous"] else 2)
            )

        with col_b:
            in_data = st.multiselect(
                "Processed Data Classifications",
                ["PII", "Financial", "Medical", "Biometric", "Protected Attributes", "Telemetry Data", "Sensor Logs", "Video Audio", "Employment History"],
                default=preset.get("data", ["Biometric", "PII"])
            )
            in_pop = st.slider("Affected Population Scale", min_value=100, max_value=1000000, value=preset.get("pop", 50000), step=5000)
            in_impact = st.select_slider("Operational Decision Impact Tier", options=["Low", "Medium", "High", "Critical"], value=preset.get("impact", "High"))

        in_purpose = st.text_area(
            "System Purpose & Operational Description",
            value=preset.get("purpose", "Continuous facial recognition and affective micro-expression monitoring in corporate office to track employee focus and automate security access.")
        )

        submit_btn = st.form_submit_button("🚀 Execute Deterministic 10-Dimension Risk & Evidence Assessment", use_container_width=True, type="primary")

    if submit_btn:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Step 1/4: Ingesting AI Architecture & Operational Parameters...")
        progress_bar.progress(25)
        time.sleep(0.3)

        # 1. Save Use Case
        uid = save_use_case(
            name=in_name, industry=in_industry, purpose=in_purpose,
            autonomy_level=in_autonomy, data_types=in_data,
            affected_population=in_pop, impact_tier=in_impact,
            is_preseeded=False
        )

        status_text.text("Step 2/4: Computing Deterministic 10-Dimension Scoring Matrix...")
        progress_bar.progress(50)
        scores = compute_deterministic_scores(
            industry=in_industry, purpose=in_purpose,
            autonomy_level=in_autonomy, data_types=in_data,
            affected_population=in_pop, impact_tier=in_impact
        )
        time.sleep(0.3)

        status_text.text("Step 3/4: Querying 6-Tier Legal & Regulatory Evidence Repository...")
        progress_bar.progress(75)
        sources = asyncio.run(retrieve_governance_evidence(in_name, in_industry, in_purpose))
        time.sleep(0.3)

        status_text.text("Step 4/4: Synthesizing Statutory Obligations & Remediation Controls...")
        progress_bar.progress(95)
        synth = asyncio.run(synthesize_governance_assessment(
            in_name, in_industry, in_purpose, in_autonomy, in_data, scores, sources
        ))
        
        aid = save_full_assessment(
            use_case_id=uid,
            overall_score=scores["overall_risk_score"],
            risk_level=scores["risk_level"],
            eu_ai_act=scores["eu_ai_act_category"],
            summary=synth["executive_summary"],
            dimensions=synth["dimension_assessments"],
            sources=sources
        )
        progress_bar.progress(100)
        status_text.text("✅ Assessment Complete! Opening Full Audit Dossier...")
        time.sleep(0.4)

        st.session_state.selected_assessment_id = aid
        st.session_state.active_view = "detail"
        st.rerun()

# -------------------------------------------------------------
# VIEW 3: 10-DIMENSION AUDIT DOSSIER (DETAILED AUDIT VIEW)
# -------------------------------------------------------------
elif st.session_state.active_view == "detail":
    aid = st.session_state.selected_assessment_id
    if not aid:
        cases = get_all_use_cases()
        if cases and cases[0].get("assessment_id"):
            aid = cases[0]["assessment_id"]

    details = get_assessment_details(aid) if aid else None

    if details:
        # Header Back Bar
        b_col1, b_col2 = st.columns([1, 4])
        with b_col1:
            if st.button("← Back to Dashboard"):
                st.session_state.active_view = "dashboard"
                st.rerun()

        # Title and badges
        risk_class = "badge-critical" if details["risk_level"] == "Critical Risk" else ("badge-high" if details["risk_level"] == "High Risk" else "badge-low")
        st.markdown(f"""
        <div class="card-panel" style="margin-top: 10px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <span class="hero-badge">{details['industry']}</span>
                    <h2 style="font-family:'Outfit'; font-size:1.9rem; margin: 4px 0;">{details['use_case_name']}</h2>
                    <div style="color:#94a3b8; font-size:0.85rem; font-family:'JetBrains Mono';">
                        Autonomy: {details['autonomy_level']} • Affected Scale: {details['affected_population']:,} • Impact: {details['impact_tier']}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="{risk_class}" style="font-size:1.1rem; padding:6px 16px; margin-bottom:6px;">
                        {details['risk_level']} • {details['overall_risk_score']}/100
                    </div>
                    <div style="color:#38bdf8; font-size:0.8rem; font-weight:600;">{details['eu_ai_act_category']}</div>
                </div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.08); margin: 16px 0;" />
            <div style="color:#e2e8f0; font-size:0.95rem; line-height:1.6; background:rgba(0,0,0,0.25); padding:16px; border-radius:8px; border-left:4px solid #38bdf8;">
                <strong>Executive Summary:</strong> {details['executive_summary']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 10 Dimensions Detailed Cards Grid
        st.markdown('<div class="sec-title">🛡️ Detailed 10-Dimension Risk Breakdown & Mitigating Controls</div>', unsafe_allow_html=True)
        
        dim_cols = st.columns(2)
        for idx, dim in enumerate(details["dimensions"]):
            col = dim_cols[idx % 2]
            d_class = "badge-critical" if dim["risk_score"] >= 85 else ("badge-high" if dim["risk_score"] >= 70 else "badge-low")
            
            with col:
                st.markdown(f"""
                <div class="card-panel" style="min-height: 280px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h4 style="color:#38bdf8; font-size:1.05rem; margin:0;">{dim['dimension_name']}</h4>
                        <span class="{d_class}">{dim['risk_score']}/100</span>
                    </div>
                    <div style="color:#cbd5e1; font-size:0.85rem; margin-bottom:10px;">
                        <strong>Audit Finding:</strong> {dim['findings']}
                    </div>
                    <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:12px;">
                        <strong>Regulatory Liability:</strong> <span style="color:#fcd34d;">{dim['regulatory_impact']}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#a7f3d0;">
                        <strong>Remediation Controls:</strong>
                        <ul style="margin-top:4px; padding-left:18px; margin-bottom:0;">
                            {''.join(f"<li>{c}</li>" for c in dim['mitigating_controls'])}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 6-Tier Legal & Regulatory Citations
        st.markdown('<div class="sec-title">📜 6-Tier Regulatory & Legal Evidence Drawer</div>', unsafe_allow_html=True)
        for src in details["sources"]:
            st.markdown(f"""
            <div class="card-panel" style="padding:16px 20px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="hero-badge">[{src['source_tier']}] {src['author_entity']} • {src.get('jurisdiction', 'Global')}</span>
                    <span style="font-size:0.75rem; color:#94a3b8;">Reliability Score: {src.get('reliability_score', 0.9)}</span>
                </div>
                <h4 style="color:#f8fafc; font-size:1rem; margin: 6px 0;">{src['title']}</h4>
                <div style="color:#cbd5e1; font-size:0.85rem; line-height:1.4;">{src['citation_text']}</div>
                {f'<div style="margin-top:8px;"><a href="{src["url"]}" target="_blank" style="color:#38bdf8; font-size:0.8rem; text-decoration:none;">🔗 Access Official Statutory Portal &rarr;</a></div>' if src.get('url') else ''}
            </div>
            """, unsafe_allow_html=True)

        # Export Dossier Button
        st.markdown("---")
        json_payload = json.dumps(details, indent=2)
        st.download_button(
            label="📥 Export Full Audit Report (JSON Payload)",
            data=json_payload,
            file_name=f"veritrust_audit_{details['use_case_name'].replace(' ', '_').lower()}.json",
            mime="application/json",
            type="primary"
        )
    else:
        st.warning("No assessment selected. Please return to the dashboard.")

# -------------------------------------------------------------
# VIEW 4: 6-TIER KNOWLEDGE BASE EXPLORER
# -------------------------------------------------------------
elif st.session_state.active_view == "knowledge":
    st.markdown('<div class="sec-title">📚 6-Tier Regulatory & Legal Knowledge Repository</div>', unsafe_allow_html=True)
    st.markdown("Explore pre-seeded statutory texts, regulatory guidance, and international consensus standards.")

    k_col1, k_col2 = st.columns([2, 1])
    with k_col1:
        search_query = st.text_input("🔍 Search Knowledge Base (e.g., 'EU AI Act', 'NIST', 'Bias', 'GDPR', 'ECOA')", "")
    with k_col2:
        tier_select = st.selectbox(
            "Filter by Source Tier:",
            ["All Tiers", "Law / Regulation", "Regulatory Guidance", "Industry Standard", "Research", "Vendor Information", "General Web Content"]
        )

    filt_tier = None if tier_select == "All Tiers" else tier_select
    kb_records = query_knowledge_base(search_query, filt_tier)

    st.markdown(f"**Indexed Reference Documents ({len(kb_records)} Found):**")
    for rec in kb_records:
        st.markdown(f"""
        <div class="card-panel" style="margin-bottom: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="hero-badge">[{rec['source_tier']}] {rec['author_entity']} • {rec['jurisdiction']} ({rec['pub_date']})</span>
            </div>
            <h3 style="font-family:'Outfit'; color:#f8fafc; font-size:1.15rem; margin: 6px 0;">{rec['title']}</h3>
            <p style="color:#cbd5e1; font-size:0.9rem; line-height:1.5;">{rec['summary_content']}</p>
            {f'<a href="{rec["url"]}" target="_blank" style="color:#38bdf8; font-size:0.85rem; font-weight:600; text-decoration:none;">🔗 Access Official Statutory Portal &rarr;</a>' if rec.get('url') else ''}
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# FOOTER (Clean & Executive)
# -------------------------------------------------------------
st.markdown("""
<div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding: 20px 0; margin-top: 50px; display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.8rem;">
    <div>VeriTrust AI — Enterprise AI Governance & Risk Assessment Platform (Assignment 7)</div>
    <div>100% Free & Open-Source • Zero Paid API Dependencies • Modus Challenge</div>
</div>
""", unsafe_allow_html=True)
