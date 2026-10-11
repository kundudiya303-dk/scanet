# scanet: Master Architecture, Research & Engineering Blueprint
**Lightweight, Modular, Web-Orchestrated Cybersecurity Reconnaissance & Diagnostic Platform**  
*Academic Project Specification | Designed for University Labs, Virtual Environments & Cloud Nodes*

---

## 1. Executive Summary & Vision

**scanet** is a lightweight, modular, interactive web-based cybersecurity platform designed to consolidate essential network discovery, web reconnaissance, DNS analysis, HTTP inspection, and educational security assessment utilities into a single unified graphical dashboard. 

In university environments and cybersecurity training laboratories, students and researchers frequently navigate a fragmented landscape of command-line tools. Standard enterprise solutions (e.g., Greenbone Vulnerability Management, Tenable Nessus, full OWASP ZAP desktop suites) are often too heavyweight for resource-constrained lab environments, consuming gigabytes of RAM and requiring complex multi-service infrastructure.

`scanet` solves this problem by prioritizing:
1. **Lightweight Resource Footprint:** Capable of running smoothly on low-resource virtual machines and burstable cloud instances (e.g., 1–2 vCPU, 1–2 GB RAM, including AWS `t4g.micro` and `t3.micro`).
2. **Modular Tool Adapters:** An extensible abstraction layer where tools (Nmap, Naabu, FFUF, dnsx, HTTPX, etc.) are encapsulated in isolated Python adapters.
3. **Strict Lab Scope & Safety Guardrails:** Programmatic enforcement of target permissions, preventing scans against unauthorized external systems, cloud metadata services (`169.254.169.254`), and loopback addresses.
4. **Normalized Results Schema:** Translation of heterogeneous tool outputs (XML, line-delimited JSON, raw text) into unified JSON models for visualization, comparison, and reporting.
5. **Real-Time Job Control:** Live process output streaming via Server-Sent Events (SSE) and deterministic process-group termination (`SIGTERM`/`SIGKILL`).

---

## 2. Project Scope, Lab Assumptions & Ethical Guardrails

### 2.1 Target Audience and Academic Context
* **Undergraduate & Graduate Cyber Defense Courses:** Hands-on instruction in port scanning, DNS resolution, banner grabbing, and HTTP security headers.
* **Controlled University Labs:** Auditing designated local subnet ranges (RFC 1918) and intentionally vulnerable target machines (e.g., OWASP Juice Shop, DVWA, Metasploitable).
* **Research & Benchmarking:** Reproducible comparisons of scan duration, packet overhead, and accuracy across scanning engines.

### 2.2 Strict Ethical & Operational Boundaries
* **Authorized Target Enforcement:** Scans can only be launched against targets explicitly verified and registered in the Target & Scope Manager.
* **Non-Goals (Out of Scope):**
  * Automated exploitation, shellcode delivery, and credential brute-forcing are strictly excluded.
  * Denial-of-Service (DoS) and flood-based scanning (e.g., unthrottled Masscan) are excluded.
  * Evasion and obfuscation techniques are omitted to prioritize defensive transparency.

---

## 3. Functional and Non-Functional Requirements

### 3.1 Functional Requirements (FR)
* **FR-01 (Scope Management):** Whitelist validation for IP addresses, CIDR blocks, and hostnames before scan initiation.
* **FR-02 (Modular Tool Orchestration):** Parametrized execution of CLI security tools using structured argument arrays (`execve` safe process invocation).
* **FR-03 (Real-Time Job Monitoring):** Live progress streaming, execution elapsed timers, and live console output via Server-Sent Events (SSE).
* **FR-04 (Deterministic Cancellation):** Reliable cancellation of active child and grandchild processes via Linux process groups (`os.killpg`).
* **FR-05 (Unified Data Normalization):** Ingestion and translation of tool outputs into structured models (Hosts, Ports, Services, Routes, DNS Records, Findings).
* **FR-06 (Automated Security Scoring):** Heuristic evaluation of HTTP security headers, TLS configuration, and exposed surface areas.
* **FR-07 (Reporting & Export):** Multi-format reporting (Executive PDF, Technical HTML, JSON, CSV, and SARIF for academic evaluation).
* **FR-08 (Tool Availability Auditing):** Startup checks detecting binary availability in system `$PATH` and displaying installation status.

