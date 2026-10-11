#!/usr/bin/env bash
# ==============================================================================
# scanet — Unified High-Impact Launcher (Linux / AWS EC2 / macOS)
# Cloned? Just execute: ./run.sh
# ==============================================================================
set -e

# Trap signals to ensure terminal cursor is always restored
trap 'printf "\033[?25h" 2>/dev/null || true' INT TERM EXIT

# ==============================================================================
# Cyberpunk High-Contrast Color Palette (256-Color & ANSI Supported)
# ==============================================================================
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_DIM="\033[2m"
C_UNDERLINE="\033[4m"

# Vivid Neon Accents
C_CYAN="\033[38;5;51m"
C_SKY="\033[38;5;45m"
C_BLUE="\033[38;5;39m"
C_PURPLE="\033[38;5;141m"
C_MAGENTA="\033[38;5;201m"
C_PINK="\033[38;5;213m"
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
# Cyberpunk Multi-Color Gradient ASCII Banner
# ==============================================================================
echo ""
echo -e "${C_CYAN}   ███████╗ ██████╗ █████╗ ███╗   ██╗███████╗████████╗${C_RESET}"
echo -e "${C_SKY}   ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝${C_RESET}"
echo -e "${C_BLUE}   ███████╗██║     ███████║██╔██╗ ██║█████╗     ██║   ${C_RESET}"
echo -e "${C_PURPLE}   ╚════██║██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   ${C_RESET}"
echo -e "${C_MAGENTA}   ███████║╚██████╗██║  ██║██║ ╚████║███████╗   ██║   ${C_RESET}"
echo -e "${C_PINK}   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ${C_RESET}"
echo ""
echo -e "  ${C_PURPLE}⚡ WEB-ORCHESTRATED CYBERSECURITY RECONNAISSANCE PLATFORM${C_RESET}"
echo -e "  ${C_BLUE}🔒 12 Recon Engines · OS Fingerprinting · AI MITRE ATT&CK · SARIF v2.1${C_RESET}"
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
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Node Host:${C_RESET}       ${C_WHITE}${HOSTNAME_VAL}${C_RESET} (${ARCH_VAL}, ${CPU_COUNT} Cores)"
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Memory Pool:${C_RESET}     ${C_YELLOW}${TOTAL_MEM_MB} MB RAM${C_RESET} │ ${C_PURPLE}${TOTAL_SWAP_MB} MB Swap Shield${C_RESET}"
if [ -n "$PUBLIC_IP" ]; then
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Public IPv4:${C_RESET}     ${C_LIME}${PUBLIC_IP}${C_RESET} ${C_DIM}(AWS EC2 Cloud Node Detected)${C_RESET}"
else
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Public IPv4:${C_RESET}     ${C_GRAY}Private / Local Subnet${C_RESET}"
fi
echo -e "  ${C_WHITE}│${C_RESET}  ${C_SKY}• Target Port:${C_RESET}     ${C_CYAN}TCP ${PORT}${C_RESET} ${C_DIM}(HTTP Direct Access)${C_RESET}"
echo -e "  ${C_BOLD}${C_WHITE}╰─────────────────────────────────────────────────────────────────────────────╯${C_RESET}\n"

# ==============================================================================
# Interactive Control Panel (Automatic 3-second non-blocking countdown)
# ==============================================================================
if [ -t 0 ] && [ "${SCANET_NON_INTERACTIVE:-0}" != "1" ]; then
    echo -e "  ${C_BOLD}${C_WHITE}╭─── 🎮 INTERACTIVE CONTROL ───────────────────────────────────────────────────╮${C_RESET}"
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_CYAN}[1]${C_RESET} ${C_BOLD}🚀 Launch Web Platform${C_RESET} ${C_DIM}(Default - Auto-launching in 3s...)${C_RESET}                       ${C_WHITE}│${C_RESET}"
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_YELLOW}[2]${C_RESET} ${C_BOLD}🔧 Change HTTP Port${C_RESET}    ${C_DIM}(Current: TCP ${PORT})${C_RESET}                                      ${C_WHITE}│${C_RESET}"
    echo -e "  ${C_WHITE}│${C_RESET}  ${C_PURPLE}[3]${C_RESET} ${C_BOLD}🩺 Self-Diagnostics${C_RESET}    ${C_DIM}(System resources & network interfaces)${C_RESET}              ${C_WHITE}│${C_RESET}"
    echo -e "  ${C_BOLD}${C_WHITE}╰─────────────────────────────────────────────────────────────────────────────╯${C_RESET}"
    echo -en "  ${C_SKY}Select option [1-3] or press [ENTER] to continue:${C_RESET} "

    read -t 3 USER_CHOICE || true
    echo ""

    if [ "$USER_CHOICE" = "2" ]; then
        echo -en "  ${C_YELLOW}Enter custom HTTP port [default: 8000]:${C_RESET} "
        read -r CUSTOM_PORT || true
        if [ -n "$CUSTOM_PORT" ] && [[ "$CUSTOM_PORT" =~ ^[0-9]+$ ]]; then
            PORT="$CUSTOM_PORT"
            echo -e "  ${C_GREEN}✓ Port updated to ${PORT}${C_RESET}\n"
        fi
    elif [ "$USER_CHOICE" = "3" ]; then
        echo -e "  ${C_SKY}--- RUNNING SELF-DIAGNOSTICS ---${C_RESET}"
        echo -e "  ${C_DIM}Disk Space:${C_RESET} $(df -h . | awk 'NR==2 {print $4 " available on " $1}')"
        echo -e "  ${C_DIM}Memory:${C_RESET}     $(free -h 2>/dev/null | awk '/^Mem:/{print $3 " used / " $2 " total"}' || echo 'N/A')"
        echo -e "  ${C_DIM}Cores:${C_RESET}      $(nproc 2>/dev/null || echo '1') cores"
        echo -e "  ${C_GREEN}✓ Diagnostics completed.${C_RESET}\n"
    fi
