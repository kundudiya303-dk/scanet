#!/usr/bin/env bash
# =============================================================================
# scanet — Main Installation Script
# Installs system dependencies, Python virtual environment,
# and downloads static Go/Rust tool binaries for the detected architecture.
#
# Supported: Ubuntu 22.04+, Debian 11+, Kali Linux, Amazon Linux 2023, Fedora
# Architecture: x86_64 (amd64), aarch64 (arm64)
# Usage: chmod +x install.sh && ./install.sh
# =============================================================================
set -euo pipefail

SCANET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="/opt/scanet/bin"
VENV_DIR="${SCANET_DIR}/backend/.venv"
ARCH="$(uname -m)"

# Normalize architecture naming
case "${ARCH}" in
    x86_64)  TOOL_ARCH="amd64" ;;
    aarch64) TOOL_ARCH="arm64" ;;
    *)       echo "❌ Unsupported architecture: ${ARCH}"; exit 1 ;;
esac

echo "=========================================="
echo "  scanet Installation"
echo "  Architecture: ${ARCH} (${TOOL_ARCH})"
echo "=========================================="

# ── Detect package manager ──────────────────────────────────────────────────
if command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt"
    sudo apt-get update -qq
    sudo apt-get install -y nmap mtr python3 python3-pip python3-venv curl wget
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
    sudo dnf install -y nmap mtr python3 python3-pip curl wget
elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
    sudo pacman -Sy --noconfirm nmap mtr python python-pip curl wget
else
    echo "⚠️  Unknown package manager. Install nmap, mtr, python3, curl, wget manually."
fi
echo "✅ System packages installed."

# ── Create /opt/scanet/bin ──────────────────────────────────────────────────
sudo mkdir -p "${BIN_DIR}"
sudo chmod 755 "${BIN_DIR}"

# ── Download ProjectDiscovery Go binaries ───────────────────────────────────
download_pd_tool() {
    local TOOL="$1"
    local VERSION="$2"
    local URL="https://github.com/projectdiscovery/${TOOL}/releases/download/${VERSION}/${TOOL}_${VERSION#v}_linux_${TOOL_ARCH}.zip"
    echo "⬇️  Downloading ${TOOL} ${VERSION}..."
    wget -qO "/tmp/${TOOL}.zip" "${URL}" && \
        sudo unzip -qo "/tmp/${TOOL}.zip" "${TOOL}" -d "${BIN_DIR}" && \
        sudo chmod +x "${BIN_DIR}/${TOOL}" && \
        rm -f "/tmp/${TOOL}.zip" && \
        echo "✅ ${TOOL} installed at ${BIN_DIR}/${TOOL}" || \
        echo "⚠️  Failed to install ${TOOL} — skipping"
}

download_pd_tool "naabu"     "v2.3.1"
download_pd_tool "httpx"     "v1.6.9"
download_pd_tool "dnsx"      "v1.2.0"
download_pd_tool "subfinder" "v2.6.7"
download_pd_tool "nuclei"    "v3.3.0"

# ── Download FFUF ───────────────────────────────────────────────────────────
echo "⬇️  Downloading ffuf..."
FFUF_VERSION="v2.1.0"
FFUF_URL="https://github.com/ffuf/ffuf/releases/download/${FFUF_VERSION}/ffuf_${FFUF_VERSION#v}_linux_${TOOL_ARCH}.tar.gz"
wget -qO "/tmp/ffuf.tar.gz" "${FFUF_URL}" && \
    sudo tar -xzf "/tmp/ffuf.tar.gz" -C "${BIN_DIR}" ffuf && \
    sudo chmod +x "${BIN_DIR}/ffuf" && \
    rm -f "/tmp/ffuf.tar.gz" && \
    echo "✅ ffuf installed" || echo "⚠️  Failed to install ffuf — skipping"

# ── Add /opt/scanet/bin to PATH ─────────────────────────────────────────────
if ! grep -q "/opt/scanet/bin" ~/.bashrc 2>/dev/null; then
    echo 'export PATH="/opt/scanet/bin:$PATH"' >> ~/.bashrc
    echo "✅ Added /opt/scanet/bin to PATH"
fi

# ── Python virtual environment ──────────────────────────────────────────────
echo "🐍 Creating Python virtual environment..."
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "${SCANET_DIR}/backend/requirements.txt"
echo "✅ Python environment ready at ${VENV_DIR}"

# ── Create data directory ────────────────────────────────────────────────────
mkdir -p "${SCANET_DIR}/backend/data"
echo "✅ Data directory created."

echo ""
echo "=========================================="
echo "  scanet Installation Complete!"
echo "  Run: ./scripts/health_check.sh to verify"
echo "  Start: cd backend && source .venv/bin/activate && uvicorn main:app --reload"
echo "=========================================="