### 3.2 Non-Functional Requirements (NFR)
* **NFR-01 (Memory Efficiency):** Idle system memory consumption $\le 120\text{ MB}$; peak memory with 2 concurrent scans $\le 650\text{ MB}$.
* **NFR-02 (CPU Throttling):** Enforced rate limits and concurrency caps to prevent starving single-core virtual machines.
* **NFR-03 (Cross-Architecture Portability):** Zero-code-change execution on both `x86_64` (AMD64) and `aarch64` (ARM64 / Apple Silicon / AWS Graviton).
* **NFR-04 (Zero Shell Injection):** Zero usage of `shell=True` or raw shell string concatenation in process management.
* **NFR-05 (Self-Contained Deployment):** Operable as a standalone Python virtual environment or minimal Docker container without external message broker daemons (no Celery, Redis, or RabbitMQ required for base operations).

---

## 4. Comprehensive Tool Catalogue & Comparison

### 4.1 Network Discovery & Port Scanning

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nmap** | C/C++ | Non-root (`-sT`) / Root (`-sS`, `-sU`) | $0\text{ MB}$ / $35\text{–}65\text{ MB}$ | XML (`-oX`) | Low (Parsed via `defusedxml`) | **Tier 1 (Core Engine):** Standard for deep service versioning and OS fingerprinting. |
| **Naabu** | Go | Non-root fallback / Root for SYN | $0\text{ MB}$ / $25\text{–}50\text{ MB}$ | JSON lines (`-json`) | Very Low | **Tier 1 (Fast Discovery):** High-speed multi-port screening; outputs pipeable to Nmap. |
| **RustScan** | Rust | Non-root (TCP Connect) | $0\text{ MB}$ / $15\text{–}40\text{ MB}$ | Text output | Medium (Regex parsing) | **Tier 2:** Rapid port discovery, but delegates service analysis to Nmap. |
| **Masscan** | C | **Root Mandatory (`CAP_NET_RAW`)** | $0\text{ MB}$ / $40\text{–}90\text{ MB}$ | JSON / XML | High | **Tier 3 (Excluded):** Bypasses kernel TCP stack; high risk of flooding lab switches or triggering cloud abuse flags. |
| **Netcat (nc)** | C | Non-root | $0\text{ MB}$ / $< 5\text{ MB}$ | Raw text | Low | **Tier 1 (Native Utility):** Single-port reachability and raw banner grabbing. |

### 4.2 Web Content & Directory Discovery

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FFUF** | Go | Non-root | $0\text{ MB}$ / $30\text{–}75\text{ MB}$ | Native JSON (`-of json`) | Very Low | **Tier 1 (Primary Fuzzer):** Resource-efficient, highly configurable wordlist filtering and rate limiting. |
| **Gobuster** | Go | Non-root | $0\text{ MB}$ / $35\text{–}80\text{ MB}$ | Text / JSON | Low | **Tier 1 (Alternative):** Popular academic tool for directory and virtual host discovery. |
| **Feroxbuster**| Rust | Non-root | $0\text{ MB}$ / $70\text{–}180\text{ MB}$ | Streaming JSON (`--json`) | Low | **Tier 2:** Fast recursion, but deep recursion requires memory limits on small nodes. |
| **DirBuster** | Java | Non-root | $0\text{ MB}$ / $350\text{–}600\text{ MB}$ | Text | High (Heavy JVM) | **Tier 3 (Excluded):** Obsolete; requires full Java runtime environment. |
| **Dirb** | C | Non-root | $0\text{ MB}$ / $15\text{–}30\text{ MB}$ | Plaintext | Medium | **Tier 3 (Excluded):** Single-threaded, slow, and lacks structured output. |

### 4.3 DNS Discovery & Intelligence

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **dnsx** | Go | Non-root | $0\text{ MB}$ / $20\text{–}45\text{ MB}$ | JSON lines (`-json`) | Very Low | **Tier 1:** Active multi-record resolver (A, AAAA, CNAME, MX, TXT, PTR). |
| **Subfinder** | Go | Non-root | $0\text{ MB}$ / $25\text{–}50\text{ MB}$ | JSON lines (`-json`) | Very Low | **Tier 1:** Passive subdomain mapping without sending packets to target. |
| **Dig / Host** | C | Non-root | $0\text{ MB}$ / $< 5\text{ MB}$ | Text | Low | **Tier 1 (Built-in):** Precise query verification and AXFR zone transfer checks. |
| **OWASP Amass**| Go | Non-root | $0\text{ MB}$ / $1.0\text{–}2.5\text{ GB}$ | JSON / Graph DB | High | **Tier 3 (Excluded):** Heavy graph dependencies; causes Out-Of-Memory (OOM) crashes on low-resource VMs. |

