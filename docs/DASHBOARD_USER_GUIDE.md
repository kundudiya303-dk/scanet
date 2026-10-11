# 📖 scanet — Complete Dashboard Operator's Guide

> **Official Step-by-Step Operator Manual for the scanet Web-Orchestrated Cybersecurity Reconnaissance Platform**  
> *Targeted for Cybersecurity Students, Penetration Testers, DevSecOps Engineers, and Lab Administrators*  
> *Release: v0.3.0 Production Ready*

---

## 📑 Table of Contents

1. [Introduction & Quick Access](#1-introduction--quick-access)
2. [Global Navigation & Shell Architecture](#2-global-navigation--shell-architecture)
3. [Page-by-Page Feature Guide](#3-page-by-page-feature-guide)
   - [3.1 ◈ Main Dashboard Overview (`#/dashboard`)](#31--main-dashboard-overview-dashboard)
   - [3.2 ⊹ Target & Scope Manager (`#/targets`)](#32--target--scope-manager-targets)
   - [3.3 ☵ Chained Recon Pipelines (`#/pipelines`)](#33--chained-recon-pipelines-pipelines)
   - [3.4 ▷ Scan Launcher & Live Job Center (`#/jobs`)](#34--scan-launcher--live-job-center-jobs)
   - [3.5 ☊ Attack Surface Topology Graph (`#/topology`)](#35--attack-surface-topology-graph-topology)
   - [3.6 🛡️ Web Security & Misconfiguration Auditor (`#/webaudit`)](#36-️-web-security--misconfiguration-auditor-webaudit)
   - [3.7 ≡ Results Explorer & Scan Diff Engine (`#/results`)](#37--results-explorer--scan-diff-engine-results)
   - [3.8 ✦ AI Security Advisor & MITRE ATT&CK Copilot (`#/advisor`)](#38--ai-security-advisor--mitre-attck-copilot-advisor)
   - [3.9 ⊕ System Health & Host Diagnostics (`#/system`)](#39--system-health--host-diagnostics-system)
4. [End-to-End Operational Workflows](#4-end-to-end-operational-workflows)
   - [Workflow A: Complete External Attack Surface Recon](#workflow-a-complete-external-attack-surface-recon)
   - [Workflow B: Web Application Vulnerability & Misconfiguration Audit](#workflow-b-web-application-vulnerability--misconfiguration-audit)
   - [Workflow C: Subdomain Takeover & CNAME Dangling Record Verification](#workflow-c-subdomain-takeover--cname-dangling-record-verification)
   - [Workflow D: DevSecOps SARIF Export for GitHub Code Scanning](#workflow-d-devsecops-sarif-export-for-github-code-scanning)
5. [AWS EC2 Deployment & Operational Best Practices](#5-aws-ec2-deployment--operational-best-practices)
6. [Frequently Asked Questions (FAQ) & Troubleshooting](#6-frequently-asked-questions-faq--troubleshooting)

---

## 1. Introduction & Quick Access

**scanet** is a web-based, multi-tool cybersecurity reconnaissance platform that consolidates 12 industry-standard tools (Nmap, Naabu, RustScan, Katana, FFUF, Gobuster, dnsx, Subfinder, HTTPX, Nuclei, MTR, and passive OSINT) into a single, cohesive graphical interface.

### How to Access the Dashboard:

Once the server is launched (via `./run.sh` on EC2/Linux, `run.bat` on Windows, or `python run.py`), open your browser and navigate to:

- **From an AWS EC2 Instance (Public Access):**  
  👉 `http://<YOUR_EC2_PUBLIC_IP>:8000` *(e.g., `http://54.81.16.128:8000`)*
- **From Your Local Machine:**  
  👉 `http://localhost:8000`

> [!NOTE]  
> **No HTTPS, Domain, or SSL Certificates Required:** The dashboard runs directly over lightweight, unencrypted HTTP on port 8000. Ensure that **Custom TCP Port 8000** is open in your **AWS EC2 Security Group**.

---

## 2. Global Navigation & Shell Architecture

The dashboard is built as an ultra-fast Single Page Application (SPA). The navigation sidebar on the left gives instant access to all core modules without full-page reloads:

```
┌──────────────────────────────┐
│  [🛡️] scanet                 │
│      CYBER RECON             │
├──────────────────────────────┤
│  OVERVIEW                    │
│  ◈ Dashboard                 │
├──────────────────────────────┤
│  RECONNAISSANCE              │
│  ⊹ Target Manager            │
│  ☵ Recon Pipelines           │
│  ▷ Scan Launcher             │
│  ☊ Topology Graph            │
│  🛡️ Web Security Auditor     │
│  ≡ Results Explorer          │
├──────────────────────────────┤
│  INTELLIGENCE & AI           │
│  ✦ AI Security Advisor       │
├──────────────────────────────┤
│  PLATFORM                    │
│  ⊕ System Health             │
└──────────────────────────────┘
```

---

## 3. Page-by-Page Feature Guide

### 3.1 ◈ Main Dashboard Overview (`#/dashboard`)

The default landing page providing situational awareness, active scan statuses, and quick shortcuts.

* **Welcome Hero Banner:**
  - Displays the unique glowing cyber shield emblem with animated rotating radar pulse.
  - Live system status indicators: `● SYSTEM ONLINE`, `v0.3.0 PRODUCTION`, `12 TOOLS REGISTERED`, `AI MITRE COPILOT`.
  - Quick action buttons: **⚡ Launch Pipeline** (jumps directly to automated playbooks) and **▷ Custom Scan** (opens manual tool parameters).
* **Colorful KPI Cards:**
  - **Security Tools:** Shows availability status of integrated engines (`12/12 100% Ready`).
  - **Active Scans:** Count of currently running background scan workers.
  - **Lab Targets:** Number of authorized targets registered in scope.
  - **Cyber Hygiene Score:** Aggregate security rating calculated across all audited assets.
* **Recent Activity Feed:** Real-time log of recent scan executions, target creations, and detected vulnerability events.

---

### 3.2 ⊹ Target & Scope Manager (`#/targets`)

Before any tool can execute a scan, the target must be validated and registered in the **Scope Guard**. This protects operators from accidental scans against out-of-scope or forbidden infrastructure.

#### How to Register a Target:
1. Navigate to **⊹ Target Manager**.
2. Click **Add Target**.
3. Provide the required parameters:
   - **Target Address:** IP address (`192.168.1.50`), CIDR range (`10.0.0.0/24`), or fully qualified domain (`scanme.nmap.org`).
   - **Environment Tag:** Select `Lab Target`, `Staging`, `Production`, or `CTF Challenge`.
   - **Scope Classification:** `In-Scope (Whitelisted)`.
4. Click **Save Target**.

#### Built-in Scope Guardrails (SSRF & IMDS Protection):
`scanet` strictly blocks unauthorized targets to ensure safe lab operations:
- ❌ **AWS IMDS Metadata IP (`169.254.169.254`):** Hard-blocked to prevent cloud credential exfiltration.
- ❌ **Loopback Addresses (`127.0.0.0/8`, `localhost`):** Hard-blocked by default to prevent scanning host internal loopbacks.
- ❌ **Broadcast & Link-Local Addresses (`255.255.255.255`, `0.0.0.0`):** Rejected automatically.

#### One-Click Academic Lab Presets:
The dashboard includes instant registration buttons for standard vulnerable learning labs:
- **Metasploitable 2** (Linux network exploitation lab)
- **OWASP Juice Shop** (Modern web application security lab)
- **Damn Vulnerable Web App (DVWA)** (Classic PHP web vulnerabilities)

---

### 3.3 ☵ Chained Recon Pipelines (`#/pipelines`)

Pipelines allow you to chain multiple security tools sequentially into an automated, hands-off workflow. The output of one tool automatically feeds into the next.

#### Available Pre-Configured Playbooks:

| Playbook | Tools Executed in Sequence | Best Used For |
|---|---|---|
| **⚡ Full External Surface Recon** | `subfinder` ➔ `dnsx` ➔ `naabu` ➔ `nmap` ➔ `httpx` ➔ `nuclei` | Full end-to-end reconnaissance from domain discovery to vulnerability analysis. |
| **🌐 Web Application Security Audit** | `katana` ➔ `ffuf` ➔ `httpx` ➔ `nuclei` | Deep crawl and directory fuzzing of modern web apps and REST APIs. |
| **🩺 Network Diagnostics & Pathing** | `mtr` ➔ `naabu` ➔ `nmap` ➔ `subnet` | Network latency, routing hops, open ports, and CIDR subnet math. |
| **🕵️ Stealth Passive OSINT** | `subfinder` ➔ `crt.sh` ➔ `ip-api` ➔ `rdap` | 100% passive intelligence without sending a single probe packet to the target. |

#### How to Run a Pipeline:
1. Go to **☵ Recon Pipelines**.
2. Select your desired playbook.
3. Choose an authorized target from the dropdown.
4. Click **Execute Pipeline**.
5. Watch the live stage progress tracker:
   - `[✓ Completed]` Subdomain Enumeration
   - `[⠋ In Progress]` Active Port Screening
   - `[⏳ Pending]` Web Surface Inspection

---

### 3.4 ▷ Scan Launcher & Live Job Center (`#/jobs`)

The central command console for executing individual security tools with custom arguments and monitoring live streaming outputs.

#### Launching an Individual Tool:
1. Select the **Target Asset** from your whitelisted scope.
2. Select the **Tool**:
   - **Nmap:** Choose scan profile: *Quick Scan (`-F`)*, *Standard Connect (`-sT -sV`)*, or *Full Port Sweep (`-p-`)*.
   - **Naabu:** High-speed multi-port screening with custom rate limits.
   - **RustScan:** Adaptive multithreaded discovery.
   - **Katana:** Configure crawl depth (1–5) and toggle headless Chromium mode.
   - **FFUF:** Select wordlist (*common.txt*, *raft-medium-directories.txt*) and rate limit (req/sec).
   - **Gobuster:** Choose directory mode or virtual host (`vhost`) mode.
   - **Subfinder:** Select passive sources and timeout.
   - **dnsx:** Choose record types to query (`A`, `AAAA`, `CNAME`, `MX`, `TXT`, `PTR`).
   - **HTTPX:** Toggle status code detection, title extraction, and tech stack detection.
   - **Nuclei:** Choose template categories (*cves*, *vulnerabilities*, *exposures*, *misconfigurations*).
   - **MTR:** Configure report cycle count and packet size.
3. Click **Start Scan Job**.

#### Real-Time SSE Terminal Output:
- The embedded terminal emulator connects to a live **Server-Sent Events (SSE)** stream.
- As the security tool produces stdout or stderr lines, they stream immediately into the dark cyber console.
- Displays elapsed time and live status badges (`RUNNING`, `COMPLETED`, `CANCELLED`).

#### Process Group Job Control (`os.setsid`):
- Click **Stop Job** at any time.
- `scanet` sends a deterministic `SIGTERM` / `SIGKILL` signal to the entire Linux process group, guaranteeing that child scanners are killed instantly without leaving orphaned or zombie background processes on your EC2 instance.

---

### 3.5 ☊ Attack Surface Topology Graph (`#/topology`)

A visual, force-directed node map showing the hierarchical relationships between assets, network boundaries, and vulnerability findings.

#### Color-Coded Node Key:
- 🟢 **Root Target Domain / CIDR Network:** Center origin node.
- 🔵 **Subdomains:** Discovered via Subfinder and dnsx.
- 🟣 **IP Host Nodes:** Discovered IP addresses mapped to subdomains.
- 🟡 **Open TCP Ports & Services:** Open ports discovered by Nmap and Naabu (e.g., `80/http`, `22/ssh`, `443/https`).
- 🔴 **Vulnerability Finding Alerts:** High-severity exposures and CVEs discovered by Nuclei.

#### Graph Interactions:
- **Pan & Zoom:** Click and drag the background or use mouse wheel to zoom in/out.
- **Node Dragging:** Drag any node to rearrange the cluster layout.
- **Inspect Node:** Click any node to open the side inspector panel displaying raw IP, DNS records, banner details, and CVSS scores.

---

### 3.6 🛡️ Web Security & Misconfiguration Auditor (`#/webaudit`)

A dedicated, lightweight web application scanner combining the core auditing functions of **Nikto, OWASP ZAP, and Amass Takeover Detection** into a single page.

#### Feature Capabilities:
1. **Security Health Grade (`A+` to `F`):**
   - Automatically computes a risk score ($0\text{–}100$) based on detected critical, high, medium, and low issues.
2. **HTTP Insecure Methods Audit:**
   - Probes `OPTIONS`, `TRACE`, `PUT`, and `DELETE`.
   - Flags `TRACE` as Cross-Site Tracing (XST) risk.
   - Flags unauthenticated `PUT`/`DELETE` as file modification risks.
3. **Sensitive File & Directory Exposure Probes:**
   - Detects leaked `.env` environment credential files.
   - Detects exposed `.git/HEAD` source code repositories.
   - Audits `robots.txt` and `sitemap.xml` for internal admin routes.
   - Checks for `phpinfo.php`, `config.json`, and database `.sql` dumps.
4. **Cookie Security Diagnostics:**
   - Verifies whether session cookies enforce `HttpOnly` (preventing XSS theft), `Secure` (preventing cleartext transmission), and `SameSite` (preventing CSRF).
5. **CORS Policy Checker:**
   - Flags dangerous wildcard configurations (`*`) combined with `Allow-Credentials: true` and arbitrary origin reflection.
6. **Subdomain Takeover & DNS Dangling Record Checker:**
   - Test any domain or CNAME against 8+ cloud providers (AWS S3, GitHub Pages, Heroku, Shopify, CloudFront, Azure, Surge, Bitbucket).
   - Instant warning if an orphaned CNAME points to an unclaimed cloud resource.
   - Verifies authoritative nameservers for DNS AXFR Zone Transfer leaks.

#### How to Run a Web Audit:
1. Go to **🛡️ Web Security Auditor**.
2. Enter the target web address (e.g., `http://target-app.local` or `http://54.81.16.128:8000`).
3. Click **⚡ Start Web Audit**.
4. The dashboard displays the letter grade, risk breakdown, and itemized remediation steps.

---

### 3.7 ≡ Results Explorer & Scan Diff Engine (`#/results`)

Unified table view of all findings across every scan job with filtering, asset drift comparison, and multi-format export.

#### Tabbed Tables:
- **Hosts Tab:** IP addresses, hostnames, detected operating systems, and open port counts.
- **Endpoints Tab:** URLs discovered by Katana and FFUF, HTTP response codes, and content lengths.
- **Vulnerabilities Tab:** Detailed findings list with severity pills (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`), matched CVE IDs, and CVSS v3.1 scores.

#### Scan Diff Engine (Asset Drift):
- Select **Scan Job A** (Baseline) and **Scan Job B** (Recent).
- Click **Compare Diffs**.
- Highlights newly opened ports (attack surface expansion), closed ports, and newly discovered vulnerabilities between the two scan timestamps.

#### Multi-Format Reporting:
Export your findings in any industry-standard format with a single click:
- **OASIS SARIF v2.1.0:** Direct compatibility with GitHub Code Scanning, GitLab CI/CD, and VS Code SARIF viewers.
- **Executive PDF / HTML:** Clean formatted report with executive summary, tables, and remediation playbooks.
- **JSON & CSV:** Raw machine-readable data for data science or SIEM ingestion.

---

### 3.8 ✦ AI Security Advisor & MITRE ATT&CK Copilot (`#/advisor`)

An intelligent advisory engine running **100% offline with zero external API dependencies**, translating raw scan findings into tactical defenses.

#### Features:
1. **MITRE ATT&CK Mapping:**
   - Maps exposed services and open ports to specific MITRE ATT&CK Enterprise tactics and techniques (e.g., `T1190 - Exploit Public-Facing Application`, `T1078 - Valid Accounts`, `T1046 - Network Service Discovery`).
2. **Attack Path Simulation:**
   - Simulates likely adversary lateral movement pathways based on the combination of discovered ports (e.g., SMB 445 + RDP 3389 = Pass-the-Hash / Ransomware deployment path).
3. **Student & Operator Remediation Playbooks:**
   - Generates exact hardening commands for Apache, Nginx, OpenSSH, Redis, MySQL, and PostgreSQL.

---

### 3.9 ⊕ System Health & Host Diagnostics (`#/system`)

Displays real-time telemetry from your AWS EC2 host and verifies tool dependencies.

* **Host Hardware Meters:**
  - CPU utilization and core count.
  - RAM memory usage (used vs total).
  - Swap file usage (verifies the 2GB OOM shield is active).
  - Disk storage capacity on the root partition.
* **Tool Availability Matrix:**
  - Audits which CLI binaries are installed on the host system (`nmap`, `subfinder`, `nuclei`, `python3`, `curl`, `git`).
  - Green badge = Installed and ready.
  - Gray badge = Optional engine not present.
* **Network Latency & IP Detection:**
  - Confirms external internet reachability and displays detected AWS EC2 Public IPv4.

---

## 4. End-to-End Operational Workflows

### Workflow A: Complete External Attack Surface Recon
1. Go to **⊹ Target Manager** and add your target domain (e.g., `example.com`).
2. Click **☵ Recon Pipelines**.
3. Select **⚡ Full External Surface Recon** and choose your target.
4. Click **Execute Pipeline**.
5. Wait for the automated stages to complete:
   - Subfinder discovers subdomains.
   - dnsx resolves IP addresses.
   - Naabu screens active open ports.
   - Nmap extracts service banners and detects operating system.
   - HTTPX fingerprints web technologies.
   - Nuclei scans for vulnerabilities and CVEs.
6. Open **☊ Topology Graph** to see the interactive visual map of all discovered assets.
7. Open **≡ Results Explorer** and export the final report as **SARIF** or **PDF**.

---

### Workflow B: Web Application Vulnerability & Misconfiguration Audit
1. Navigate to **🛡️ Web Security Auditor**.
2. Enter the web application URL (e.g., `http://target-web.com`).
3. Click **⚡ Start Web Audit**.
4. Review the generated letter grade (e.g., `Grade: B - MODERATE`).
5. Inspect the **Sensitive Endpoints** table: Check if `.env`, `.git`, or backup files returned HTTP 200.
6. Review the **Cookie Security** card: Verify that `HttpOnly` and `Secure` flags are enabled.
7. Implement the remediation steps provided at the bottom of the page.

---

### Workflow C: Subdomain Takeover & CNAME Dangling Record Verification
1. Run a Subdomain Discovery scan via **▷ Scan Launcher** using `subfinder`.
2. Review the discovered subdomains in **≡ Results Explorer**.
3. Go to **🛡️ Web Security Auditor** and scroll to the **Subdomain Takeover Checker**.
4. Enter the subdomain (e.g., `blog.example.com`) and observed CNAME (e.g., `myblog.github.io`).
5. Click **🔍 Verify Takeover**.
6. If the signature matches an unclaimed service, take immediate action to either claim the asset or delete the stale CNAME record in DNS.

---

### Workflow D: DevSecOps SARIF Export for GitHub Code Scanning
1. Complete any pipeline or custom scan job.
2. Navigate to **≡ Results Explorer**.
3. Click the **Export SARIF v2.1** button at the top right.
4. The browser downloads `scanet_report.sarif`.
5. Upload this file directly to your GitHub repository using the GitHub Code Scanning action:
   ```yaml
   - name: Upload SARIF report
     uses: github/codeql-action/upload-sarif@v3
     with:
       sarif_file: scanet_report.sarif
   ```
6. Findings will appear directly in your repository's **Security ➔ Code scanning alerts** tab!

---

## 5. AWS EC2 Deployment & Operational Best Practices

When running `scanet` on AWS EC2 instances (such as Free-Tier `t3.micro` or `t4g.micro`):

1. **Security Group Inbound Rule:**
   - In the AWS EC2 Management Console, open **Security Groups** ➔ **Inbound Rules**.
   - Add rule: **Type:** `Custom TCP`, **Port Range:** `8000`, **Source:** `0.0.0.0/0` (or restrict to your office/home IP for security).
2. **Low-Memory OOM Shield:**
   - `scanet`'s `./run.sh` launcher automatically creates and enables a **2GB swap file (`/swapfile`)** on EC2 instances with $\le 2.5\text{ GB}$ RAM. This prevents the Linux Out-Of-Memory (OOM) killer from terminating your scans.
3. **Process-Group Isolation:**
   - Even if you disconnect your SSH session, scans running via `nohup` or `screen`/`tmux` will continue uninterrupted.
4. **Graceful Shutdown:**
   - In the terminal running `scanet`, press `Ctrl + C` once. The ASGI server will gracefully flush pending SQLite WAL writes and terminate safely.

---

## 6. Frequently Asked Questions (FAQ) & Troubleshooting

### Q1: The web page does not load in my browser after running `./run.sh` on EC2.
* **Fix:** Make sure you are using `http://` and **NOT** `https://`. (e.g., `http://54.81.16.128:8000`). Also verify that **Port 8000** is open in your AWS EC2 Security Group Inbound Rules.

### Q2: Can I change the port from 8000 to something else (e.g., 8080 or 80)?
* **Fix:** Yes! You can pass the port argument directly:
  ```bash
  ./run.sh 8080
  # Or for port 80 (standard HTTP, requires root/sudo):
  sudo ./run.sh 80
  ```
  Or choose option `[2]` in the interactive launcher menu.

### Q3: Why does target validation reject `127.0.0.1` or `169.254.169.254`?
* **Answer:** This is a built-in safety guardrail. Scanning `127.0.0.1` attacks the local host running the scanner, and `169.254.169.254` is the AWS instance metadata service (IMDS). `scanet` hard-blocks these to maintain strict ethical safety.

### Q4: Does `scanet` send scan data to third-party cloud servers?
* **Answer:** **No.** `scanet` operates 100% locally on your machine or EC2 node. All databases (SQLite), AI heuristics, and report generators run locally with zero external telemetry.

---

*scanet — Engineered for Educational Defense, Rigorous Auditing, and Cloud Resilience.*
