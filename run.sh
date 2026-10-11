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

# Determine port (default: 8000, or first argument, or $PORT env var)
PORT="${1:-${PORT:-8000}}"

# Ensure data directory exists
mkdir -p "$BACKEND_DIR/data"

# Detect Public IP (AWS EC2 metadata / checkip)
PUBLIC_IP=$(curl -s -m 2 https://checkip.amazonaws.com 2>/dev/null || curl -s -m 2 https://ifconfig.me 2>/dev/null || echo "")

echo -e "\n${GREEN}[✓] Setup complete! scanet running on port ${PORT}...${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────────────${NC}"
if [ -n "$PUBLIC_IP" ]; then
    echo -e "  🌐 ${CYAN}EC2 Public Access: \033[1;33mhttp://${PUBLIC_IP}:${PORT}${NC}"
fi
echo -e "  🌐 ${CYAN}Local Dashboard:   ${GREEN}http://localhost:${PORT}${NC}"
echo -e "  📚 ${CYAN}API Documentation: ${BLUE}http://localhost:${PORT}/docs${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────────────${NC}"
echo -e "  * AWS EC2 Tip: Ensure Inbound Port ${PORT} (Custom TCP) is OPEN in your Security Group!"
echo -e "Press CTRL+C at any time to stop the server.\n"

cd "$BACKEND_DIR"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
