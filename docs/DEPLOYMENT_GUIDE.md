# VeriTrust AI — Live Application URL & Cloud Deployment Guide

**Project**: VeriTrust AI — Enterprise AI Governance Platform  
**Author**: Vanshika Aggarwal  
**Challenge**: Modus Enterprise AI Build Challenge — Assignment 7  

---

## 1. Live Application Options

You can submit a live URL using any of the following 3 approaches:

### Option A: Free Cloud Deployment on Render / Vercel (Recommended)
1. **Repository Link**: [https://github.com/vanshika-data-lab/VeriTrust-AI-Governance](https://github.com/vanshika-data-lab/VeriTrust-AI-Governance)
2. **Backend (Render Free Web Service)**:
   - Go to [render.com](https://render.com) -> New -> Web Service.
   - Connect your GitHub repo: `vanshika-data-lab/VeriTrust-AI-Governance`.
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Resulting URL**: `https://veritrust-ai-backend.onrender.com`
3. **Frontend (Vercel / Render Static Site)**:
   - Go to [vercel.com](https://vercel.com) -> Import Git Repository.
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Resulting URL**: `https://veritrust-ai-governance.vercel.app`

---

### Option B: Instant Public Tunnel URL (1-Minute Live Demo Setup)
If running locally during evaluation, you can expose the local server to a live public HTTPS URL with one command using **ngrok** or **localtunnel**:

```bash
# Terminal 1: Start Application
python run_app.py

# Terminal 2: Expose Frontend Port 3000 to the Web
npx localtunnel --port 3000
```
This generates a live public URL (e.g. `https://veritrust-governance.loca.lt`) accessible by anyone worldwide.

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

## 2. Default Submission Links Template

| Field Name | Recommended Submission Content |
|---|---|
| **Live Application URL** | `https://veritrust-ai-governance.vercel.app` *(or your localtunnel / Render URL)* |
| **GitHub Repository** | `https://github.com/vanshika-data-lab/VeriTrust-AI-Governance` |
| **Backend API Health Check** | `http://localhost:5000/api/health` / `https://veritrust-ai-backend.onrender.com/api/health` |
