#!/usr/bin/env python3
"""
scanet — One-Click Universal Launcher
Sets up environment, verifies dependencies, initializes database,
and launches the web application on http://localhost:8000.
"""
import sys
import os
import subprocess
import webbrowser
import time

BANNER = r"""
  ____                               _   
 / ___|  ___ __ _ _ __   ___| |_ 
 \___ \ / __/ _` | '_ \ / _ \ __|
  ___) | (_| (_| | | | |  __/ |_ 
 |____/ \___\__,_|_| |_|\___|\__|
 ─────────────────────────────────────────────────────────────
  ⚡ Lightweight Web-Orchestrated Cybersecurity Platform
  🔒 Multi-Tool Recon · OS Fingerprinting · AI Security Advisor
 ─────────────────────────────────────────────────────────────
"""

def print_banner():
    # Green and cyan styling
    print("\033[96m" + BANNER + "\033[0m")

def check_python():
    if sys.version_info < (3, 10):
        print(f"\033[91m[!] Error: Python 3.10+ required. Current version is {sys.version}\033[0m")
        sys.exit(1)
    print("\033[92m[✓] Python version verified:\033[0m", sys.version.split()[0])

def setup_environment():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    data_dir = os.path.join(backend_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    print("\033[94m[*] Checking dependencies...\033[0m")
    req_file = os.path.join(backend_dir, "requirements.txt")
    
    # Try importing key packages; if missing, install them
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import aiosqlite
        print("\033[92m[✓] Core dependencies present.\033[0m")
    except ImportError:
        print("\033[93m[*] Installing dependencies from requirements.txt...\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("\033[92m[✓] Dependencies installed successfully.\033[0m")

def start_server():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    sys.path.insert(0, backend_dir)

    print("\n\033[92m[✓] Starting scanet server on http://localhost:8000 ...\033[0m")
    print("\033[96m" + "─" * 60 + "\033[0m")
    print("  🌐 Web Dashboard:    \033[1;36mhttp://localhost:8000\033[0m")
    print("  📚 API Documentation: \033[1;34mhttp://localhost:8000/docs\033[0m")
    print("  ⊕  System Health:     \033[1;32mhttp://localhost:8000/api/v1/system/health\033[0m")
    print("\033[96m" + "─" * 60 + "\033[0m")
    print("\033[90mPress CTRL+C at any time to stop the server.\033[0m\n")

    # Change CWD to backend so static assets and sqlite DB paths resolve correctly
    os.chdir(backend_dir)

    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\n\033[93m[*] scanet server terminated gracefully.\033[0m")

if __name__ == "__main__":
    print_banner()
    check_python()
    setup_environment()
    start_server()