### 4.4 HTTP Inspection & Technology Fingerprinting

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HTTPX** | Go | Non-root | $0\text{ MB}$ / $30\text{–}60\text{ MB}$ | JSON lines (`-json`) | Very Low | **Tier 1:** Comprehensive HTTP status, redirect chains, titles, TLS cert info, and WAF discovery. |
| **WhatWeb** | Ruby | Non-root | $0\text{ MB}$ / $60\text{–}120\text{ MB}$ | JSON (`--log-json`) | Medium | **Tier 2:** Deep tech fingerprinting; requires Ruby runtime. |
| **cURL** | C | Non-root | $0\text{ MB}$ / $< 10\text{ MB}$ | Raw Headers/Body | Low | **Tier 1 (Built-in):** Low-level header inspection and HTTP method probing (`OPTIONS`, `HEAD`). |

### 4.5 TLS & Cryptographic Auditing

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **testssl.sh** | Bash + OpenSSL | Non-root | $0\text{ MB}$ / $25\text{–}45\text{ MB}$ | JSON (`--jsonfile`) | Low | **Tier 2:** Cipher suite support, TLS 1.0–1.3 negotiation, Heartbleed/POODLE testing. |
| **SSLyze** | Python | Non-root | $0\text{ MB}$ / $80\text{–}120\text{ MB}$ | Native JSON | Medium | **Tier 2:** Cryptographic TLS probing via Python C-bindings. |
| **Native Python SSL**| Python | Non-root | $0\text{ MB}$ / $0\text{ MB}$ (Internal) | Native Dict | Very Low | **Tier 1 (Built-in):** Instant certificate chain, SAN, and expiry inspection in $< 100\text{ ms}$. |

### 4.6 Security Assessment & Diagnostics

| Tool | Language | Privilege Model | Idle / Active RAM | Output Format | Integration Complexity | Evaluation / Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nuclei** | Go | Non-root | $0\text{ MB}$ / $55\text{–}130\text{ MB}$ | JSON lines (`-json`) | Very Low | **Tier 2 (Curated Tags):** Targeted, non-destructive checks (`tags: ["misconfig", "exposure", "ssl"]`). |
| **Nikto** | Perl | Non-root | $0\text{ MB}$ / $40\text{–}85\text{ MB}$ | XML / JSON (limited) | Medium | **Tier 3 (Excluded):** Noisy, legacy tests with high false positive rates. |
| **OWASP ZAP** | Java | Non-root | $0\text{ MB}$ / $1.5\text{–}2.2\text{ GB}$ | REST API / JSON | High | **Tier 3 (Excluded):** Demands $\ge 2\text{ GB}$ dedicated RAM; crashes low-resource nodes. |
| **MTR** | C | Unprivileged UDP / Raw | $0\text{ MB}$ / $10\text{–}20\text{ MB}$ | JSON (`--json`) | Very Low | **Tier 1 (Diagnostic):** Network hop routing, latency, and packet loss visualization. |

---

## 5. Tool Tier Categorization

### Tier 1: Essential Bundle (Minimum Viable Product)
* **Port & Service Discovery:** `Naabu` (fast port discovery) + `Nmap` (unprivileged `-sT` deep service probe).
* **Web Discovery:** `FFUF` (directory/file fuzzing with rate limits).
* **DNS Intelligence:** `dnsx` (active resolution) + `Subfinder` (passive subdomain discovery).
* **HTTP Surface Inspection:** `HTTPX` (headers, title, redirect chains, TLS cert preview).
* **Network Diagnostics:** `MTR` (hop-by-hop latency and route inspection via `--json`).
* **Native Python Modules:** Built-in WHOIS/RDAP, Subnet Math, HTTP Security Headers Analyzer, robots/sitemap parser, and Scan Diff engine.

### Tier 2: Recommended Extensions (Milestone 2)
* **Cryptographic Health:** `testssl.sh` for in-depth TLS cipher and protocol compliance.
* **Controlled Assessment:** `Nuclei` using strictly non-intrusive configuration audit templates.
* **Technology Fingerprinting:** `WhatWeb` (optional containerized worker).
* **Alternative Web Discovery:** `Feroxbuster` (user-selectable engine).

### Tier 3: Excluded / Heavyweight Tools (Academic Rationale)
* **OWASP ZAP & Greenbone (OpenVAS):** Excluded due to excessive RAM requirements ($> 2\text{–}4\text{ GB}$), high initialization times, and heavy background daemon requirements.
* **Masscan:** Excluded due to raw-packet transmission hazards and root-privilege requirements that compromise container security.
* **DirBuster & Dirb:** Excluded because modern Go/Rust utilities provide superior performance, lower memory usage, and structured JSON output.

