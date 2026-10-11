#!/usr/bin/env bash
# ==============================================================================
# scanet — Single Command One-Click Launcher (Linux / AWS EC2 / macOS)
# Cloned? Just run: ./run.sh
# ==============================================================================
set -e

# ANSI Color Tokens
CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear 2>/dev/null || true

cat << "EOF"
  ____                               _   
 / ___|  ___ __ _ _ __   ___| |_ 
 \___ \ / __/ _` | '_ \ / _ \ __|
  ___) | (_| (_| | | | |  __/ |_ 
 |____/ \___\__,_|_| |_|\___|\__|
 ─────────────────────────────────────────────────────────────
  ⚡ Lightweight Web-Orchestrated Cybersecurity Platform
  🔒 Multi-Tool Recon · OS Fingerprinting · AI Security Advisor
 ─────────────────────────────────────────────────────────────
EOF

echo -e "${CYAN}[*] Initializing scanet universal launcher...${NC}"

# Check for Python 3.10+
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo -e "${RED}[!] Error: Python 3 not found. Please install Python 3.10+ (e.g. sudo apt install python3).${NC}"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/.venv"

# Create and activate virtualenv if not existing
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[*] Creating Python virtual environment in $VENV_DIR ...${NC}"
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install/verify dependencies
echo -e "${BLUE}[*] Verifying requirements...${NC}"
pip install --upgrade pip -q
pip install -r "$BACKEND_DIR/requirements.txt" -q

# Ensure data directory exists
mkdir -p "$BACKEND_DIR/data"

echo -e "\n${GREEN}[✓] Setup complete! Launching scanet web platform...${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────────────${NC}"
echo -e "  🌐 ${CYAN}Web Dashboard:    ${GREEN}http://localhost:8000${NC}"
echo -e "  📚 ${CYAN}API Documentation: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  ⊕  ${CYAN}System Health:     ${GREEN}http://localhost:8000/api/v1/system/health${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────────────${NC}"
echo -e "Press CTRL+C at any time to stop the server.\n"

cd "$BACKEND_DIR"
exec uvicorn main:app --host 0.0.0.0 --port 8000
