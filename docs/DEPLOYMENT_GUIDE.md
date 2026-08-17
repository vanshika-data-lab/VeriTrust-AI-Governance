# VeriTrust AI — Live Application URL & Cloud Deployment Guide

**Project**: VeriTrust AI — Enterprise AI Governance Platform  
**Author**: Vanshika Aggarwal  
**Challenge**: Modus Enterprise AI Build Challenge — Assignment 7  
**GitHub Repository**: [https://github.com/vanshika-data-lab/VeriTrust-AI-Governance](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance)  

---

## 1. Primary Live Application Method: Streamlit Community Cloud (Recommended 🌟)

Streamlit Community Cloud provides an **instant, 100% free, 1-click public HTTPS URL** with zero configuration.

### 🚀 60-Second Deployment Steps:
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"**.
3. Select your repository:
   - **Repository**: `vanshika-data-lab/VeriTrust-AI-Governance`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy!"**
5. Streamlit will install dependencies from `requirements.txt` and launch your live application at:
   👉 **`https://veritrust-ai-governance.streamlit.app`** (or custom sub-domain of your choice)

---

## 2. Alternative Live Deployment Options

### Option B: Free Cloud Deployment on Render / Vercel
1. **Backend (Render Free Web Service)**:
   - Go to [render.com](https://render.com) -> New -> Web Service.
   - Connect your GitHub repo: `vanshika-data-lab/VeriTrust-AI-Governance`.
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. **Frontend (Vercel)**:
   - Go to [vercel.com](https://vercel.com) -> Import `vanshika-data-lab/VeriTrust-AI-Governance`.
   - **Root Directory**: `frontend` -> Output: `dist`.

---

### Option C: Instant Public Tunnel URL (1-Minute Live Demo Setup)
If running locally during evaluation, expose the local server to a live public HTTPS URL with one command using **ngrok** or **localtunnel**:

```bash
# Terminal 1: Start Streamlit App
streamlit run app.py

# Terminal 2: Expose Port 8501 to the Web
npx localtunnel --port 8501
```
This generates a live public URL (e.g. `https://veritrust-governance.loca.lt`) accessible worldwide.

---

### Option D: Docker Container Deployment
```bash
# Build the unified container
docker build -t veritrust-ai .

# Run on port 5000 / 3000
docker run -d -p 5000:5000 -p 3000:3000 --name veritrust veritrust-ai
```

---

## 3. Submission URL Template

| Field Name | Recommended Submission Content |
|---|---|
| **Live Application URL** | `https://veritrust-ai-governance.streamlit.app` |
| **GitHub Repository** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance` |
| **Architecture Diagram** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/ARCHITECTURE_DIAGRAM.md` |
| **Technical Documentation** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/TECHNICAL_DOCUMENTATION.md` |
| **Database Model** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/DATABASE_DATA_MODEL.md` |