---

## 6. Linux Compatibility & Multi-Architecture Strategy

### 6.1 Distribution Support Matrix

| Linux Distribution | Version | x86_64 Support | ARM64 Support | Primary Installation Route |
| :--- | :--- | :---: | :---: | :--- |
| **Ubuntu LTS** | 22.04 / 24.04 | Full | Full | `apt` (Nmap, MTR, Python) + `/opt/scanet/bin/` (Go binaries) |
| **Debian Stable** | 11 / 12 | Full | Full | `apt` + `/opt/scanet/bin/` |
| **Kali Linux** | 2024.x | Full | Full | Native `apt` repository tools pre-configured |
| **Amazon Linux** | AL2023 | Full | Full | `dnf` + GitHub release static binaries |
| **Fedora** | 39 / 40 | Full | Full | `dnf` + `/opt/scanet/bin/` |

### 6.2 Binary Management & Portability Engine
1. **Self-Contained Binaries:** Go and Rust utilities are distributed as static binaries without shared library dependencies.
2. **Standard Install Directory:** Standalone binaries are stored in `/opt/scanet/bin/`, which is prepended to the worker subprocess `PATH`.
3. **Graceful Tool Degradation:**
   * On startup, the backend runs `shutil.which()` against all configured tool adapters.
   * If a tool is missing, the backend marks it as `UNAVAILABLE` in the system registry.
   * The web UI shows a disabled toggle with an informative tooltip and installation command, allowing the rest of the platform to function normally.

---

## 7. Cloud Deployment: AWS EC2 & Cost Models

### 7.1 Instance Sizing Comparison

| Instance | vCPU | RAM | Architecture | Estimated Monthly Cost (us-east-1) | Suitability |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`t4g.nano`** | 2 | 0.5 GB | ARM64 (Graviton2) | $\sim \$3.07$ | Educational demo; limited concurrency |
| **`t4g.micro`** | 2 | 1.0 GB | ARM64 (Graviton2) | $\sim \$6.13$ | **Recommended Production Value** |
| **`t4g.small`** | 2 | 2.0 GB | ARM64 (Graviton2) | $\sim \$12.26$ | Ideal for Tier 1 + Nuclei multi-user lab |
| **`t3.micro`** | 2 | 1.0 GB | x86_64 (Intel) | $\sim \$7.60$ | **AWS Free Tier Eligible** |
| **`t3.small`** | 2 | 2.0 GB | x86_64 (Intel) | $\sim \$15.18$ | Standard x86 lab environment |

### 7.2 Cloud Security & Hardening Controls
* **IMDSv2 Enforcement:** Require token-based AWS Instance Metadata Service (IMDSv2) with hop-limit set to 1 to block SSRF exfiltration of cloud credentials.
* **Network Security Groups:** Inbound access restricted strictly to port `443` (HTTPS) from authorized campus CIDR blocks. Administrative SSH restricted to campus VPNs.
* **Scanning Egress Policy:** Outbound scanning traffic allowed only to specified target lab IPs/VPCs, blocking outbound access to internet IP ranges where unauthorized.
* **Automatic Cost Controls:** CloudWatch alarms with automated EC2 stop actions if daily network egress or CPU utilization exceeds lab budget limits.

---

## 8. Expanded Features & Advanced Platform Options

Beyond basic tool wrappers, `scanet` includes the following educational and operational capabilities:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           scanet Unified Architecture                           │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │
     ┌───────────────────┬─────────────┴─────────────┬────────────────────┐
     ▼                   ▼                           ▼                    ▼
