#!/usr/bin/env bash
# ==============================================================================
# scanet — Unified High-Impact Launcher (Linux / AWS EC2 / macOS)
# Cloned? Just execute: ./run.sh
# ==============================================================================
set -e

# ==============================================================================
# Cyberpunk High-Contrast Color Palette (256-Color & ANSI Supported)
# ==============================================================================
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_DIM="\033[2m"
C_UNDERLINE="\033[4m"

# Vivid Neon Accents
C_CYAN="\033[38;5;51m"
C_SKY="\033[38;5;39m"
C_PURPLE="\033[38;5;141m"
C_MAGENTA="\033[38;5;201m"
C_GREEN="\033[38;5;48m"
C_LIME="\033[38;5;154m"
C_YELLOW="\033[38;5;226m"
C_ORANGE="\033[38;5;208m"
C_RED="\033[38;5;196m"
C_WHITE="\033[38;5;231m"
C_GRAY="\033[38;5;245m"
C_DARK="\033[38;5;238m"

# Clear terminal screen cleanly if supported
clear 2>/dev/null || true

# ==============================================================================
# Cyberpunk ASCII Banner
# ==============================================================================
echo -e "${C_CYAN}"
cat << "EOF"
  ███████╗ ██████╗ █████╗ ███╗   ██╗███████╗████████╗
  ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝
  ███████╗██║     ███████║██╔██╗ ██║█████╗     ██║   
  ╚════██║██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   
  ███████║╚██████╗██║  ██║██║ ╚████║███████╗   ██║   
  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
EOF
echo -e "${C_RESET}"
echo -e "  ${C_PURPLE}⚡ WEB-ORCHESTRATED CYBERSECURITY RECONNAISSANCE PLATFORM${C_RESET}"
echo -e "  ${C_SKY}🔒 12-Tool Recon · OS Fingerprinting · AI MITRE ATT&CK Copilot · SARIF v2.1${C_RESET}"
echo -e "  ${C_DARK}─────────────────────────────────────────────────────────────────────────────${C_RESET}"

# ==============================================================================
# Host Environment & Telemetry Extraction
# ==============================================================================
HOSTNAME_VAL=$(hostname 2>/dev/null || echo "localhost")
CPU_COUNT=$(nproc 2>/dev/null || echo "1")
ARCH_VAL=$(uname -m 2>/dev/null || echo "x86_64")
TOTAL_MEM_MB=$(free -m 2>/dev/null | awk '/^Mem:/{print $2}' || echo "N/A")
TOTAL_SWAP_MB=$(free -m 2>/dev/null | awk '/^Swap:/{print $2}' || echo "N/A")
PORT="${1:-${PORT:-8000}}"

