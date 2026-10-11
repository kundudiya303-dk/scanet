# scanet — Tool Integration Matrix & Status Registry

**Comprehensive Security Tool & Analyzer Registry**  
*Maintained under Phase 2: Deep Research & Extended Tool Universe*

---

## 1. Tool Implementation Matrix

| Tool Name | Category | Tier | Implementation Status | Adapter Location | Output Normalization | Verification Status |
|---|---|---|---|---|---|---|
| **Nmap** | Port Scanning & Services | **Tier 1 (Core)** | **Implemented** | `backend/adapters/nmap_adapter.py` | XML to JSON via `defusedxml` | Tested |
| **Naabu** | Fast Port Discovery | **Tier 1 (Core)** | **Implemented** | `backend/adapters/naabu_adapter.py` | Streaming JSON Lines | Tested |
| **RustScan** | Ultra-Fast Adaptive Port Scan | **Tier 2 (Ext)** | **Implemented** | `backend/adapters/rustscan_adapter.py` | Clean Bracket & Host Regex | Tested |
| **FFUF** | Web Directory Fuzzing | **Tier 1 (Core)** | **Implemented** | `backend/adapters/ffuf_adapter.py` | Native JSON (`-of json`) | Tested |
| **Gobuster** | Academic Directory Fuzzing | **Tier 1 (Core)** | **Implemented** | `backend/adapters/gobuster_adapter.py` | Regex Normalized Routes | Tested |
| **Katana** | Next-Gen Web Crawler & APIs | **Tier 1 (Core)** | **Implemented** | `backend/adapters/katana_adapter.py` | Structured JSONL Endpoints | Tested |
| **dnsx** | DNS Analysis & Resolution | **Tier 1 (Core)** | **Implemented** | `backend/adapters/dnsx_adapter.py` | Streaming JSON Lines | Tested |
| **Subfinder** | Passive Subdomain Discovery | **Tier 1 (Core)** | **Implemented** | `backend/adapters/subfinder_adapter.py` | Streaming JSON Lines | Tested |
| **HTTPX** | HTTP Surface Inspection | **Tier 1 (Core)** | **Implemented** | `backend/adapters/httpx_adapter.py` | Streaming JSON Lines | Tested |
| **Nuclei** | Vulnerability & Misconfig Audit | **Tier 1 (Core)** | **Implemented** | `backend/adapters/nuclei_adapter.py` | JSONL Findings & CVSS Scores | Tested |
| **MTR** | Hop-by-Hop Network Path | **Tier 1 (Core)** | **Implemented** | `backend/adapters/mtr_adapter.py` | Native JSON (`--json`) | Tested |
| **Passive OSINT** | Geolocation, ASN & crt.sh | **Tier 1 (Native)**| **Implemented** | `backend/adapters/osint_adapter.py` | Async JSON Dict | Tested |
| **Native Headers** | HTTP Security Header Audit | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/headers.py` | Letter Grade (A+ to F) | Tested |
| **Native SSL** | Certificate Chain & Expiry | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/ssl_cert.py` | Direct Cert Model JSON | Tested |
| **Native Subnet** | CIDR Math & Subnet Info | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/subnet.py` | Built-in IP Math Dict | Tested |
| **Scan Diff** | Asset Drift & Port Drift | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/diff.py` | Delta JSON (Added/Removed) | Tested |
| **CVE Correlator** | CPE to CVE & CISA KEV | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/cve_correlator.py`| Known Exploit Records | Tested |
| **AI Advisor** | MITRE ATT&CK & Remediation | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/ai_advisor.py` | Expert Heuristic Scoring | Tested |
| **Compliance Mapper**| OWASP Top 10 & CIS Controls| **Tier 1 (Native)**| **Implemented** | `backend/analyzers/compliance.py` | Audit Matrix Dict | Tested |
| **SARIF Exporter** | DevSecOps / GitHub Security | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/sarif_exporter.py`| OASIS SARIF v2.1.0 JSON | Tested |
| **Webhook Notifier**| Discord, Slack & Webhooks | **Tier 1 (Native)**| **Implemented** | `backend/analyzers/webhook_notifier.py`| Real-time HTTP Dispatch | Tested |
| **Pipelines Manager**| Multi-Tool Orchestration | **Tier 1 (Engine)**| **Implemented** | `backend/engine/pipeline_manager.py`| Chained Stage Execution | Tested |

---

## 2. Multi-Stage Pipeline Playbooks

| Playbook Name | Tools Chained in Sequence | Target Profile | Execution Mode |
|---|---|---|---|
| **Full Recon Pipeline** | `subfinder` ➔ `dnsx` ➔ `naabu` ➔ `nmap` ➔ `httpx` ➔ `nuclei` | Full External Surface | Sequential Chained |
| **Web Security Audit** | `katana` ➔ `ffuf` ➔ `httpx` ➔ `nuclei` | Web Applications & APIs | Sequential Chained |
| **Network Diagnostics**| `mtr` ➔ `naabu` ➔ `nmap` ➔ `subnet` | Subnet & Host Routing | Sequential Chained |
| **Passive OSINT** | `subfinder` ➔ `crt.sh` ➔ `ip-api` ➔ `rdap` | 100% Passive Discovery | Async Parallel |

---

## 3. Status Definitions
- **Implemented:** Code fully implemented with structured command building and parsing.
- **Tested:** Tested against syntax, interfaces, and expected output schemas.
- **Production Ready:** Actively wired to backend routers and UI dashboards.
