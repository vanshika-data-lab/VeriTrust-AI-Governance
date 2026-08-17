# VeriTrust AI — Comprehensive Technical Documentation

**Platform Name**: VeriTrust AI — Enterprise AI Governance & Risk Intelligence Platform  
**Candidate Name**: Vanshika Aggarwal  
**Challenge**: Modus Enterprise AI Build Challenge — Assignment 7  
**Target Domain Exposure**: BFSI / Financial Services, Healthcare, HR & Employment, Aviation & Aerospace  
**GitHub Repository**: [https://github.com/vanshika-data-lab/VeriTrust-AI-Governance](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance)  
**Version**: 1.0.0 (Enterprise Production Grade)  

---

## 1. Executive Summary & Questionnaire Alignment

VeriTrust AI is a full-stack, enterprise-grade AI Governance and Risk Assessment platform built to evaluate, score, and audit artificial intelligence systems operating in high-stakes, regulated environments.

In direct alignment with the **Candidate Technical Questionnaire**:
1. **Deterministic, Non-Black-Box Scoring**: Rather than relying on unreliable, uncalibrated LLM prompts to assign risk numbers, VeriTrust AI employs a **deterministic, weighted 10-dimension mathematical matrix** (`scoring_matrix.py`). The resulting scores are 100% reproducible, explainable, and auditable.
2. **6-Tier Source Hierarchy**: Classifies regulatory and technical evidence into a strict 6-tier credibility taxonomy, ranging from binding statutory law (Tier 1) down to general web commentary (Tier 6).
3. **Live Dynamic "Surprise Record" Ingestion**: Accepts completely un-seeded, novel AI use cases submitted by evaluators in real-time without code modifications.
4. **Persistent Relational Database**: Features a structured, ACID-compliant SQLite schema with 5 relational tables for complete auditability.
5. **100% Free & Open-Source Tech**: Operates independently of commercial API keys or proprietary software licenses.

---

## 2. 5-Layer System Architecture

VeriTrust AI implements the **Modus 5-Layer Enterprise AI Architecture**:

```
+-------------------------------------------------------------------------+
| Layer 1: Presentation & UI Layer (React 18, Vite, Modern Dark Theme)    |
| - Executive KPI Dashboard, "Surprise Record" Dynamic Evaluator, Gauges |
+-------------------------------------------------------------------------+
                                    | REST / JSON
+-------------------------------------------------------------------------+
| Layer 2: Application / API Gateway Layer (FastAPI, Python 3.10+, CORS)  |
| - Stateless Async Endpoints, Pydantic Type-Safe Payload Validation      |
+-------------------------------------------------------------------------+
                                    | Async Handlers
+-------------------------------------------------------------------------+
| Layer 3: AI Intelligence & Scoring Layer (Deterministic Matrix Engine)  |
| - 10-Dimension Risk Engine, EU AI Act Classifier, AI Synthesis Engine   |
+-------------------------------------------------------------------------+
                                    | ORM / SQL
+-------------------------------------------------------------------------+
| Layer 4: Data & Knowledge Persistence Layer (SQLite3 - governance_app.db)|
| - Normalized Tables: use_cases, assessments, dimensions, sources, KB    |
+-------------------------------------------------------------------------+
                                    | Inverted Index Queries
+-------------------------------------------------------------------------+
| Layer 5: External Research & Evidence Retrieval (6-Tier Statutory KB)   |
| - Canonical Statues (EU AI Act, GDPR, NYC LL144, ECOA, NIST AI RMF)     |
+-------------------------------------------------------------------------+
```

---

## 3. The 10-Dimension Governance Risk Matrix

The platform evaluates AI use cases across **10 mandatory governance dimensions**:

| # | Governance Dimension | Key Regulatory & Technical Focus | Impact Factors |
|---|---|---|---|
| 1 | **Data Governance & Lineage** | Data quality, provenance, sensitive category tagging, pipeline integrity. | PII, Financial, Biometrics, Health Data (+15 to +30 pts) |
| 2 | **Privacy Protection** | GDPR Art. 35 DPIA, consent mechanisms, data minimization, right to erasure. | Biometric/Health Data, Large Population Scale |
| 3 | **Bias & Demographic Fairness** | Disparate impact ratio, Title VII 80% rule, proxy discrimination. | Protected attributes, automated hiring/credit decisions |
| 4 | **Human Oversight** | EU AI Act Art. 14, Human-in-the-Loop vs Fully Autonomous decisioning. | Autonomous (+35 pts), Human-on-the-Loop (+20 pts) |
| 5 | **Explainability & Transparency** | Adverse Action notices (ECOA 12 CFR 1002), model interpretability (SHAP/LIME). | Black-box neural nets, high stakeholder impact |
| 6 | **Cybersecurity & Robustness** | Prompt injection resilience, SOC 2 CC6.1 access controls, model theft defense. | External facing, public network connectivity |
| 7 | **Decision Impact Severity** | Harm irreversibility, financial/bodily safety, operational criticality. | Critical Industry, Large Affected Population |
| 8 | **Regulatory Exposure** | Statutory liabilities under EU AI Act High-Risk, NYC LL144, FTC Act Sec 5. | BFSI, Healthcare, HR & Employment, Aviation |
| 9 | **Model Risk & Hallucination** | RAG grounding confidence, drift tolerance, validation benchmarks. | Generative LLMs, autonomous action agents |
| 10 | **Continuous Operational Monitoring** | Real-time telemetry, drift alerts, immutable audit logging cadence. | High-frequency trading, real-time diagnostic systems |

### 3.1 Composite Scoring Formula

The overall risk score $R_{overall}$ is computed as the weighted normalized sum:

$$R_{overall} = \sum_{i=1}^{10} (w_i \cdot S_i)$$

Where:
- $S_i \in [0, 100]$ represents the calculated score for dimension $i$.
- $w_i$ represents the dimension weight ($\sum w_i = 1.0$).
- Regulatory Exposure ($w_8 = 0.15$), Human Oversight ($w_4 = 0.15$), and Bias & Fairness ($w_3 = 0.15$) carry dominant weights for high-stakes enterprise systems.

### 3.2 Risk Classification Tiers

| Overall Score Range | Risk Level Tier | EU AI Act Classification | Deployment Action |
|---|---|---|---|
| **0.0 – 25.0** | **Minimal Risk** | Minimal / Low Risk | Authorized for immediate deployment with baseline monitoring. |
| **25.1 – 50.0** | **Low / Moderate Risk** | Limited Risk (Transparency obligations) | Authorized subject to user transparency disclosures. |
| **50.1 – 75.0** | **High Risk** | High-Risk (Annex III Mandatory Conformity) | Mandatory DPIA, pre-deployment algorithmic bias audit, and Human-in-the-Loop oversight. |
| **75.1 – 100.0** | **Critical Risk** | Unacceptable Risk (Article 5 Prohibited) or Strict High-Risk | Deployment blocked pending executive board and legal compliance sign-off. |

---

## 4. 6-Tier Evidence Retrieval & Classification Model

VeriTrust AI implements a strict hierarchical source indexing mechanism:

| Tier | Category Name | Authority & Reliability Weight | Examples in VeriTrust AI Knowledge Base |
|---|---|---|---|
| **Tier 1** | **Law / Regulation** | **1.00 (Binding Statutory)** | EU AI Act (Regulation 2024/1689), GDPR (Regulation 2016/679), NYC Local Law 144, ECOA (12 CFR Part 1002) |
| **Tier 2** | **Regulatory Guidance** | **0.95 (Enforcement Interpretation)** | FTC Guidance on AI & Algorithmic Deception, EEOC Guidance on ADA & Employment Tests, FDA Good Machine Learning Practice (GMLP), FAA DO-178C |
| **Tier 3** | **Industry Standards** | **0.90 (Consensus Frameworks)** | NIST AI Risk Management Framework (AI 100-1), ISO/IEC 42001:2023 AI Management System, SOC 2 Type II CC6.1 |
| **Tier 4** | **Academic Research** | **0.80 (Peer-Reviewed Science)** | Stanford CRFM Foundation Model Transparency Index, ACM FAccT Disparate Impact Auditing Standards |
| **Tier 5** | **Vendor Documentation**| **0.65 (Provider Assertions)** | Cloud Provider Responsible AI Documentation, Vendor Model Cards & Datasheets |
| **Tier 6** | **General Web Content** | **0.50 (Informational Commentary)**| Legal AI Analysis Blogs, Technology News, Industry Whitepapers |

---

## 5. REST API Specification & Endpoints

Base URL: `http://localhost:5000` (or live deployed host)

### 5.1 Endpoint Index

```
GET    /api/health                  # Service health status
GET    /api/use-cases               # Retrieve all evaluated AI systems
POST   /api/assess                  # Ingest & dynamically assess a novel use case
GET    /api/assessments/{id}        # Full 10-dimension assessment with 6-tier citations
DELETE /api/use-cases/{id}          # Remove use case & cascade delete assessments
GET    /api/sources                 # Query 6-tier knowledge base by term or tier
GET    /api/analytics               # Portfolio aggregate risk metrics & distributions
GET    /api/export-report/{id}      # Downloadable JSON compliance report payload
```

### 5.2 Dynamic Assessment Request (`POST /api/assess`)

**Request Payload:**
```json
{
  "name": "Biometric Facial Recognition for Retail Anti-Theft",
  "industry": "Retail & Security",
  "purpose": "Automated surveillance scanning customer facial geometry to match against known shoplifting databases in real time.",
  "autonomy_level": "Fully Autonomous",
  "data_types": ["Biometric", "Video Audio", "PII"],
  "affected_population": 500000,
  "impact_tier": "Critical"
}
```

**Response Payload (200 OK):**
```json
{
  "id": 5,
  "use_case_id": 5,
  "use_case_name": "Biometric Facial Recognition for Retail Anti-Theft",
  "industry": "Retail & Security",
  "overall_risk_score": 92.5,
  "risk_level": "Critical Risk",
  "eu_ai_act_category": "Unacceptable Risk (Article 5 Prohibited Biometric Surveillance)",
  "executive_summary": "System evaluated as CRITICAL RISK. Real-time biometric surveillance in publicly accessible spaces triggers outright prohibitions under EU AI Act Article 5(1)(d) and strict GDPR Article 9 Special Category Data sanctions.",
  "dimensions": [ ... 10 dimension objects ... ],
  "sources": [ ... 6-tier citation objects ... ]
}
```

---

## 6. Technology Stack & License Compliance Inventory

| Component | Technology | Version | License | Justification |
|---|---|---|---|---|
| **Backend Runtime** | Python | 3.10+ | PSFL (Open Source) | High stability, enterprise ML ecosystem |
| **API Web Framework**| FastAPI / Uvicorn | 0.110+ | MIT | High-performance asynchronous REST API |
| **Database Engine** | SQLite 3 | 3.x | Public Domain | Zero-configuration, zero-cost, persistent ACID store |
| **Frontend UI** | React | 18.3.1 | MIT | Reactive component-based enterprise interface |
| **Build Tool** | Vite | 5.4.x | MIT | Sub-second HMR and optimized production bundles |
| **UI Iconography** | Lucide React | 0.441.0 | ISC | High-fidelity consistent iconography |

**100% Free & Open-Source Verification**:
- Zero proprietary closed-source SDKs.
- Zero commercial API key requirements.
- 100% self-contained local execution capability.

---

## 7. Deployment & Infrastructure Guide

### 7.1 Local Single-Command Launch
```bash
python run_app.py
```
Starts FastAPI on `http://localhost:5000` and Vite Frontend on `http://localhost:3000`.

### 7.2 Docker Container Deployment
```bash
docker build -t veritrust-ai .
docker run -p 5000:5000 -p 3000:3000 veritrust-ai
```

### 7.3 Cloud Production Deployment (Render / Vercel)
- **Backend (FastAPI)**: Deploy to Render / Railway using `backend/main.py` with `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Frontend (React/Vite)**: Deploy to Vercel / Netlify with `npm run build`, targeting output directory `frontend/dist`.

---

## 8. Live Evaluator Walkthrough Script (10–15 Minutes)

1. **Phase 1: Executive KPI Overview (2 Mins)**
   - Walk through the top KPI metrics: Total Assessed Systems, High/Critical Risk Ratios, 6-Tier Source Index.
   - Showcase the 10 Governance Assessment Areas visual progress meters.
2. **Phase 2: 6-Tier Knowledge Explorer (3 Mins)**
   - Navigate to the **6-Tier Knowledge Base** tab.
   - Filter by Tier 1 (Law/Regulation) and Tier 3 (Industry Standard).
   - Demonstrate direct links to official statutory authority portals (EU EUR-Lex, NIST, FTC, ECOA).
3. **Phase 3: The "Surprise Record" Live Test (5 Mins)**
   - Navigate to the **Dynamic "Surprise Record" Test** tab.
   - Enter a completely novel AI system (or pick from pre-configured evaluator scenarios).
   - Execute the 4-step dynamic evaluation.
4. **Phase 4: Detailed Audit & 10-Dimension Breakdown (3 Mins)**
   - Review composite score, EU AI Act risk tier, and granular 10-dimension ratings.
   - Open the **6-Tier Citation Drawer** to inspect statutory references and concrete engineering controls.
5. **Phase 5: Compliance Audit Export (2 Mins)**
   - Click **Export Full Audit Report** to generate the JSON compliance dossier.
