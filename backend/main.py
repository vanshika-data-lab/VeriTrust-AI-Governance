"""
FastAPI Server for AegisAI Enterprise Governance Application
"""

import os
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database.db_manager import (
    init_db, save_use_case, save_full_assessment,
    get_all_use_cases, get_assessment_details, query_knowledge_base
)
from engine.scoring_matrix import compute_deterministic_scores
from engine.evidence_classifier import enrich_source_metadata
from engine.research_retriever import retrieve_governance_evidence
from engine.ai_synthesis import synthesize_governance_assessment

app = FastAPI(
    title="AegisAI Governance & Risk Intelligence API",
    description="Enterprise AI Governance Research & Assessment Application",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UseCaseInput(BaseModel):
    name: str = Field(..., example="Algorithmic Credit Underwriting AI")
    industry: str = Field(..., example="BFSI / Financial Services")
    purpose: str = Field(..., example="Automates credit line allocation and loan interest rates using customer transactional data.")
    autonomy_level: str = Field("Human-on-the-Loop", example="Human-on-the-Loop")
    data_types: List[str] = Field(default=["PII", "Financial"], example=["PII", "Financial", "Credit Score"])
    affected_population: int = Field(50000, example=50000)
    impact_tier: str = Field("High", example="High")

# Pre-seeded industry use cases
PRESEEDED_USE_CASES = [
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

async def seed_default_use_cases_if_empty():
    existing = get_all_use_cases()
    if not existing:
        for uc in PRESEEDED_USE_CASES:
            # 1. Save use case
            use_case_id = save_use_case(
                name=uc["name"],
                industry=uc["industry"],
                purpose=uc["purpose"],
                autonomy_level=uc["autonomy_level"],
                data_types=uc["data_types"],
                affected_population=uc["affected_population"],
                impact_tier=uc["impact_tier"],
                is_preseeded=True
            )
            # 2. Compute scoring
            scores = compute_deterministic_scores(
                industry=uc["industry"],
                purpose=uc["purpose"],
                autonomy_level=uc["autonomy_level"],
                data_types=uc["data_types"],
                affected_population=uc["affected_population"],
                impact_tier=uc["impact_tier"]
            )
            # 3. Retrieve evidence
            sources = await retrieve_governance_evidence(uc["name"], uc["industry"], uc["purpose"])
            # 4. Synthesize
            synthesis = await synthesize_governance_assessment(
                uc["name"], uc["industry"], uc["purpose"],
                uc["autonomy_level"], uc["data_types"],
                scores, sources
            )
            # 5. Persist
            save_full_assessment(
                use_case_id=use_case_id,
                overall_score=scores["overall_risk_score"],
                risk_level=scores["risk_level"],
                eu_ai_act=scores["eu_ai_act_category"],
                summary=synthesis["executive_summary"],
                dimensions=synthesis["dimension_assessments"],
                sources=sources
            )

@app.on_event("startup")
async def startup_event():
    init_db()
    await seed_default_use_cases_if_empty()

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "AegisAI Governance Engine", "version": "1.0.0"}

@app.get("/api/use-cases")
def list_use_cases():
    return get_all_use_cases()

@app.get("/api/assessments/{assessment_id}")
def read_assessment(assessment_id: int):
    details = get_assessment_details(assessment_id)
    if not details:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return details

@app.post("/api/assess")
async def assess_new_use_case(payload: UseCaseInput):
    """
    Dynamic assessment endpoint for pre-seeded or surprise live AI use cases.
    """
    # 1. Persist Use Case
    use_case_id = save_use_case(
        name=payload.name,
        industry=payload.industry,
        purpose=payload.purpose,
        autonomy_level=payload.autonomy_level,
        data_types=payload.data_types,
        affected_population=payload.affected_population,
        impact_tier=payload.impact_tier,
        is_preseeded=False
    )

    # 2. Compute Deterministic Scoring Matrix
    scores = compute_deterministic_scores(
        industry=payload.industry,
        purpose=payload.purpose,
        autonomy_level=payload.autonomy_level,
        data_types=payload.data_types,
        affected_population=payload.affected_population,
        impact_tier=payload.impact_tier
    )

    # 3. Retrieve Evidence from 6 Source Tiers (Local KB + Dynamic Web)
    sources = await retrieve_governance_evidence(payload.name, payload.industry, payload.purpose)

    # 4. AI Reasoning & Evidence Synthesis
    synthesis = await synthesize_governance_assessment(
        payload.name, payload.industry, payload.purpose,
        payload.autonomy_level, payload.data_types,
        scores, sources
    )

    # 5. Persist Full Assessment
    assessment_id = save_full_assessment(
        use_case_id=use_case_id,
        overall_score=scores["overall_risk_score"],
        risk_level=scores["risk_level"],
        eu_ai_act=scores["eu_ai_act_category"],
        summary=synthesis["executive_summary"],
        dimensions=synthesis["dimension_assessments"],
        sources=sources
    )

    return get_assessment_details(assessment_id)

@app.get("/api/sources")
def search_sources(query: str = "", source_tier: Optional[str] = None):
    return query_knowledge_base(query, source_tier)

@app.get("/api/analytics")
def get_analytics():
    cases = get_all_use_cases()
    total_cases = len(cases)
    high_critical_count = sum(1 for c in cases if c.get("risk_level") in ["High Risk", "Critical Risk"])
    
    tier_distribution = {
        "Law / Regulation": 4,
        "Regulatory Guidance": 4,
        "Industry Standard": 3,
        "Research": 2,
        "Vendor Information": 2,
        "General Web Content": 1
    }
    
    industry_breakdown = {}
    for c in cases:
        ind = c.get("industry", "Other")
        industry_breakdown[ind] = industry_breakdown.get(ind, 0) + 1

    return {
        "total_use_cases": total_cases,
        "high_critical_count": high_critical_count,
        "high_risk_ratio": round((high_critical_count / total_cases * 100) if total_cases > 0 else 0, 1),
        "source_tier_distribution": tier_distribution,
        "industry_breakdown": industry_breakdown
    }

@app.get("/api/export-report/{assessment_id}")
def export_report(assessment_id: int):
    details = get_assessment_details(assessment_id)
    if not details:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return {
        "title": f"AI Governance Assessment Report - {details['use_case_name']}",
        "export_timestamp": os.getenv("CURRENT_TIME", "2026-08-16"),
        "assessment": details
    }
