# VeriTrust AI — Enterprise AI Governance & Risk Intelligence Platform

VeriTrust AI is a full-stack, enterprise-grade AI Governance and Risk Assessment platform built to evaluate, score, and audit artificial intelligence use cases against global legal statutes, regulatory guidance, and industry standards.

---

## 📋 Assignment 7 Key Deliverables & Compliance Verification

| Assignment Deliverable Requirement | Project Implementation | Status |
|---|---|---|
| **10 Mandatory Assessment Dimensions** | Evaluates Data, Privacy, Bias/Fairness, Human Oversight, Explainability, Security, Impact, Regulatory Exposure, Model Risk, & Monitoring | ✅ **Completed** |
| **6-Tier Citation & Evidence Engine** | Categorizes evidence into *Law/Regulation*, *Regulatory Guidance*, *Industry Standard*, *Research*, *Vendor Information*, & *General Web Content* | ✅ **Completed** |
| **Repeatable & Deterministic Scoring** | Weighted mathematical matrix calculating score (0–100) and risk tier based on data sensitivity, autonomy level, & population scale | ✅ **Completed** |
| **Live Evaluator Testing ("Surprise Record")** | Evaluator can input any custom, novel AI use case to dynamically run dynamic assessment and legal retrieval | ✅ **Completed** |
| **Audit Export & Report Generation** | One-click JSON / PDF compliance report download for enterprise audit logs | ✅ **Completed** |
| **Validated Official Authority Links** | 100% active canonical links to official legal repositories (EUR-Lex, GDPR, NIST, ISO, CFPB, EEOC, FTC) | ✅ **Completed** |

---

## 🏗️ Architecture & Component Overview

```
ai_governance_app/
├── backend/
│   ├── app.py                      # Flask REST API server & router
│   ├── db_manager.py               # SQLite database manager & migration engine
│   ├── research_retriever.py       # 6-Tier knowledge base retrieval engine
│   ├── risk_assessment_engine.py   # 10-Dimension risk scoring matrix
│   ├── data/
│   │   └── seed_knowledge_base.json # 6-Tier legal & regulatory knowledge base
│   └── database/
│       └── governance_app.db       # SQLite database store
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx               # Navigation header & tab state
│   │   │   ├── DashboardView.jsx        # Executive risk analytics dashboard
│   │   │   ├── AssessmentForm.jsx       # Dynamic "Surprise Record" test form
│   │   │   ├── AssessmentDetailView.jsx # 10-dimension audit breakdown
│   │   │   ├── EvidenceDrawer.jsx       # 6-Tier citation drawer
│   │   │   └── KnowledgeExplorerView.jsx# Regulatory knowledge base explorer
│   │   ├── App.jsx                      # Main React container
│   │   └── index.css                    # Design system styling tokens
│   ├── index.html                       # HTML entry point
│   ├── package.json                     # Frontend dependencies
│   └── vite.config.js                   # Vite configuration & dev proxy
├── run_app.py                           # Single-command unified application launcher
├── README.md                            # Complete platform documentation
└── .gitignore                           # Repository exclusions
```

---

## 🚀 Quick Start Instructions

### Option 1: Single-Command Full Stack Launcher (Recommended)

Run both the Flask backend (Port 5000) and Vite frontend (Port 3000) simultaneously with one command:

```bash
python run_app.py
```

Open your browser at `http://localhost:3000`.

---

### Option 2: Manual Terminal Startup

#### Terminal 1 — Start Backend Server:
```bash
cd backend
pip install flask flask-cors
python app.py
```
*(Backend API runs at http://localhost:5000)*

#### Terminal 2 — Start Frontend Client:
```bash
cd frontend
npm install
npm run dev
```
*(Frontend UI runs at http://localhost:3000)*

---

## 🎯 Evaluator Live Testing Guide ("Surprise Record" Test)

To test a completely new AI use case dynamically:

1. Click on **`Dynamic "Surprise Record" Test`** in the top navigation bar.
2. Either click one of the **Quick Load Sample Demo Buttons** or enter custom details:
   - **System Name**: e.g., *Autonomous Medical Triage Chatbot*
   - **Industry**: e.g., *Healthcare & Life Sciences*
   - **Autonomy Level**: e.g., *Fully Autonomous*
   - **Data Types**: Select *Medical*, *PII*, *Biometric*
   - **Affected Population**: e.g., *250,000*
   - **Impact Severity**: e.g., *Critical*
3. Click **`Execute Dynamic 10-Dimension Risk & Evidence Assessment`**.
4. View the generated score, risk level, dimension ratings, statutory obligations, and 6-tier evidence citations!
5. Click **`Export Full Audit Report`** to download the JSON report artifact.

---

## 🛰️ REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/use-cases` | List all evaluated AI use cases |
| `GET` | `/api/use-cases/<id>` | Get specific use case assessment summary |
| `GET` | `/api/assessments/<id>` | Get complete 10-dimension assessment with 6-tier evidence citations |
| `POST` | `/api/assess` | Dynamically assess a new AI use case ("Surprise Record") |
| `GET` | `/api/sources` | Search 6-tier knowledge base by query and source tier |
| `GET` | `/api/analytics` | Get aggregate KPI metrics, risk distribution, & industry breakdown |
| `GET` | `/api/export-report/<id>` | Export complete compliance report JSON artifact |

---

## ⚖️ 10-Dimension Risk Evaluation Matrix Logic

1. **Data Governance & Quality**: Evaluates sensitivity of processed datasets (PII, Biometrics, Health Data, Financial Records) and provenance tracking.
2. **Privacy & Data Protection**: Checks compliance with GDPR Art. 35 (DPIA), data minimization rules, and explicit consent requirements.
3. **Bias & Demographic Fairness**: Evaluates disparate impact using the Title VII 4/5ths (80%) Rule and protected attribute filtering.
4. **Human Oversight & Autonomy**: Assesses decision autonomy (Fully Autonomous vs. Human-in-the-Loop) and emergency override mechanisms (EU AI Act Art. 14).
5. **Explainability & Transparency**: Audits model interpretability and ECOA 12 CFR 1002.9 adverse action explanation capabilities.
6. **Cybersecurity & Robustness**: Audits SOC 2 CC6.1 access controls, prompt injection defenses, and data poisoning resilience.
7. **Decision Impact Severity**: Evaluates reversibility of harm, scale of affected individuals, and safety-critical operations.
8. **Regulatory Exposure**: Calculates statutory liabilities under EU AI Act High-Risk rules, NYC LL144, FTC Section 5, and EEOC guidelines.
9. **Model Risk & Hallucination**: Evaluates RAG grounding confidence thresholds and hallucination mitigation mechanisms.
10. **Continuous Monitoring**: Tracks real-time telemetry logging, performance drift detection, and automated audit frequencies.

---

## 📜 License & Enterprise Notice
Developed for enterprise AI governance assessment, regulatory audit compliance, and responsible AI deployment.
