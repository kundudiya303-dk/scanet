# scanet: Deep Internet & GitHub Research, Extended Tool Universe & High-Impact Feature Blueprint

**Comprehensive Research Synthesis & Strategic Expansion Report**  
*Document Version: 2.0.0 | Academic & Enterprise Attack Surface Management Blueprint*  
*Author: scanet Core Research & Architecture Team*

---

## 1. Executive Research Overview

To elevate **scanet** from a conventional security tool wrapper into an **award-winning, enterprise-competitive, and academically rigorous cybersecurity platform**, an exhaustive review of leading open-source Attack Surface Management (ASM) platforms, bug bounty frameworks, university capstone projects, and GitHub repositories was performed.

### Key Benchmark Frameworks Analyzed:
1. **reNgine (`yogeshojha/rengine`):** Pioneered web reconnaissance orchestration with YAML-defined scan engines, visual graph mapping, LLM-assisted attack surface analysis, and continuous monitoring.
2. **reconFTW (`six2dez/reconftw`):** Highly automated multi-tool bash/CLI recon framework integrating Subfinder, Naabu, Nuclei, Katana, and FFUF into structured sequential pipelines.
3. **Attack Surface Framework (`vmware-labs/attack-surface-framework`):** Enterprise attack surface watchdog focusing on asset drift, port lifecycle tracking, and vulnerability correlation.
4. **SpiderFoot (`smicallef/spiderfoot`):** The preeminent modular OSINT automation tool combining hundreds of passive data sources without sending intrusive traffic.
5. **ProjectDiscovery Tool Suite:** The modern standard for modular, high-speed, line-delimited JSON security tools (`nuclei`, `katana`, `subfinder`, `httpx`, `naabu`, `dnsx`, `tlsx`).

---

## 2. Exhaustive Tool Taxonomy Across 8 Security Domains

The following matrix represents the complete universe of reconnaissance, inspection, and vulnerability assessment tools, categorized by operational domain, privilege model, performance profile, and integration suitability for `scanet`.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             scanet Tool Taxonomy                                 │
└──────────────────────────────────────┬───────────────────────────────────────────┘
                                       │
     ┌──────────────────┬──────────────┴───────────────┬──────────────────┐
     ▼                  ▼                              ▼                  ▼
