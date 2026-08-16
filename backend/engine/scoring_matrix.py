"""
Deterministic Risk Scoring Matrix Engine for AI Governance
Computes reproducible, audit-traceable risk scores across 10 core governance dimensions.
"""

from typing import Dict, List, Any

DIMENSION_METADATA = {
    "data": {
        "name": "Data Lineage & Quality",
        "weight": 1.0,
        "description": "Evaluates training data representativeness, provenance, synthetic data usage, and data minimization."
    },
    "privacy": {
        "name": "Privacy & Data Protection",
        "weight": 1.2,
        "description": "Evaluates PII exposure, GDPR/CCPA compliance, consent mechanisms, and DPIA necessity."
    },
    "bias_fairness": {
        "name": "Bias, Fairness & Equity",
        "weight": 1.3,
        "description": "Evaluates demographic disparity risk, protected attribute handling, proxy variable contamination, and adverse impact."
    },
    "human_oversight": {
        "name": "Human Oversight & Autonomy Controls",
        "weight": 1.4,
        "description": "Evaluates human-in-the-loop vs fully autonomous execution, override controls, and emergency failsafes."
    },
    "explainability": {
        "name": "Explainability & Transparency",
        "weight": 1.1,
        "description": "Evaluates model interpretabillity, recourse availability for affected individuals, and adverse action disclosures."
    },
    "security": {
        "name": "Cybersecurity & Model Robustness",
        "weight": 1.2,
        "description": "Evaluates resistance to prompt injection, data poisoning, model inversion, and access control vulnerability."
    },
    "decision_impact": {
        "name": "Decision Impact & Severity",
        "weight": 1.5,
        "description": "Evaluates potential severity of financial, legal, physical, or employment outcomes on individuals."
    },
    "regulatory_exposure": {
        "name": "Regulatory Exposure & Compliance",
        "weight": 1.4,
        "description": "Evaluates exposure under statutory frameworks (EU AI Act, NYC LL144, ECOA, GDPR, HIPAA)."
    },
    "model_risk": {
        "name": "Model Reliability & Drift Risk",
        "weight": 1.0,
        "description": "Evaluates hallucination rates, out-of-distribution failure risk, and model architecture instability."
    },
    "monitoring": {
        "name": "Continuous Monitoring & Auditability",
        "weight": 1.0,
        "description": "Evaluates post-deployment telemetry, logging standards, drift detection, and periodic re-audit intervals."
    }
}

AUTONOMY_WEIGHTS = {
    "Fully Autonomous": 1.0,
    "Human-on-the-Loop": 0.75,
    "Human-in-the-Loop": 0.50,
    "Advisory / Decision Support": 0.30
}

IMPACT_WEIGHTS = {
    "Critical": 1.0,
    "High": 0.8,
    "Medium": 0.5,
    "Low": 0.2
}

SENSITIVE_DATA_TYPES = {"PII", "Biometric", "Medical", "Financial", "Protected Attributes", "Child Data"}