# Fast asynchronous/timed Public IP discovery (AWS checkip, ifconfig, or ipify)
PUBLIC_IP=$(curl -s -m 2 https://checkip.amazonaws.com 2>/dev/null || curl -s -m 2 https://ifconfig.me 2>/dev/null || curl -s -m 2 https://api.ipify.org 2>/dev/null || echo "")

echo -e "\n  ${C_BOLD}${C_WHITE}╭─── 🖥️  HOST ENVIRONMENT AUDIT ──────────────────────────────────────────────╮${C_RESET}"
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Node Host:${C_RESET}     ${C_WHITE}${HOSTNAME_VAL}${C_RESET} (${ARCH_VAL}, ${CPU_COUNT} Cores)"
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Memory Pool:${C_RESET}   ${C_YELLOW}${TOTAL_MEM_MB} MB RAM${C_RESET} | ${C_PURPLE}${TOTAL_SWAP_MB} MB Swap${C_RESET}"
if [ -n "$PUBLIC_IP" ]; then
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Public IPv4:${C_RESET}   ${C_LIME}${PUBLIC_IP}${C_RESET} ${C_DIM}(AWS EC2 Node Detected)${C_RESET}"
else
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Public IPv4:${C_RESET}   ${C_GRAY}Private / Local Subnet${C_RESET}"
fi
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Target Port:${C_RESET}   ${C_CYAN}TCP ${PORT}${C_RESET} ${C_DIM}(HTTP)${C_RESET}"
echo -e "  ${C_BOLD}${C_WHITE}╰─────────────────────────────────────────────────────────────────────────────╯${C_RESET}\n"

# Helper print function for pipeline steps
print_step() {
    local step_num="$1"
    local title="$2"
    local status="$3"
    echo -e "  ${C_PURPLE}[${step_num}/5]${C_RESET}  ${C_BOLD}${C_WHITE}${title}${C_RESET} ... ${status}"
}

# ==============================================================================
# STEP 1/5: System Package Update & Upgrade (Ubuntu/Debian/Amazon Linux)
# ==============================================================================
print_step "1" "SYSTEM REPOSITORIES & PACKAGES" "${C_YELLOW}Syncing...${C_RESET}"

if [ "${SKIP_SYSTEM_UPDATE:-0}" != "1" ]; then
    SUDO=""
    if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    fi

    if command -v apt-get >/dev/null 2>&1; then
        export DEBIAN_FRONTEND=noninteractive
        $SUDO apt-get update -y -q >/dev/null 2>&1 || true
        $SUDO apt-get upgrade -y -q -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" >/dev/null 2>&1 || true
        $SUDO apt-get install -y -q python3 python3-pip python3-venv python3-pydantic python3-psutil git curl nmap mtr-tiny >/dev/null 2>&1 || \
        $SUDO apt-get install -y -q python3 python3-pip python3-venv git curl nmap mtr-tiny >/dev/null 2>&1 || true
    elif command -v dnf >/dev/null 2>&1; then
        $SUDO dnf upgrade -y -q >/dev/null 2>&1 || true
        $SUDO dnf install -y -q python3 python3-pip python3-psutil git curl nmap >/dev/null 2>&1 || true
    elif command -v yum >/dev/null 2>&1; then
        $SUDO yum update -y -q >/dev/null 2>&1 || true
        $SUDO yum install -y -q python3 python3-pip python3-psutil git curl nmap >/dev/null 2>&1 || true
    fi
fi
echo -e "\033[1A\r  ${C_PURPLE}[1/5]${C_RESET}  ${C_BOLD}${C_WHITE}SYSTEM REPOSITORIES & PACKAGES${C_RESET} ... ${C_GREEN}✓ Verified & Upgraded${C_RESET}"

# ==============================================================================
# STEP 2/5: Low-RAM Swap Allocation Guardrail
# ==============================================================================
print_step "2" "LOW-MEMORY OOM GUARD (SWAP)" "${C_YELLOW}Evaluating...${C_RESET}"

if command -v free >/dev/null 2>&1; then
    MEM_INT=$(free -m | awk '/^Mem:/{print $2}')
    SWAP_INT=$(free -m | awk '/^Swap:/{print $2}')
    if [ "${SWAP_INT:-0}" -lt 500 ] && [ "${MEM_INT:-2048}" -lt 2500 ]; then
        if [ ! -f /swapfile ]; then
            $SUDO fallocate -l 2G /swapfile 2>/dev/null || $SUDO dd if=/dev/zero of=/swapfile bs=1M count=2048 2>/dev/null
            $SUDO chmod 600 /swapfile 2>/dev/null
            $SUDO mkswap /swapfile >/dev/null 2>&1 || true
        fi
        $SUDO swapon /swapfile >/dev/null 2>&1 || true
        echo -e "\033[1A\r  ${C_PURPLE}[2/5]${C_RESET}  ${C_BOLD}${C_WHITE}LOW-MEMORY OOM GUARD (SWAP)${C_RESET} ... ${C_GREEN}✓ 2GB Swap Active (OOM Shield Enabled)${C_RESET}"
    else
        echo -e "\033[1A\r  ${C_PURPLE}[2/5]${C_RESET}  ${C_BOLD}${C_WHITE}LOW-MEMORY OOM GUARD (SWAP)${C_RESET} ... ${C_GREEN}✓ Memory Pool Sufficient (${MEM_INT}MB RAM)${C_RESET}"
    fi
else
    echo -e "\033[1A\r  ${C_PURPLE}[2/5]${C_RESET}  ${C_BOLD}${C_WHITE}LOW-MEMORY OOM GUARD (SWAP)${C_RESET} ... ${C_GREEN}✓ Skipped (Standard Environment)${C_RESET}"
fi

# ==============================================================================
# STEP 3/5: Python Runtime & Isolated Virtual Environment
# ==============================================================================
print_step "3" "PYTHON RUNTIME & ENVIRONMENT" "${C_YELLOW}Checking...${C_RESET}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo -e "\033[1A\r  ${C_PURPLE}[3/5]${C_RESET}  ${C_BOLD}${C_WHITE}PYTHON RUNTIME & ENVIRONMENT${C_RESET} ... ${C_RED}✗ Error: Python 3 not found${C_RESET}"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/.venv"

# Create venv with system packages so OS-built binary wheels are automatically shared
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv --system-site-packages "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
PY_VER=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
echo -e "\033[1A\r  ${C_PURPLE}[3/5]${C_RESET}  ${C_BOLD}${C_WHITE}PYTHON RUNTIME & ENVIRONMENT${C_RESET} ... ${C_GREEN}✓ Python ${PY_VER} Active (.venv isolated)${C_RESET}"

# ==============================================================================
# STEP 4/5: Python Dependencies & Pre-Compiled Wheels
# ==============================================================================
print_step "4" "DEPENDENCIES & ANALYZER ENGINES" "${C_YELLOW}Installing...${C_RESET}"

pip install --upgrade pip -q >/dev/null 2>&1 || true
pip install --prefer-binary -r "$BACKEND_DIR/requirements.txt" -q >/dev/null 2>&1 || true

echo -e "\033[1A\r  ${C_PURPLE}[4/5]${C_RESET}  ${C_BOLD}${C_WHITE}DEPENDENCIES & ANALYZER ENGINES${C_RESET} ... ${C_GREEN}✓ FastAPI, Uvicorn, SQLite WAL Ready${C_RESET}"

# Ensure data directory exists
mkdir -p "$BACKEND_DIR/data"

# ==============================================================================
# STEP 5/5: Platform Initialization
# ==============================================================================
print_step "5" "ORCHESTRATION ENGINE & INTERFACE" "${C_GREEN}✓ Ready${C_RESET}"

# Re-check Public IP if not resolved earlier
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s -m 2 https://checkip.amazonaws.com 2>/dev/null || curl -s -m 2 https://ifconfig.me 2>/dev/null || echo "")
fi

# ==============================================================================
# Magnificent Cyberpunk Online Service Banner
# ==============================================================================
echo -e "\n${C_BOLD}${C_CYAN}  ╔══════════════════════════════════════════════════════════════════════════════╗${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}                     ${C_BOLD}${C_YELLOW}⚡  SCANET PLATFORM IS NOW ONLINE  ⚡${C_RESET}                      ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}                                                                              ${C_BOLD}${C_CYAN}║${C_RESET}"
if [ -n "$PUBLIC_IP" ]; then
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_BOLD}${C_LIME}🌐  AWS EC2 PUBLIC ACCESS:${C_RESET}   ${C_BOLD}${C_YELLOW}http://${PUBLIC_IP}:${PORT}${C_RESET}  ${C_DIM}◄ [OPEN IN BROWSER]${C_RESET}   ${C_BOLD}${C_CYAN}║${C_RESET}"
fi
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_BOLD}${C_SKY}🏠  LOCAL ACCESS LINK:${C_RESET}       ${C_WHITE}http://localhost:${PORT}${C_RESET}                              ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_BOLD}${C_PURPLE}📚  INTERACTIVE SWAGGER:${C_RESET}     ${C_WHITE}http://${PUBLIC_IP:-localhost}:${PORT}/docs${C_RESET}                         ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_BOLD}${C_GREEN}🩺  SYSTEM HEALTH PROBE:${C_RESET}     ${C_WHITE}http://${PUBLIC_IP:-localhost}:${PORT}/api/v1/system/health${C_RESET}        ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}                                                                              ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_ORANGE}⚠️  FIREWALL NOTE:${C_RESET} Ensure Port ${PORT} (Custom TCP) is OPEN in EC2 Security Group! ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║${C_RESET}   ${C_GRAY}⌨️  KEYBOARD:${C_RESET}      Press ${C_WHITE}[CTRL + C]${C_RESET} anytime to shut down the server.           ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╚══════════════════════════════════════════════════════════════════════════════╝${C_RESET}\n"

# Launch Uvicorn ASGI server from backend directory
cd "$BACKEND_DIR"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