fi

# ==============================================================================
# Professional Animated Progress Spinner
# ==============================================================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/.venv"
SETUP_LOG="/tmp/scanet_setup.log"
: > "$SETUP_LOG"

SUDO=""
if [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
fi

run_with_spinner() {
    local step_idx="$1"
    local total_steps="$2"
    local task_title="$3"
    local logfile="$4"
    shift 4

    # Run target command in background with full output redirected to logfile
    "$@" >> "$logfile" 2>&1 &
    local cmd_pid=$!

    local spin_chars=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local idx=0
    local start_ts
    start_ts=$(date +%s 2>/dev/null || echo "0")

    # Hide terminal cursor during execution
    printf "\033[?25l" 2>/dev/null || true

    while kill -0 "$cmd_pid" 2>/dev/null; do
        local now_ts
        now_ts=$(date +%s 2>/dev/null || echo "0")
        local elapsed=$(( now_ts - start_ts ))
        local char="${spin_chars[$idx]}"
        printf "\r  ${C_PURPLE}[%s/%s]${C_RESET} %s  ${C_BOLD}${C_WHITE}%-34s${C_RESET} ${C_YELLOW}Working...${C_RESET} ${C_DIM}(%ds)${C_RESET}   " "$step_idx" "$total_steps" "$char" "$task_title" "$elapsed"
        idx=$(( (idx + 1) % ${#spin_chars[@]} ))
        sleep 0.12
    done

    # Restore cursor
    printf "\033[?25h" 2>/dev/null || true

    wait "$cmd_pid"
    local exit_code=$?
    local end_ts
    end_ts=$(date +%s 2>/dev/null || echo "0")
    local total_elapsed=$(( end_ts - start_ts ))

    if [ "$exit_code" -eq 0 ]; then
        printf "\r  ${C_PURPLE}[%s/%s]${C_RESET} ${C_GREEN}✓${C_RESET}  ${C_BOLD}${C_WHITE}%-34s${C_RESET} ${C_GREEN}✓ Done${C_RESET} ${C_DIM}(%ds)${C_RESET}                 \n" "$step_idx" "$total_steps" "$task_title" "$total_elapsed"
    else
        printf "\r  ${C_PURPLE}[%s/%s]${C_RESET} ${C_RED}✗${C_RESET}  ${C_BOLD}${C_WHITE}%-34s${C_RESET} ${C_RED}✗ Attention Needed${C_RESET} ${C_DIM}(%ds)${C_RESET}   \n" "$step_idx" "$total_steps" "$task_title" "$total_elapsed"
        echo -e "      ${C_YELLOW}Log excerpt (${logfile}):${C_RESET}"
        tail -n 8 "$logfile" 2>/dev/null | sed 's/^/      /'
    fi
    return "$exit_code"
}

# ==============================================================================
# STEP 1/5: System Package Update & Upgrade
# ==============================================================================
step1_update_packages() {
    if [ "${SKIP_SYSTEM_UPDATE:-0}" = "1" ]; then
        return 0
    fi
    export DEBIAN_FRONTEND=noninteractive
    if command -v apt-get >/dev/null 2>&1; then
        $SUDO apt-get update -y -q
        $SUDO apt-get upgrade -y -q -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
        $SUDO apt-get install -y -q python3 python3-pip python3-venv python3-pydantic python3-psutil git curl nmap mtr-tiny || \
        $SUDO apt-get install -y -q python3 python3-pip python3-venv git curl nmap mtr-tiny
    elif command -v dnf >/dev/null 2>&1; then
        $SUDO dnf upgrade -y -q
        $SUDO dnf install -y -q python3 python3-pip python3-psutil git curl nmap
    elif command -v yum >/dev/null 2>&1; then
        $SUDO yum update -y -q
        $SUDO yum install -y -q python3 python3-pip python3-psutil git curl nmap
    fi
}
run_with_spinner "1" "5" "SYSTEM REPOSITORIES & UPGRADE" "$SETUP_LOG" step1_update_packages

# ==============================================================================
# STEP 2/5: Low-Memory OOM Guard (Swap)
# ==============================================================================
step2_configure_swap() {
    if command -v free >/dev/null 2>&1; then
        local mem_int=$(free -m | awk '/^Mem:/{print $2}')
        local swap_int=$(free -m | awk '/^Swap:/{print $2}')
        if [ "${swap_int:-0}" -lt 500 ] && [ "${mem_int:-2048}" -lt 2500 ]; then
            if [ ! -f /swapfile ]; then
                $SUDO fallocate -l 2G /swapfile 2>/dev/null || $SUDO dd if=/dev/zero of=/swapfile bs=1M count=2048
                $SUDO chmod 600 /swapfile
                $SUDO mkswap /swapfile
            fi
            $SUDO swapon /swapfile 2>/dev/null || true
        fi
    fi
}
run_with_spinner "2" "5" "MEMORY SHIELD (2GB SWAP)" "$SETUP_LOG" step2_configure_swap

# ==============================================================================
# STEP 3/5: Python Runtime & Isolated Virtual Environment
# ==============================================================================
step3_setup_python() {
    local py_bin="python3"
    if ! command -v python3 >/dev/null 2>&1; then
        py_bin="python"
    fi
    if [ ! -d "$VENV_DIR" ]; then
        $py_bin -m venv --system-site-packages "$VENV_DIR"
    fi
}
run_with_spinner "3" "5" "PYTHON RUNTIME & VENV" "$SETUP_LOG" step3_setup_python

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# ==============================================================================
# STEP 4/5: Python Dependencies & Analyzer Modules
# ==============================================================================
step4_install_dependencies() {
    pip install --upgrade pip -q
    pip install --prefer-binary -r "$BACKEND_DIR/requirements.txt" -q
}
run_with_spinner "4" "5" "FASTAPI & RECON ENGINES" "$SETUP_LOG" step4_install_dependencies

# ==============================================================================
# STEP 5/5: Data Storage & Platform Verification
# ==============================================================================
step5_verify_platform() {
    mkdir -p "$BACKEND_DIR/data"
    cd "$BACKEND_DIR"
    python -c "import fastapi, uvicorn, sqlalchemy; from database.connection import init_db; import asyncio; asyncio.run(init_db())"
}
run_with_spinner "5" "5" "DATA STORE & ORCHESTRATION" "$SETUP_LOG" step5_verify_platform

# Re-check Public IP if not resolved earlier
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s -m 2 https://checkip.amazonaws.com 2>/dev/null || curl -s -m 2 https://ifconfig.me 2>/dev/null || echo "")
fi

# ==============================================================================
# Magnificent Cyberpunk Online Service Banner
# ==============================================================================
echo -e "\n${C_BOLD}${C_CYAN}  ╔══════════════════════════════════════════════════════════════════════════════╗${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}                     ${C_BOLD}${C_YELLOW}⚡  SCANET PLATFORM IS NOW ONLINE  ⚡{C_RESET}                      ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}                   ${C_LIME}Status: ● LIVE & LISTENING ON 0.0.0.0${C_RESET}                      ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}                                                                              ${C_BOLD}${C_CYAN}║${C_RESET}"
if [ -n "$PUBLIC_IP" ]; then
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_BOLD}${C_LIME}🌐  AWS EC2 PUBLIC ACCESS:${C_RESET}   ${C_BOLD}${C_YELLOW}http://${PUBLIC_IP}:${PORT}${C_RESET}  ${C_DIM}◄ [OPEN IN BROWSER]${C_RESET}   ${C_BOLD}${C_CYAN}║${C_RESET}"
fi
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_BOLD}${C_SKY}🏠  LOCAL ACCESS LINK:${C_RESET}       ${C_WHITE}http://localhost:${PORT}${C_RESET}                              ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_BOLD}${C_PURPLE}📚  INTERACTIVE SWAGGER:${C_RESET}     ${C_WHITE}http://${PUBLIC_IP:-localhost}:${PORT}/docs${C_RESET}                         ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_BOLD}${C_GREEN}🩺  SYSTEM HEALTH PROBE:${C_RESET}     ${C_WHITE}http://${PUBLIC_IP:-localhost}:${PORT}/api/v1/system/health${C_RESET}        ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}                                                                              ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_ORANGE}⚠️  FIREWALL NOTE:${C_RESET} Ensure Port ${PORT} (Custom TCP) is OPEN in EC2 Security Group! ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ║{C_RESET}   ${C_GRAY}⌨️  KEYBOARD:${C_RESET}      Press ${C_WHITE}[CTRL + C]${C_RESET} anytime to shut down the server.           ${C_BOLD}${C_CYAN}║${C_RESET}"
echo -e "${C_BOLD}${C_CYAN}  ╚══════════════════════════════════════════════════════════════════════════════╝${C_RESET}\n"

# Launch Uvicorn ASGI server from backend directory
cd "$BACKEND_DIR"
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