┌─────────────┐   ┌───────────────┐           ┌──────────────┐     ┌─────────────┐
│ Scope & RBAC│   │  Core Engine  │           │ Background   │     │ Normalized  │
│  Guardrail  │   │  & Adapters   │           │ Job Manager  │     │  Database   │
├─────────────┤   ├───────────────┤           ├──────────────┤     ├─────────────┤
│• Whitelist  │   │• Naabu / Nmap │           │• Process-grp │     │• Hosts      │
│• Cloud Block│   │• FFUF / HTTPX │           │  lifecycle   │     │• Ports/Svcs │
│• SSRF Shield│   │• dnsx / MTR   │           │• SSE Streams │     │• Findings   │
│• Multi-role │   │• Native PyMod │           │• SQLite Queue│     │• Audit Logs │
└─────────────┘   └───────────────┘           └──────────────┘     └─────────────┘
```

1. **Role-Based Access Control (RBAC):**
   * *Administrator:* Manages tool binaries, approved scopes, user accounts, and system limits.
   * *Instructor:* Configures lab target presets, views all student scan sessions, and exports grading reports.
   * *Student:* Executes scans against approved targets, inspects normalized results, and exports technical findings.
2. **Pre-Configured Educational Lab Profiles:**
   * Pre-packaged scan profiles for standard lab targets (e.g., "Web App Recon: Juice Shop", "Network Infrastructure Audit: Metasploitable").
3. **Interactive Target Network Topology Graph:**
   * Visual node graph (using Cytoscape.js or D3.js) displaying discovered hosts, open ports, identified web servers, and routing hops.
4. **Automated Security Header & SSL Grading:**
   * Automated report card (A+ to F) evaluating HTTP headers (`CSP`, `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`) and certificate validity.
5. **Scan Comparison & Asset Drift Tracker:**
   * Visual side-by-side diff highlighting new open ports, changed services, or decommissioned endpoints across scan dates.
6. **SARIF & Multi-Format Reporting:**
   * Export scan results in OASIS SARIF (Static Analysis Results Interchange Format) to integrate with modern security evaluation pipelines, alongside HTML, PDF, JSON, and CSV.
7. **Webhook Notifications:**
   * Automated dispatch of scan completion summaries to Discord, Slack, or generic HTTP webhooks for lab classroom coordination.

---

## 9. Technology Stack Selection & Justification

### 9.1 Architecture Comparison

| Architecture | Backend / Workers | Frontend | DB | Overhead | Development Speed | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: Python-first** | **FastAPI + Async Subprocesses** | **Modern Vanilla JS + CSS Tokens** | **SQLite (WAL)** | **$\sim 95\text{ MB}$ RAM** | **High** | **RECOMMENDED** |
| **Option B: Go-first** | Go HTTP + Goroutines | HTMX + Tailwind | SQLite | $\sim 50\text{ MB}$ RAM | Medium | Viable, but slower adapter development |
| **Option C: Heavy Distributed**| FastAPI + Celery + Redis | React + Next.js | PostgreSQL | $\sim 550\text{ MB}$ RAM | Slow | Excluded (Heavyweight infrastructure) |

### 9.2 The Recommended Stack: Python FastAPI + SQLite (WAL) + Modern Vanilla UI
* **Backend:** **Python 3.10+ with FastAPI and Uvicorn.** Provides native async I/O, fast startup, zero-overhead background job queues (`asyncio.subprocess`), and comprehensive libraries for network protocol parsing.
* **Database:** **SQLite with Write-Ahead Logging (WAL mode).** Zero-daemon configuration, single-file backups, concurrent read performance, and embedded JSON query support (`json_extract`).
* **Frontend:** **Modern Vanilla CSS & JavaScript (ES6+ Modules).** Zero Node.js build-step dependency at runtime, lightning-fast page loads, and native Server-Sent Events (`EventSource`) support.
* **Process Isolation:** Direct process execution via `asyncio.create_subprocess_exec()` using isolated process groups (`preexec_fn=os.setsid`).

---

## 10. Database Schema (SQLite WAL Mode)

```sql
-- 1. Authorized Targets & Scopes
CREATE TABLE targets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    target_value TEXT NOT NULL, -- Hostname, IP, or CIDR
    target_type TEXT NOT NULL,  -- 'ip', 'cidr', 'domain'
    is_approved INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT NOT NULL
);

-- 2. Scan Jobs
CREATE TABLE scan_jobs (
    id TEXT PRIMARY KEY,
    target_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    profile_name TEXT NOT NULL,
    status TEXT NOT NULL, -- 'queued', 'running', 'completed', 'failed', 'cancelled'
    parameters_json TEXT NOT NULL,
    pid INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    exit_code INTEGER,
    error_message TEXT,
    FOREIGN KEY(target_id) REFERENCES targets(id) ON DELETE CASCADE
);

-- 3. Normalized Findings: Hosts & Ports
CREATE TABLE normalized_hosts (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    hostname TEXT,
    os_fingerprint TEXT,
    status TEXT NOT NULL, -- 'up', 'down'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_id) REFERENCES scan_jobs(id) ON DELETE CASCADE
);

CREATE TABLE normalized_ports (
    id TEXT PRIMARY KEY,
    host_id TEXT NOT NULL,
    port_number INTEGER NOT NULL,
    protocol TEXT NOT NULL, -- 'tcp', 'udp'
    state TEXT NOT NULL,    -- 'open', 'filtered', 'closed'
    service_name TEXT,
    product TEXT,
    version TEXT,
    FOREIGN KEY(host_id) REFERENCES normalized_hosts(id) ON DELETE CASCADE
);

