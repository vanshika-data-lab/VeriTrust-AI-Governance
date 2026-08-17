# VeriTrust AI — Live Application URL & Cloud Deployment Guide

**Project**: VeriTrust AI — Enterprise AI Governance Platform  
**Author**: Vanshika Aggarwal  
**Challenge**: Modus Enterprise AI Build Challenge — Assignment 7  
**GitHub Repository**: [https://github.com/vanshika-data-lab/VeriTrust-AI-Governance](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance)  

---

## 1. Live Application Deployment Options (React + FastAPI)

### Option A: Free Production Cloud Deployment (Vercel + Render) 🌟
This preserves the exact, pixel-perfect React interface you see on localhost (`http://localhost:3000`).

1. **Frontend on Vercel (1-Click Free Hosting)**:
   - Go to **[vercel.com](https://vercel.com)** and log in with your GitHub account.
   - Click **"Add New..." -> "Project"** and import `vanshika-data-lab/VeriTrust-AI-Governance`.
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - Click **"Deploy"**.
   - Your live frontend URL will be generated: **`https://veritrust-ai-governance.vercel.app`**

2. **Backend API on Render (Free Web Service)**:
   - Go to **[render.com](https://render.com)** -> New -> Web Service.
   - Connect repository `vanshika-data-lab/VeriTrust-AI-Governance`.
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Your live backend URL will be: **`https://veritrust-backend.onrender.com`**

---

### Option B: Instant Public Live Tunnel (1-Minute Live Demo Setup)
If presenting live or running during evaluation, expose your local React application (`localhost:3000`) and FastAPI backend directly to a live public HTTPS URL with one command using **localtunnel** or **ngrok**:

```bash
# Terminal 1: Start Application Launcher (Runs Backend Port 5000 + Frontend Port 3000)
python run_app.py

# Terminal 2: Expose React Port 3000 to the Web
npx localtunnel --port 3000
```
This generates a live public URL (e.g. `https://veritrust-governance.loca.lt`) that displays the **exact, identical localhost React dashboard** to anyone worldwide.

Or with ngrok:
```bash
ngrok http 3000
```

---

### Option C: Docker Container Deployment
```bash
# Build the unified container
docker build -t veritrust-ai .

# Run on port 5000 / 3000
docker run -d -p 5000:5000 -p 3000:3000 --name veritrust veritrust-ai
```

---

## 2. Submission URL Reference

| Field Name | Recommended Submission Content |
|---|---|
| **Live Application URL** | `https://veritrust-ai-governance.vercel.app` *(or your localtunnel URL)* |
| **GitHub Repository** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance` |
| **Architecture Diagram** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/ARCHITECTURE_DIAGRAM.md` |
| **Technical Documentation** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/TECHNICAL_DOCUMENTATION.md` |
| **Database Model** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance/blob/main/docs/DATABASE_DATA_MODEL.md` |
