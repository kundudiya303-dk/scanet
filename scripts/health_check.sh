#!/usr/bin/env bash
# =============================================================================
# scanet — Health Check Script
# Verifies all required and optional tools are correctly installed.
# =============================================================================
set -euo pipefail

BIN_DIR="/opt/scanet/bin"
PASS=0; FAIL=0; WARN=0

check_tool() {
    local TOOL="$1"
    local REQUIRED="$2"
    local PATH_CHECK="${BIN_DIR}/${TOOL}"
    if command -v "${TOOL}" &>/dev/null || [ -x "${PATH_CHECK}" ]; then
        VERSION=$(${TOOL} --version 2>&1 | head -n1 || echo "version unknown")
        echo "  ✅ ${TOOL}: ${VERSION}"
        ((PASS++))
    else
        if [ "${REQUIRED}" = "required" ]; then
            echo "  ❌ ${TOOL}: NOT FOUND (required)"
            ((FAIL++))
        else
            echo "  ⚠️  ${TOOL}: NOT FOUND (optional)"
            ((WARN++))
        fi
    fi
}

echo "=========================================="
echo "  scanet Health Check"
echo "=========================================="
echo ""
echo "── Tier 1 Core Tools (Required) ──"
check_tool "nmap"      "required"
check_tool "mtr"       "required"
check_tool "curl"      "required"
check_tool "dig"       "required"
check_tool "naabu"     "required"
check_tool "httpx"     "required"
check_tool "dnsx"      "required"
check_tool "subfinder" "required"
check_tool "ffuf"      "required"

echo ""
echo "── Tier 2 Extended Tools (Optional) ──"
check_tool "nuclei"    "optional"
check_tool "whatweb"   "optional"
check_tool "gobuster"  "optional"

echo ""
echo "── Python Environment ──"
if python3 -c "import fastapi, uvicorn, sqlalchemy" &>/dev/null; then
    echo "  ✅ Python packages: fastapi, uvicorn, sqlalchemy OK"
    ((PASS++))
else
    echo "  ❌ Python packages missing — run: pip install -r backend/requirements.txt"
    ((FAIL++))
fi

echo ""
echo "=========================================="
echo "  Results: ✅ ${PASS} passed  ❌ ${FAIL} failed  ⚠️  ${WARN} optional missing"
echo "=========================================="
[ "${FAIL}" -eq 0 ] && exit 0 || exit 1