-- 4. Normalized Findings: Web Routes & Discovered Endpoints
CREATE TABLE normalized_endpoints (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    url TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    content_length INTEGER,
    title TEXT,
    tech_stack_json TEXT, -- Extracted technologies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_id) REFERENCES scan_jobs(id) ON DELETE CASCADE
);

-- 5. Normalized Findings: Security Issues & Configuration Warnings
CREATE TABLE normalized_findings (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    category TEXT NOT NULL, -- 'ssl', 'headers', 'misconfig', 'info'
    severity TEXT NOT NULL, -- 'info', 'low', 'medium', 'high'
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence TEXT,
    remediation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_id) REFERENCES scan_jobs(id) ON DELETE CASCADE
);

-- 6. Audit Logs
CREATE TABLE audit_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    details_json TEXT,
    ip_address TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 11. Backend API Design Specification

### 11.1 Target & Scope Endpoints
* `GET /api/v1/targets` — List all configured target assets and approval statuses.
* `POST /api/v1/targets` — Register a new authorized target (validates against private/lab scope whitelist).
* `DELETE /api/v1/targets/{id}` — De-register an authorized target.

### 11.2 Scan Job Orchestration Endpoints
* `POST /api/v1/jobs` — Queue a new scan job.
  * **Request Body:**
    ```json
    {
      "target_id": "tgt_01J8F3",
      "tool_name": "nmap",
      "profile": "service_detect",
      "parameters": {
        "ports": "top-100",
        "speed": 3
      }
    }
    ```
* `GET /api/v1/jobs` — Retrieve paginated job history.
* `GET /api/v1/jobs/{id}` — Retrieve detailed job status and configuration.
* `POST /api/v1/jobs/{id}/cancel` — Terminate an active job and its process group.
* `GET /api/v1/jobs/{id}/stream` — Server-Sent Events (SSE) endpoint streaming real-time console lines and completion status.

### 11.3 Results & Analytics Endpoints
* `GET /api/v1/results/hosts` — Query discovered hosts and services across jobs.
* `GET /api/v1/results/endpoints` — Query discovered HTTP endpoints, status codes, and titles.
* `GET /api/v1/results/diff` — Compare findings between two historical jobs (`job_a`, `job_b`).
* `GET /api/v1/results/export/{format}` — Download scan reports in `pdf`, `html`, `json`, `csv`, or `sarif`.

### 11.4 System Health & Configuration Endpoints
* `GET /api/v1/system/tools` — Report detection status, version, and architecture compatibility for all tool adapters.
* `GET /api/v1/system/resources` — Return CPU, RAM, and disk utilization metrics.

---

## 12. Modular Tool Adapter Architecture

Every security tool is integrated by implementing the abstract base class `BaseToolAdapter`. 

```python
# File: scanet/adapters/base.py
import abc
import typing

class ToolResult:
    def __init__(self, exit_code: int, raw_output: str, normalized_data: dict, error: str = None):
        self.exit_code = exit_code
        self.raw_output = raw_output
        self.normalized_data = normalized_data
        self.error = error

class BaseToolAdapter(abc.ABC):
    @property
    @abc.abstractmethod
    def tool_name(self) -> str:
        """Name of the tool binary (e.g., 'nmap', 'ffuf')."""
        pass

    @property
    @abc.abstractmethod
    def category(self) -> str:
        """Category: 'port_scan', 'web_discovery', 'dns', 'http', 'ssl'."""
        pass

    @abc.abstractmethod
    def is_installed(self) -> bool:
        """Check if binary exists in PATH or /opt/scanet/bin/."""
        pass

    @abc.abstractmethod
    def get_version(self) -> str:
        """Return detected version string."""
        pass

    @abc.abstractmethod
    def build_command_args(self, target: str, options: dict) -> typing.List[str]:
        """
        Safely construct argument list.
        MUST NEVER return a concatenated shell string.
        """
        pass

    @abc.abstractmethod
    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        """Transform raw tool output into scanet normalized dictionary."""
        pass
```