def compute_deterministic_scores(
    industry: str,
    purpose: str,
    autonomy_level: str,
    data_types: List[str],
    affected_population: int,
    impact_tier: str
) -> Dict[str, Any]:
    
    autonomy_w = AUTONOMY_WEIGHTS.get(autonomy_level, 0.6)
    impact_w = IMPACT_WEIGHTS.get(impact_tier, 0.5)

    # Sensitivity factor
    sensitive_count = sum(1 for dt in data_types if dt in SENSITIVE_DATA_TYPES)
    data_sensitivity_factor = min(1.0, 0.3 + (sensitive_count * 0.2))

    # Scale factor for population
    if affected_population > 500000:
        scale_factor = 1.0
    elif affected_population > 50000:
        scale_factor = 0.85
    elif affected_population > 5000:
        scale_factor = 0.70
    else:
        scale_factor = 0.50

    # Industry risk baselines
    industry_lower = industry.lower()
    if any(k in industry_lower for k in ["banking", "finance", "credit", "insurance"]):
        ind_risk_bias = 0.9
        ind_risk_reg = 0.95
        ind_risk_privacy = 0.85
    elif any(k in industry_lower for k in ["health", "medical", "pharma"]):
        ind_risk_bias = 0.8
        ind_risk_reg = 0.95
        ind_risk_privacy = 0.95
    elif any(k in industry_lower for k in ["hr", "hiring", "recruitment", "employment"]):
        ind_risk_bias = 0.95
        ind_risk_reg = 0.90
        ind_risk_privacy = 0.80
    elif any(k in industry_lower for k in ["aviation", "aerospace", "transport", "autonomous"]):
        ind_risk_bias = 0.4
        ind_risk_reg = 0.90
        ind_risk_privacy = 0.50
    else:
        ind_risk_bias = 0.6
        ind_risk_reg = 0.6
        ind_risk_privacy = 0.6

    dimension_results = {}
    weighted_score_sum = 0.0
    weight_total = 0.0

    # Calculate score per dimension (0 to 100)
    for key, meta in DIMENSION_METADATA.items():
        base = 40.0
        
        if key == "data":
            base += (data_sensitivity_factor * 35.0) + (impact_w * 25.0)
        elif key == "privacy":
            base += (data_sensitivity_factor * 40.0) + (ind_risk_privacy * 25.0)
        elif key == "bias_fairness":
            base += (ind_risk_bias * 35.0) + (impact_w * 25.0)
        elif key == "human_oversight":
            base += (autonomy_w * 45.0) + (impact_w * 15.0)
        elif key == "explainability":
            base += (autonomy_w * 30.0) + (impact_w * 30.0)
        elif key == "security":
            base += (scale_factor * 30.0) + (autonomy_w * 30.0)
        elif key == "decision_impact":
            base += (impact_w * 50.0) + (scale_factor * 10.0)
        elif key == "regulatory_exposure":
            base += (ind_risk_reg * 40.0) + (impact_w * 20.0)
        elif key == "model_risk":
            base += (autonomy_w * 35.0) + (scale_factor * 25.0)
        elif key == "monitoring":
            base += (scale_factor * 30.0) + (autonomy_w * 30.0)

        # Cap score between 10 and 98
        score = min(98.0, max(12.0, round(base, 1)))

        if score >= 75.0:
            level = "Critical" if score >= 88.0 else "High"
        elif score >= 50.0:
            level = "Medium"
        else:
            level = "Low"

        dimension_results[key] = {
            "dimension_key": key,
            "dimension_name": meta["name"],
            "risk_score": score,
            "risk_level": level,
            "weight": meta["weight"]
        }

        weighted_score_sum += score * meta["weight"]
        weight_total += meta["weight"]

    overall_score = round(weighted_score_sum / weight_total, 1)

    if overall_score >= 82.0:
        overall_level = "Critical Risk"
        eu_ai_act = "High Risk (Mandatory Conformity & FRIA required)"
    elif overall_score >= 68.0:
        overall_level = "High Risk"
        eu_ai_act = "High Risk (Annex III Listed Category)"
    elif overall_score >= 48.0:
        overall_level = "Medium Risk"
        eu_ai_act = "Specific Transparency Risk (Article 50 Obligations)"
    else:
        overall_level = "Low Risk"
        eu_ai_act = "Minimal Risk (Voluntary Code of Conduct)"

    # Handle prohibited AI cases (e.g. social scoring, untargeted biometric scraping)
    purpose_lower = purpose.lower()
    if any(p in purpose_lower for p in ["social scoring", "subliminal manipulation", "biometric categorisation for politics"]):
        overall_score = 99.0
        overall_level = "Critical Risk"
        eu_ai_act = "Unacceptable Risk (Prohibited under Article 5)"

    return {
        "overall_risk_score": overall_score,
        "risk_level": overall_level,
        "eu_ai_act_category": eu_ai_act,
        "dimensions": dimension_results
    }
