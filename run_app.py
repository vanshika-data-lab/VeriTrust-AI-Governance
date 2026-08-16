"""
Single-command launcher for AegisAI Governance Application.
Starts FastAPI backend (port 8000) and Vite frontend (port 3000).
"""

import subprocess
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("=" * 70)
    print("🚀 Starting AegisAI Enterprise Governance & Risk Assessment Application")
    print("=" * 70)

    backend_dir = os.path.join(BASE_DIR, "backend")
    frontend_dir = os.path.join(BASE_DIR, "frontend")

    # 1. Start Backend FastAPI
    print("\n[1/2] Starting Python FastAPI Backend on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=backend_dir
    )

    time.sleep(2)

    # 2. Start Frontend Vite
    print("[2/2] Starting React Vite Frontend on http://localhost:3000 ...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )

    print("\n" + "=" * 70)
    print("✅ AegisAI Governance Application is now RUNNING!")
    print("👉 Access Dashboard UI: http://localhost:3000")
    print("👉 Access API Docs (Swagger): http://localhost:8000/docs")
    print("=" * 70)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping AegisAI servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