### 12.1 Nmap Tool Adapter Implementation Example
```python
# File: scanet/adapters/nmap_adapter.py
import shutil
import subprocess
import defusedxml.ElementTree as ET
from scanet.adapters.base import BaseToolAdapter

class NmapAdapter(BaseToolAdapter):
    tool_name = "nmap"
    category = "port_scan"

    def is_installed(self) -> bool:
        return shutil.which(self.tool_name) is not None

    def get_version(self) -> str:
        if not self.is_installed():
            return "Not Installed"
        res = subprocess.run([self.tool_name, "-V"], capture_output=True, text=True)
        return res.stdout.splitlines()[0] if res.stdout else "Unknown"

    def build_command_args(self, target: str, options: dict) -> list[str]:
        # Unprivileged TCP Connect scan with XML stdout stream
        args = [self.tool_name, "-sT", "-oX", "-", "--no-stylesheet"]
        
        # Enforce rate/timing limits
        speed = str(options.get("speed", 3))
        args.extend(["-T", speed if speed in ["1", "2", "3", "4"] else "3"])
        
        ports = options.get("ports", "top-100")
        if ports == "top-100":
            args.extend(["--top-ports", "100"])
        elif ports == "top-1000":
            args.extend(["--top-ports", "1000"])
            
        if options.get("service_detection", True):
            args.append("-sV")
            
        args.append(target)
        return args

    def parse_output(self, raw_output: str, exit_code: int) -> dict:
        parsed = {"hosts": [], "open_ports_count": 0}
        if exit_code != 0 and not raw_output:
            return parsed

        try:
            root = ET.fromstring(raw_output)
            for host_el in root.findall("host"):
                addr = host_el.find("address").get("addr")
                ports = []
                ports_el = host_el.find("ports")
                if ports_el is not None:
                    for p in ports_el.findall("port"):
                        state = p.find("state").get("state")
                        if state == "open":
                            service_el = p.find("service")
                            ports.append({
                                "port": int(p.get("portid")),
                                "protocol": p.get("protocol"),
                                "state": state,
                                "service": service_el.get("name") if service_el is not None else "unknown",
                                "product": service_el.get("product") if service_el is not None else "",
                                "version": service_el.get("version") if service_el is not None else ""
                            })
                parsed["hosts"].append({"ip": addr, "ports": ports})
                parsed["open_ports_count"] += len(ports)
        except Exception as e:
            parsed["parse_error"] = str(e)
            
        return parsed
```

---

## 13. Background Process Manager & Cancellation Architecture

Long-running security tools must not block the web server or leave orphaned scanning processes when cancelled.

```python
# File: scanet/engine/job_manager.py
import asyncio
import os
import signal
import typing

class ProcessJobManager:
    def __init__(self):
        self.active_processes: dict[str, asyncio.subprocess.Process] = {}

    async def execute_job(
        self,
        job_id: str,
        cmd_args: list[str],
        output_callback: typing.Callable[[str], typing.Awaitable[None]],
        timeout_seconds: int = 600
    ) -> tuple[int, str]:
        """
        Executes a command within an independent process group.
        Streams line output via output_callback.
        """
        # Execute in a new session (setsid) to allow terminating the entire process group
        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            preexec_fn=os.setsid
        )
        self.active_processes[job_id] = proc
        output_lines = []

        try:
            async with asyncio.timeout(timeout_seconds):
                while True:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    decoded_line = line.decode("utf-8", errors="replace")
                    output_lines.append(decoded_line)
                    await output_callback(decoded_line)
                    
                await proc.wait()
        except asyncio.TimeoutError:
            await self.cancel_job(job_id)
            return (-1, "".join(output_lines) + "\n[ERROR] Job exceeded timeout limit.")
        finally:
            self.active_processes.pop(job_id, None)

        return (proc.returncode or 0, "".join(output_lines))

    async def cancel_job(self, job_id: str) -> bool:
        """Sends SIGTERM followed by SIGKILL to the process group."""
        proc = self.active_processes.get(job_id)
        if not proc or proc.returncode is not None:
            return False

        try:
            # Kill the entire process group
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGTERM)
            await asyncio.sleep(1.0)
            if proc.returncode is None:
                os.killpg(pgid, signal.SIGKILL)
            return True
        except ProcessLookupError:
            return True
```

---

## 14. Application Security Threat Model & Safeguards

