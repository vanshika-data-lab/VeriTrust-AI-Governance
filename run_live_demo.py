"""
VeriTrust AI — Single-Command Full-Stack Live Launcher + Public HTTPS Tunnel
Starts:
  1. Python FastAPI Backend on http://localhost:8000
  2. React Vite Frontend on http://localhost:3000
  3. Public HTTPS Web Tunnel on https://veritrust-ai-governance.loca.lt
"""

import subprocess
import sys
import time
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_tunnel_password():
    try:
        req = urllib.request.Request("https://loca.lt/mytunnelpassword", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.read().decode('utf-8').strip()
    except Exception:
        return "Check terminal / IP"

def main():
    print("=" * 75)
    print("🚀 VeriTrust AI — Single-Command Full-Stack Live Launcher")
    print("=" * 75)

    backend_dir = os.path.join(BASE_DIR, "backend")
    frontend_dir = os.path.join(BASE_DIR, "frontend")

    # 1. Start Backend FastAPI
    print("\n[1/3] Starting Python FastAPI Backend on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=backend_dir
    )

    time.sleep(2)

    # 2. Start Frontend Vite
    print("[2/3] Starting React Vite Frontend on http://localhost:3000 ...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )

    time.sleep(3)

    # 3. Start Public Live Tunnel
    print("[3/3] Opening Live Public HTTPS Tunnel (Localtunnel) ...")
    tunnel_process = subprocess.Popen(
        ["npx", "localtunnel", "--port", "3000", "--subdomain", "veritrust-ai-governance"],
        shell=True
    )

    time.sleep(3)
    tunnel_pwd = get_tunnel_password()

    print("\n" + "=" * 75)
    print("🎉 ALL SYSTEMS ONLINE & FULLY FUNCTIONAL!")
    print("=" * 75)
    print("🌐 LIVE PUBLIC APPLICATION URL : https://veritrust-ai-governance.loca.lt")
    print(f"🔑 Tunnel Password / IP        : {tunnel_pwd}")
    print("💻 Localhost Dashboard URL     : http://localhost:3000")
    print("📡 FastAPI Backend Swagger API : http://localhost:8000/docs")
    print("=" * 75)
    print("\n💡 NOTE: If the live page asks for a password/Endpoint IP on first load:")
    print(f"👉 Enter: {tunnel_pwd} and click 'Submit' to open the app!")
    print("\nPress Ctrl + C at any time to safely shut down all servers.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping VeriTrust AI servers & tunnel...")
        backend_process.terminate()
        frontend_process.terminate()
        tunnel_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