┌──────────────┐ ┌──────────────┐               ┌──────────────┐   ┌──────────────┐
│  Domain 1-2  │ │  Domain 3-4  │               │  Domain 5-6  │   │  Domain 7-8  │
│ Port & Net   │ │ Crawl & Fuzz │               │ HTTP & Vuln  │   │ OSINT & AI   │
├──────────────┤ ├──────────────┤               ├──────────────┤   ├──────────────┤
│• Nmap        │ │• Katana      │               │• HTTPX       │   │• WHOIS/RDAP  │
│• Naabu       │ │• FFUF        │               │• testssl.sh  │   │• ASN/IP-API  │
│• RustScan    │ │• Gobuster    │               │• Nuclei      │   │• CVE Lookup  │
│• MTR / Ping  │ │• Feroxbuster │               │• Gitleaks    │   │• AI Advisor  │
│• Netcat (nc) │ │• ParamSpider │               │• Header Grdr │   │• Topology    │
└──────────────┘ └──────────────┘               └──────────────┘   └──────────────┘
```

### 2.1 Domain 1: Port Scanning & Network Host Discovery
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **Nmap** | Deep service detection, OS fingerprinting, NSE scripts | Gold standard accuracy, rich service probes | XML (`-oX`) | **Core Engine (Tier 1)** |
| **Naabu** | High-speed multi-port screening | Native JSON lines, SYN/Connect fallback | JSONL | **Fast Scanner (Tier 1)** |
| **RustScan** | Adaptive port discovery using Rust threads | Extremely rapid (1,000 ports in < 3s) | Text | **Fast Discovery (Tier 2)** |
| **Netcat** | Single-port reachability & raw banner grabs | Zero dependencies, instant verification | Raw text | **Diagnostic (Tier 1)** |
| **MTR** | Route tracing, latency, packet loss diagnostics | Replaces ping/traceroute with JSON metrics | JSON (`--json`)| **Network Health (Tier 1)**|
| **Masscan** | Asynchronous internet-scale SYN scanner | Ultra-fast (millions pkt/sec) | JSON | **Restricted / Lab Only** |

### 2.2 Domain 2: DNS Intelligence & Subdomain Enumeration
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **Subfinder** | Passive subdomain enumeration | Zero traffic sent to target, 30+ sources | JSONL | **Passive Recon (Tier 1)**|
| **dnsx** | Active multi-record DNS resolution & wildcards | Resolves A, AAAA, CNAME, MX, TXT, PTR | JSONL | **Active DNS (Tier 1)** |
| **Dig / Host** | Low-level DNS querying & AXFR zone transfers | Standard Unix utility, verified protocol behavior| Text | **Diagnostic (Tier 1)** |
| **crt.sh API** | TLS Certificate Transparency query | 100% passive, finds historical certificates | JSON | **Native Python (Tier 1)**|
| **OWASP Amass**| Full attack surface graph mapping | Deep multi-source intelligence | Graph / JSON | **Heavy / Tier 3** |

### 2.3 Domain 3: Web Crawling, Spidering & Endpoint Discovery
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **Katana** | Modern web crawler (Standard & Headless modes) | Parses HTML, JS, forms, API routes, regex scope | JSONL | **Next-Gen Crawler (Tier 1)**|
| **GAU** | GetAllUrls from AlienVault, Wayback, CommonCrawl | Rapid historical URL gathering | Text | **Passive Recon (Tier 2)**|
| **Waybackurls**| Historical endpoint retrieval from archive.org | Passive discovery of unlinked legacy endpoints | Text | **Passive Recon (Tier 2)**|
| **ParamSpider**| Extracts URL query parameters for fuzzing | Finds reflection points and injection surfaces | Text | **Targeted Fuzzing (Tier 2)**|

### 2.4 Domain 4: Web Content & Directory Fuzzing
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **FFUF** | Fast web fuzzer for paths, vhosts, parameters | Low RAM (30-75MB), granular rate limits | JSON | **Primary Fuzzer (Tier 1)**|
| **Gobuster** | Academic directory, DNS, and vhost bruteforce | Highly familiar to cybersecurity students | Text / JSON | **Academic Engine (Tier 1)**|
| **Feroxbuster**| Recursive directory exploration in Rust | Auto-recursion, wildcards filtering | JSONL | **Deep Fuzzer (Tier 2)** |
| **Dirsearch** | Python-based advanced path scanner | Rich default extensions and response handling | JSON | **Fallback Fuzzer (Tier 2)**|

### 2.5 Domain 5: HTTP Inspection & Technology Fingerprinting
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **HTTPX** | Multi-purpose HTTP surface probe | Titles, status codes, tech stack, TLS previews | JSONL | **Primary Probe (Tier 1)** |
| **WhatWeb** | Deep web technology fingerprinting | Detects CMS, JS libs, embedded frameworks | JSON | **Tech Discovery (Tier 2)**|
| **cURL** | Raw request/response inspection & method checks | Unaltered raw HTTP debugging | Raw | **Diagnostic (Tier 1)** |
| **fingerprintx**| Standalone service fingerprinting utility | Detects non-standard protocol daemons | JSONL | **Micro-Service Probe (Tier 2)**|

### 2.6 Domain 6: Vulnerability Assessment & Misconfiguration Auditing
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **Nuclei** | Fast template-based vulnerability & misconfig scanner| 5,000+ community templates, strict severity tags| JSONL | **Auditing Engine (Tier 1)**|
| **testssl.sh** | Cryptographic TLS/SSL auditing | Deep cipher test, TLS 1.0-1.3, known flaws | JSON | **Crypto Audit (Tier 2)** |
| **Gitleaks** | Secret scanning for exposed API keys & credentials | Detects leaked AWS, GitHub, JWT tokens in JS | JSON | **Secret Auditing (Tier 2)**|
| **Nikto** | Traditional web server vulnerability scanner | Familiar academic tool for comparison | XML / JSON | **Comparative (Tier 3)** |

### 2.7 Domain 7: Threat Intelligence & OSINT (Passive)
| Tool | Primary Purpose | Strengths | Output | Role in scanet |
| :--- | :--- | :--- | :--- | :--- |
| **WHOIS / RDAP**| Domain registrar, organization, and CIDR blocks | Standard RFC compliance, zero active scans | JSON | **Native Python (Tier 1)**|
| **IP-API / ASN**| Geolocation, Autonomous System Number, ISP info | Identifies cloud providers (AWS, Azure, Cloudflare)| JSON | **Native Python (Tier 1)**|
| **Shodan API** | Internet-wide exposed service indexing | Passive service discovery without touching target | JSON | **API Adapter (Tier 2)** |
| **AbuseIPDB** | IP reputation and malicious report history | Identifies known attack infrastructure | JSON | **API Adapter (Tier 2)** |

### 2.8 Domain 8: Native Zero-Dependency Internal Analyzers
| Engine Name | Implementation | Functionality |
| :--- | :--- | :--- |
| **Header Grader** | Native Python `httpx` | Grades HTTP posture (A+ to F), checks CSP, HSTS, XFO |
| **SSL Inspector** | Native Python `ssl` | Extracts SANs, issuer, cipher suite, and expiry warnings (<30d) |
| **Subnet Calculator**| Native Python `ipaddress` | Computes network masks, usable IPs, broadcast, wildcard bits |
| **Scan Diff Engine**| Native Python Dict Diff | Highlights added ports, removed endpoints, and altered services |
| **CVE Correlator** | Native Python CPE Matcher | Correlates service banners with known CVEs & CISA KEV entries |
| **AI Advisor Engine**| Rule Expert System + LLM | Explains vulnerabilities, maps to MITRE ATT&CK, gives remediations|
| **SARIF Exporter** | Native Python Builder | Exports OASIS SARIF v2.1.0 for GitHub / CI/CD ingestion |

---

## 3. High-Impact Flagship Features

To create maximum real-world impact and academic distinction, `scanet` introduces six flagship feature modules:

### 3.1 Feature 1: Chained Multi-Tool Recon Pipelines (Playbooks)
Rather than requiring users to manually run tools one at a time, `scanet` provides pre-configured, automated sequential pipelines:
1. **Full Attack Surface Pipeline:**
   `Subfinder` (Passive Subdomains) ➔ `dnsx` (Resolve Active IPs) ➔ `Naabu` (Rapid Port Screening) ➔ `Nmap` (Service & Version Probes) ➔ `HTTPX` (Web Surface Probing) ➔ `Header Grader & SSL Inspector` ➔ `Nuclei` (Exposure Audit) ➔ `SARIF & PDF Report Generation`.
2. **Web Security Audit Pipeline:**
   `Katana` (Deep Web Crawling) ➔ `FFUF` (Sensitive Path Fuzzing) ➔ `HTTPX` (Header & TLS Verification) ➔ `Nuclei` (Misconfiguration Templates).
3. **Network Diagnostics Pipeline:**
   `MTR` (Route & Packet Loss Analysis) ➔ `Naabu` (All-Port TCP Connect) ➔ `Nmap` (Service Versioning) ➔ `Subnet Math & CIDR Boundary Check`.
4. **Passive OSINT Stealth Pipeline:**
   `Subfinder` (Passive DNS) ➔ `crt.sh` (Cert Transparency) ➔ `WHOIS/RDAP` ➔ `IP-API Geolocation & ASN Mapping` (Zero direct target packets).

### 3.2 Feature 2: AI-Powered Security Advisory & MITRE ATT&CK Copilot
* **Zero-Cost Heuristic Expert Engine:** Functions completely offline without requiring paid API keys or external tokens. Evaluates open ports and misconfigurations against a built-in knowledge base.
* **MITRE ATT&CK Mapping:** Automatically maps findings to Enterprise TTPs (e.g., T1046 Network Service Discovery, T1190 Exploit Public-Facing Application, T1595 Active Scanning).
* **Student-Friendly Remediation Explanations:** Translates raw tool flags and technical jargon into clear, actionable hardening instructions for system administrators and students.
* **Pluggable LLM Integration:** Optional interface for Ollama (local offline models like Llama3/Mistral in university labs) or cloud APIs (OpenAI, Gemini).

### 3.3 Feature 3: Interactive Force-Directed Network Topology Graph
* **Visual Graph Hierarchy:** `Target (Root)` ➔ `Subdomains (Child Nodes)` ➔ `IP Addresses (Host Nodes)` ➔ `Open Ports (Service Nodes)` ➔ `Vulnerabilities / CVEs (Alert Nodes)`.
* **Dynamic Node Color-Coding:**
  - 🟢 Green: Verified secure or informational service.
  - 🟡 Amber: Potential exposure (missing security headers, outdated TLS).
  - 🔴 Red: Critical finding, high-severity CVE, or dangerous exposed port (e.g. 6379 unauthenticated Redis, 445 SMB, 3389 RDP).
* **Interactive Filtering:** Allows filtering nodes by CIDR subnet, port number, protocol, and finding severity.

### 3.4 Feature 4: Continuous Asset Monitoring, Drift Detection & Webhooks
* **Scheduled Cron Scans:** Run daily, weekly, or custom cron intervals against authorized target assets.
* **Automated Asset Drift Detection:**
  - 🚨 *New Open Port Alert:* Notifies if a port opens that was not present in the baseline scan.
  - ⚠️ *Service Version Change:* Detects when a software package is updated or downgraded.
  - ⏰ *SSL Expiry Warning:* Triggers when a certificate is within 30 days of expiration.
* **Multi-Platform Webhook Dispatcher:** Instant notifications dispatched to Discord, Slack, Telegram, or generic webhooks.

### 3.5 Feature 5: Interactive Educational "Flag Explainer" & Lab Training Mode
* **Hover Flag Explanations:** When a student configures a scan, the UI previews the exact CLI command (e.g., `nmap -sT -sV -T3 -p 80,443,8080 target.lab`) and provides interactive callouts:
  - `-sT`: Explains the full 3-way TCP handshake (`SYN -> SYN-ACK -> ACK`) executed via the unprivileged `connect()` system call.
  - `-sV`: Explains banner grabbing, probe scripts, and version match regexes.
  - `-T3`: Explains timing templates and packet throttling to prevent lab switch congestion.
* **Pre-Configured University Lab Presets:** Single-click configurations for Metasploitable 2/3, OWASP Juice Shop, DVWA, and RFC1918 subnets.

### 3.6 Feature 6: Enterprise Multi-Format Reporting & DevSecOps Compliance
* **OASIS SARIF v2.1.0:** The industry standard for static and dynamic analysis results, importable into GitHub Security Center, GitLab, and DefectDojo.
* **Executive Summary PDF / HTML:** Formatted with executive risk score (0-100), severity distribution graphs, top 5 high-risk findings, and executive sign-off sections.
* **Compliance Framework Mapping:** Automatically categorizes scan findings against:
  - **OWASP Top 10 (2021):** A01 Broken Access Control, A05 Security Misconfiguration, A07 Identification and Authentication Failures.
  - **CIS Controls v8:** Control 4 (Secure Configuration of Assets), Control 7 (Vulnerability Management), Control 12 (Network Infrastructure Management).
  - **NIST CSF:** Identify (ID.AM Asset Management), Protect (PR.IP Information Protection).

---

## 4. Architectural Implementation Strategy

The following architectural updates will be integrated directly into the `scanet` codebase:
1. **Adapters:** Addition of `katana_adapter.py`, `nuclei_adapter.py`, `gobuster_adapter.py`, and `rustscan_adapter.py`.
2. **Analyzers:** Addition of `cve_correlator.py`, `ai_advisor.py`, `compliance.py`, `sarif_exporter.py`, and `webhook_notifier.py`.
3. **Engine:** Addition of `pipeline_manager.py` to chain sequential tool runs with automatic output piping.
4. **Database Models:** Addition of `Pipelines`, `Schedules`, `CVEFindings`, and `WebhookConfigs` tables.
5. **API Endpoints:** Routes for `/api/v1/pipelines`, `/api/v1/advisor`, `/api/v1/schedules`, `/api/v1/compliance`, and `/api/v1/export/sarif`.
6. **Frontend Dashboard:** Modern dark-themed user interface with interactive tabs for Pipelines, Topology Graph, AI Advisor, and Lab Scenarios.

---
*End of Deep Research & Feature Blueprint Specification.*