| Threat Vector | Risk Description | scanet Mitigation Engine |
| :--- | :--- | :--- |
| **Command Injection (CWE-78)** | Malicious payloads in target or option inputs leading to remote code execution. | Strict use of `asyncio.create_subprocess_exec` passing argument arrays; zero usage of shell wrappers (`/bin/sh -c`). Input regex whitelist validation. |
| **Server-Side Request Forgery (CWE-918)** | Scanning loopback or cloud metadata services (`169.254.169.254`) to steal instance tokens. | Target Scope Validator strictly blocks `127.0.0.0/8`, `169.254.0.0/16`, `::1`, and AWS IMDS endpoints. |
| **Out-of-Scope Scanning** | Scanning unapproved external university assets or third-party web services. | Database-backed target whitelist; all scan requests must match pre-approved domain/CIDR rules. |
| **Resource Starvation (DoS)** | Scan processes consuming 100% CPU/RAM or spawning unthrottled concurrent jobs. | System concurrency limit (max 2 concurrent scans on 1 GB RAM nodes); enforced timeouts (default 10 min); rate-limiting flags in tool arguments. |
| **Path Traversal (CWE-22)** | Arbitrary file read via malicious wordlist or report paths. | Wordlists restricted strictly to `/opt/scanet/wordlists/`; all user file paths validated using `os.path.realpath` with prefix validation. |

---

## 15. User Interface Sitemaps & Workflows

The front-end design uses an educational, streamlined dashboard built with responsive CSS grid and flexbox:

1. **Dashboard Overview:** Real-time metrics showing total jobs executed, currently active scans, system RAM/CPU load gauges, tool health indicators, and quick-launch shortcuts.
2. **Target & Scope Management:** Target inventory with whitelist indicators, approval tags, CIDR calculator tools, and historical scan timelines per target.
3. **Scan Execution Console:** Tool selection tabs (Nmap, Naabu, FFUF, dnsx, HTTPX, Diagnostics), parameter dropdowns (speed, port profiles, wordlist selection), and launch actions.
4. **Live Job Center:** Split-view console showing active jobs, elapsed timers, cancel buttons, and streaming terminal output via SSE.
5. **Interactive Findings Explorer:** Searchable, filterable tables detailing discovered hosts, open ports, web routes, technologies, and cryptographic findings.
6. **Reporting Center:** One-click generation and download of audit reports in HTML, JSON, CSV, and PDF formats.

---

## 16. Development Phases & Implementation Roadmap

```
Phase 1: Foundation (Days 1–3)
├── Setup FastAPI project layout & SQLite WAL models
├── Implement Scope Validator (blocking loopback/cloud metadata)
├── Implement ProcessJobManager with process-group cancellation
└── Build Tool Health Engine checking system PATH

Phase 2: Core Tool Adapters (Days 4–7)
├── Nmap Adapter (unprivileged -sT, XML parsing via defusedxml)
├── Naabu & HTTPX Adapters (JSON streaming)
├── FFUF Adapter (safe wordlist handling, JSON output)
└── Native Python Modules (Security Headers, Subnet Math, SSL Expiry)

Phase 3: Web Dashboard & Live Streaming (Days 8–11)
├── Modern CSS Design System (dark-mode aesthetic, responsive tokens)
├── Target Management & Scan Launch UI
├── SSE Live Output Console
└── Results Explorer Table & Diff Engine

Phase 4: Reporting & Hardening (Days 12–14)
├── Multi-format report exporter (HTML, JSON, CSV, PDF)
├── Audit logging & role-based restrictions
├── Docker & EC2 deployment scripts
└── Lab benchmark testing against vulnerable targets
```

---

## 17. References & Official Documentation

1. **Nmap Project:** Gordon Lyon, *Nmap Network Scanning: The Official Nmap Project Guide to Network Discovery and Security Scanning*, Insecure.com LLC. [nmap.org/book/man.html](https://nmap.org/book/man.html)
2. **ProjectDiscovery Tools (Naabu, HTTPX, dnsx, Subfinder, Nuclei):** Official Documentation & GitHub Repositories. [docs.projectdiscovery.io](https://docs.projectdiscovery.io/)
3. **FFUF (Fuzz Faster U Fool):** Project Repository & Documentation. [github.com/ffuf/ffuf](https://github.com/ffuf/ffuf)
4. **OWASP Top 10 Security Guidance:** Open Web Application Security Project. [owasp.org/Top10](https://owasp.org/Top10/)
5. **AWS Penetration Testing & Customer Policies:** Amazon Web Services Customer Support & Security Guides. [aws.amazon.com/security/penetration-testing/](https://aws.amazon.com/security/penetration-testing/)
6. **Python `asyncio` & Subprocess Management:** Python Software Foundation. [docs.python.org/3/library/asyncio-subprocess.html](https://docs.python.org/3/library/asyncio-subprocess.html)
7. **SQLite Write-Ahead Logging:** SQLite Consortium. [sqlite.org/wal.html](https://sqlite.org/wal.html)
