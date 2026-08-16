# VeriTrust AI — Enterprise AI Governance & Risk Intelligence Platform

VeriTrust AI is a full-stack, enterprise-grade AI Governance and Risk Assessment application built to continuously evaluate, score, and audit artificial intelligence use cases against global legal statutes, regulatory guidance, and industry standards.

---

## 🌟 Key Features & Deliverables Checklist

- [x] **10 Mandatory AI Governance Assessment Dimensions**:
  1. **Data Governance & Quality**
  2. **Privacy & Data Protection**
  3. **Bias & Demographic Fairness**
  4. **Human Oversight & Autonomy Controls**
  5. **Explainability & Transparency**
  6. **Cybersecurity & Model Robustness**
  7. **Decision Impact Severity**
  8. **Regulatory & Statutory Exposure**
  9. **Model Risk & Hallucination Management**
  10. **Continuous Operational Monitoring & Auditing**

- [x] **6-Tier Knowledge Base & Citation Engine**:
  - **Tier 1: Law / Regulation** (e.g., EU AI Act Regulation 2024/1689, GDPR, NYC Local Law 144, ECOA Regulation B)
  - **Tier 2: Regulatory Guidance** (e.g., NIST AI RMF 1.0, FTC Section 5 Enforcement Guidance, EEOC Disparate Impact Guidance)
  - **Tier 3: Industry Standards** (e.g., ISO/IEC 42001:2023 AIMS, IEEE 7000 Ethical System Design, SOC 2 Type II AI Criteria)
  - **Tier 4: Academic Research** (e.g., Stanford HAI AI Index Report 2024, NIST SP 1270 Socio-Technical Bias)
  - **Tier 5: Vendor Specifications** (e.g., AWS Bedrock Guardrails, Microsoft Responsible AI Standard v2)
  - **Tier 6: General Web Content** (e.g., Gartner AI TRiSM Architecture Matrix)

- [x] **Repeatable & Deterministic Scoring Engine**:
  - Uses weighted domain matrices, data type sensitivities (PII, Biometrics, Medical, Financial), affected population scaling, and autonomy multipliers.
  - Generates reproducible numerical risk scores (0–100) and risk classifications (Low, Medium, High, Critical).

- [x] **Dynamic "Surprise Record" Live Assessment**:
  - Allows evaluators to dynamically submit novel, un-seeded AI use cases for instant 10-dimension evaluation and evidence retrieval.

- [x] **Executive Dashboard & Audit Export**:
  - Interactive risk distribution, industry risk breakdown, tier breakdown, and one-click JSON/PDF audit report download.

---

## 🏗️ Project Architecture

```
ai_governance_app/
├── backend/
│   ├── app.py                      # Flask REST API server
│   ├── db_manager.py               # SQLite database interface & migrations
│   ├── research_retriever.py       # 6-Tier knowledge base retrieval engine
│   ├── risk_assessment_engine.py   # 10-Dimension risk scoring matrix
│   ├── data/
│   │   └── seed_knowledge_base.json # Initial 6-Tier knowledge base seed
│   └── database/
│       └── governance_app.db       # Persistent SQLite database store
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx               # High-contrast navigation bar
│   │   │   ├── DashboardView.jsx        # Executive risk analytics dashboard
│   │   │   ├── AssessmentForm.jsx       # Dynamic "Surprise Record" test form
│   │   │   ├── AssessmentDetailView.jsx # 10-dimension audit detail view
│   │   │   └── KnowledgeExplorerView.jsx# 6-Tier knowledge base explorer
│   │   ├── App.jsx                      # Main app container & routing state
│   │   └── index.css                    # Design system & dark theme tokens
│   ├── index.html                       # Application HTML entry point
│   ├── package.json                     # Frontend dependencies
│   └── vite.config.js                   # Vite configuration & backend proxy
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**

### 1. Start the Flask Backend Server
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install flask flask-cors

# Start the Flask API server (runs on http://localhost:5000)
python app.py
```

### 2. Start the Vite Frontend Client
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server (runs on http://localhost:3000)
npm run dev
```

Open your browser at `http://localhost:3000` to interact with the platform!

---

## 📊 10-Dimension Scoring System Logic

| Dimension | Key Evaluation Criteria |
|---|---|
| **Data Governance** | Data sensitivity (PII, Biometrics, Medical), data lineage, training set provenance |
| **Privacy Protection** | GDPR Art 35 DPIA compliance, data minimization, consent mechanisms |
| **Bias & Fairness** | Demographic parity, Title VII 80% Rule, disparate impact evaluation |
| **Human Oversight** | Decision autonomy level (Fully Autonomous vs. Human-in-the-Loop) |
| **Explainability** | Black-box model opacity vs. ECOA 12 CFR 1002.9 adverse action notice capability |
| **Cybersecurity** | SOC 2 CC6.1 access control, prompt injection defense, data poisoning resilience |
| **Decision Impact** | Reversibility of harm, population scale, critical infrastructure involvement |
| **Regulatory Exposure** | Multi-jurisdictional liability (EU AI Act High Risk, NYC LL144, FTC Sec 5) |
| **Model Risk** | Hallucination mitigation (RAG grounding), performance drift monitoring |
| **Continuous Monitoring** | Telemetry logging, audit frequency, real-time alert triggers |

---

## 📜 License & Compliance Notice
Developed for enterprise AI governance assessment, regulatory audit, and compliance evaluation.
