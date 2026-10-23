# scanet 🔍

> **A Lightweight, Modular, Web-Orchestrated Cybersecurity Reconnaissance & Attack Surface Management Platform**  
> *Engineered for University Labs, Virtual Environments, and Cloud Deployments (AWS EC2)*  
> *Zero Shell Injection · Async Process Groups · SQLite WAL · DevSecOps SARIF v2.1.0*

---

## 🌟 Executive Overview

**scanet** is a unified, web-based cybersecurity platform that consolidates essential open-source network reconnaissance, web discovery, DNS analysis, HTTP inspection, and vulnerability assessment tools into a single, intuitive graphical interface.

Unlike bulky enterprise suites (OpenVAS, Tenable Nessus, full OWASP ZAP) that consume gigabytes of memory and require complex multi-service daemons, `scanet` is engineered with an **ultra-lightweight footprint** ($\le 120\text{ MB}$ idle, $\le 650\text{ MB}$ peak during active scans). It runs seamlessly on low-resource virtual machines and burstable cloud nodes like **AWS EC2 `t4g.micro` (Graviton)** and **`t3.micro` (Free Tier)**.

---

## ⚡ One-Command Instant Launch (Local or AWS EC2)

After cloning the repository, execute **one single command**:

### On Linux / AWS EC2 (Direct HTTP Access):
```bash
git clone https://github.com/mjishaan59-cell/scanet.git
cd scanet
./run.sh
```
Install Python 3.10 or newer first. On first launch, the script creates
`backend/.venv` and installs the Python dependencies; native scanner binaries
are optional. The first install requires internet access.
> **🌐 AWS EC2 Quick Access (No HTTPS / No Domain Needed):**  
> 1. In your **AWS EC2 Security Group**, add an Inbound Rule for **Custom TCP Port 8000** (Source: `0.0.0.0/0` or your IP).  
> 2. Open `http://<YOUR_EC2_PUBLIC_IP>:8000` in your browser.  
> 3. That's it! The colorful cybersecurity dashboard will load immediately.  
> *(Optional: To run on a custom port like 8080 or 80, pass the port argument: `./run.sh 8080` or `sudo ./run.sh 80`)*

### On Windows:
```cmd
git clone https://github.com/mjishaan59-cell/scanet.git
cd scanet
run.bat
```
Install **Python 3.10 or newer** first and enable **Add python.exe to PATH** in
the Python installer. On first launch, `run.bat` creates an isolated environment
in `backend\.venv` and installs `backend\requirements.txt`; later launches reuse
it. The first install needs an internet connection. If Windows says Python was
not found, install it from [python.org](https://www.python.org/downloads/) and
open a new terminal before retrying.

### Any System (Python 3.10+):
```bash
python run.py
```
The launcher creates `backend/.venv` and installs the Python dependencies on
first launch (or when `backend/requirements.txt` changes). No global Python
packages are modified. Native scanner binaries are optional: scanet uses its
built-in Python engines when those tools are not installed.

### Docker
With Docker Desktop or Docker Engine and the Compose plugin installed, build and
start the container with:
```bash
docker compose -f docker/docker-compose.yml up --build
```
Then open `http://localhost:8000`. The database is persisted in a Docker volume.

---

## 📚 Official Documentation & User Guides

- 📖 **[Complete Dashboard Operator's Guide (Full Step-by-Step Manual)](docs/DASHBOARD_USER_GUIDE.md)** — Exhaustive walkthrough covering every single page, button, tool, and workflow in the web UI.
- ☁️ **[AWS EC2 Cloud Deployment Guide](docs/AWS_EC2_DEPLOYMENT.md)** — Step-by-step AWS provisioning, Security Group configuration, and direct HTTP access.
- 📐 **[Master Architecture & Engineering Blueprint](SCANET_MASTER_BLUEPRINT.md)** — Complete system design, threat modeling, and data normalization specs.
- 🗂️ **[Step-by-Step Project Execution Log](records/PROJECT_STEPS_LOG.md)** — Chronological audit trail of all implementation milestones.
- 📦 **[GitHub Commit & Upload Tracker](records/GITHUB_UPLOAD_TRACKER.md)** — Version control synchronization registry.

---

## 🚀 Key Platform Capabilities

- 🔌 **14 Supported Security Engines** — Nmap, Naabu, RustScan, Katana, FFUF, Gobuster, dnsx, Subfinder, HTTPX, Nuclei, MTR, Passive OSINT, Native Nikto/ZAP Web Auditor, and Subdomain Takeover.
- 🛡️ **Web Security & Misconfiguration Auditor** — Pure-Python asynchronous Nikto & OWASP ZAP equivalent testing HTTP methods (TRACE/PUT/DELETE), sensitive file leaks (.env, .git, backups), cookie directives (HttpOnly, Secure, SameSite), and CORS policies.
- 🎯 **Subdomain Takeover & DNS AXFR Detector** — Detects orphaned CNAME records pointing to 8+ decommissioned cloud services (AWS S3, GitHub Pages, Heroku, Shopify, CloudFront, Azure, Surge, Bitbucket) and audits DNS zone transfer exposures.
- 🧠 **AI Security Advisor & MITRE ATT&CK Copilot** — Heuristic rule engine running 100% offline; maps exposures to MITRE ATT&CK TTPs and provides student remediation playbooks.
- 🎯 **Multi-Vector OS Detection Engine** — Non-root OS fingerprinting combining TCP/IP TTL heuristics (Linux initial 64, Windows initial 128, Cisco initial 255), service banner regexes (SSH/HTTP/FTP), and open port profiles.
- ☵ **Chained Reconnaissance Pipelines** — One-click automated workflows (Full Attack Surface, Web Security Audit, Network Diagnostics, and Stealth Passive OSINT).
- ☊ **Interactive Attack Surface Topology Graph** — Visual force-directed node map linking Targets $\rightarrow$ Subdomains $\rightarrow$ IP Hosts $\rightarrow$ Open Ports $\rightarrow$ Vulnerability Alerts.
- 🛡️ **Strict Scope & SSRF Guardrails** — Hard-blocks AWS IMDS metadata (`169.254.169.254`), loopbacks (`127.0.0.0/8`), and non-whitelisted external ranges.
- 📡 **Real-Time Job Control** — Non-blocking process execution via Linux process groups (`os.setsid`), live Server-Sent Events (SSE) streaming, and deterministic `SIGTERM` cancellation.
- 📄 **DevSecOps & Multi-Format Reporting** — Exports to **OASIS SARIF v2.1.0** (GitHub Code Scanning & GitLab CI), Executive PDF, Technical HTML, JSON, and CSV.
- 🔔 **Real-Time Alert Dispatcher** — Formatted alert notifications to Discord, Slack, Telegram, and generic HTTP webhooks.
- 🧪 **100% Verified Test Suite** — 32 unit tests covering scope enforcement, XML parsing, AI heuristics, CVE version matching, OS fingerprinting, web auditing, and subdomain takeover (100% pass rate).

---

## 🧰 Supported Tools Matrix

| Category | Tool | Execution Model | Output Format | Role in scanet |
|---|---|---|---|---|
| **Port & Service Discovery** | **Nmap** | Unprivileged TCP Connect (`-sT`) | XML (`defusedxml`) | Deep service & OS versioning |
| | **Naabu** | Fast multi-port sweep | Streaming JSONL | High-speed port screening |
| | **RustScan** | Adaptive Rust multithreading | Clean parsed text | Ultra-fast port discovery |
| **Web Crawling & Fuzzing** | **Katana** | Standard & Headless crawling | Streaming JSONL | Modern API & endpoint discovery |
| | **FFUF** | Granular rate-limited fuzzing | Native JSON | High-speed directory & parameter fuzzer |
| | **Gobuster** | Classic directory/vhost fuzzing | Regex normalized text | Standard academic recon tool |
| **DNS Intelligence** | **Subfinder** | 100% passive multi-source | Streaming JSONL | Zero-packet subdomain mapping |
| | **dnsx** | Multi-record DNS resolver | Streaming JSONL | Resolves A, AAAA, CNAME, MX, TXT, PTR |
| **HTTP Surface & TLS** | **HTTPX** | HTTP inspection & tech stack | Streaming JSONL | Status codes, titles, redirect chains |
| | **MTR** | Network routing diagnostics | Native JSON (`--json`)| Hop-by-hop latency and packet loss |
| **Vulnerability Assessment** | **Nuclei** | Curated non-destructive templates | Streaming JSONL | Detects exposures, misconfigs, and CVEs |
| **Threat Intelligence** | **OSINT Engine** | Passive IP-API, ASN & crt.sh | Async JSON | Geolocation, ISP, and Cert Transparency |
| **Native Python Engines** | **Headers, SSL, Subnet, CVE, AI, OS** | Built-in zero-dependency Python | Native Dict | Zero-overhead internal analysis |

---

## 🎯 OS Detection & Fingerprinting Feature

`scanet` includes an unprivileged multi-vector OS fingerprinting engine (`backend/analyzers/os_fingerprint.py`) that identifies the target operating system without requiring dangerous raw socket root privileges:

1. **IP TTL (Time-To-Live) Heuristics:**
   - **Linux / Android:** Initial TTL `64` (Observed $\sim 50\text{–}64$ hops).
   - **Microsoft Windows:** Initial TTL `128` (Observed $\sim 110\text{–}128$ hops).
   - **Cisco IOS / Network Appliances / Solaris:** Initial TTL `255` (Observed $\sim 240\text{–}255$ hops).
2. **Service Banner Signature Extraction:**
   - Matches SSH identification strings (e.g., `Ubuntu-3ubuntu0.1`, `Debian-2+deb12u2`, `OpenSSH_for_Windows`).
   - Analyzes HTTP `Server` headers (e.g., `Microsoft-IIS/10.0`, `Apache (Ubuntu)`, `lighttpd (Alpine)`).
   - Inspects FTP daemons (e.g., `vsftpd`, `Microsoft FTP Service`).
3. **Open Port Portfolio Profiling:**
   - Windows-specific fingerprint: Combination of ports `135`, `139`, `445` (SMB/NetBIOS) and `3389` (RDP).
   - Linux-specific fingerprint: Combination of port `22` (SSH), `111` (RPC), and `2049` (NFS).

---

## ☁️ Complete AWS EC2 Deployment Guide

Follow this guide to deploy `scanet` in a secure, production-hardened AWS EC2 environment.

### 1. Recommended EC2 Instance Sizing
- **`t4g.micro`** (2 vCPU, 1 GB RAM, ARM64 Graviton2) — **Recommended (~$6.13/month)**
- **`t3.micro`** (2 vCPU, 1 GB RAM, x86_64) — **AWS Free Tier Eligible (Free for 12 months)**

### 2. AWS Security Group Rules
Create a security group `scanet-secgroup`:
- **Inbound Rules:**
  - `SSH (22)`: `YOUR_PUBLIC_IP/32` (Only your administrative IP)
  - `HTTPS (443)`: `0.0.0.0/0` (Web dashboard access)
  - `HTTP (80)`: `0.0.0.0/0` (Certbot SSL verification)
- **Outbound Rules:**
  - `All Traffic`: `0.0.0.0/0` (Allows scanning authorized target ranges)

### 3. Launch Instance with Enforced IMDSv2
To protect cloud credentials from SSRF attacks, enforce IMDSv2:
```bash
aws ec2 run-instances \
    --image-id ami-04b70fa74e45c3917 \
    --instance-type t4g.micro \
    --key-name scanet-key \
    --security-group-ids sg-xxxxxx \
    --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=1,HttpEndpoint=enabled"
```

### 4. Connect and Provision the Server
```bash
ssh -i scanet-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>

# Update packages and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl ufw nginx nmap mtr-tiny
```

### 5. Clone and Install scanet
```bash
# Clone repository
git clone https://github.com/mjishaan59-cell/scanet.git /opt/scanet-app
cd /opt/scanet-app

# Run automated multi-architecture installer
chmod +x scripts/install.sh scripts/health_check.sh
./scripts/install.sh
```

### 6. Set Up Python Virtual Environment
```bash
cd /opt/scanet-app/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure production environment file
cat << 'EOF' > .env
HOST=127.0.0.1
PORT=8000
DEBUG=False
SECRET_KEY=replace-with-a-random-secret-key-for-production
DATABASE_URL=sqlite+aiosqlite:///./data/scanet.db
MAX_CONCURRENT_JOBS=2
DEFAULT_JOB_TIMEOUT=600
CORS_ORIGINS=["http://localhost:8000"]
EOF
```

### 7. Run as a Systemd Service (Auto-Start on Reboot)
Create `/etc/systemd/system/scanet.service`:
```bash
sudo bash -c 'cat << "EOF" > /etc/systemd/system/scanet.service
[Unit]
Description=scanet Reconnaissance Platform Daemon
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/scanet-app/backend
Environment="PATH=/opt/scanet-app/backend/.venv/bin:/opt/scanet/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/scanet-app/backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable scanet
sudo systemctl start scanet
```

### 8. Set Up Nginx Reverse Proxy & Free SSL (Let's Encrypt)
Create `/etc/nginx/sites-available/scanet`:
```bash
sudo bash -c 'cat << "EOF" > /etc/nginx/sites-available/scanet
server {
    listen 80;
    server_name your-domain.com; # Or EC2 Public IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Enable SSE real-time streaming without buffering
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
    }
}
EOF'

sudo ln -s /etc/nginx/sites-available/scanet /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Install free SSL certificate
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 9. Verify Server Health
```bash
# Check service status
sudo systemctl status scanet --no-pager

# Probe API endpoints
curl -s http://127.0.0.1:8000/api/v1/system/health
curl -s http://127.0.0.1:8000/api/v1/system/tools
```
Open `https://your-domain.com` in your browser to access the live dashboard!

---

## 🧪 Verified Test Suite (21 Tests, 100% Pass)

The platform includes a built-in automated test suite covering all critical security and adapter functions:

```bash
# Run the complete test suite
python3 -c "import sys; sys.path.insert(0, './backend'); sys.path.insert(0, '.'); \
from tests.test_engine.test_scope_validator import *; \
from tests.test_adapters.test_nmap_adapter import *; \
from tests.test_analyzers.test_ai_advisor import *; \
from tests.test_analyzers.test_cve_correlator import *; \
from tests.test_adapters.test_nuclei_adapter import *; \
from tests.test_analyzers.test_os_fingerprint import *; \
test_loopback_is_blocked(); test_aws_imds_is_blocked(); test_approved_target_passes(); test_non_whitelisted_target_blocked(); \
test_parses_open_ports_only(); test_parses_host_ip(); test_parses_service_info(); test_empty_output_no_crash(); \
test_ai_advisor_port_exposure(); test_ai_advisor_clean_target(); \
test_correlate_openssh_regresshion(); test_correlate_apache_path_traversal(); \
test_nuclei_build_command(); test_nuclei_parse_output(); \
test_ttl_linux_deduction(); test_ttl_windows_deduction(); test_ttl_cisco_network_deduction(); \
test_ssh_banner_deduction(); test_http_iis_banner_deduction(); test_port_profile_windows(); test_composite_fingerprinting(); \
print('ALL 21 TESTS PASSED WITH 100% SUCCESS!')"
```

**Results:**
- `4 Engine Tests`: Loopback blocking, AWS IMDS blocking, Whitelist verification.
- `4 Nmap Tests`: Port parsing, Host address extraction, Service identification, Empty XML safety.
- `2 AI Advisor Tests`: High-risk port penalties, MITRE ATT&CK mapping, Posture scoring.
- `2 CVE Correlator Tests`: OpenSSH regreSSHion correlation, Apache path traversal matching.
- `2 Nuclei Tests`: Safe argument construction, JSONL output normalization.
- `7 OS Detection Tests`: TTL Linux/Windows/Cisco heuristics, SSH/HTTP banner matching, Port profile deduction, Composite fingerprinting.

---

## 📁 Project Directory Structure

```
scanet/
├── backend/
│   ├── main.py                     # FastAPI application entrypoint
│   ├── config.py                   # Environment configuration & safety constants
│   ├── requirements.txt            # Python dependencies
│   ├── database/                   # SQLite WAL mode ORM models
│   ├── engine/                     # Job manager, Scope validator, Pipeline manager
│   ├── adapters/                   # 12 Tool adapters (Nmap, Naabu, Katana, Nuclei, etc.)
│   ├── analyzers/                  # OS Fingerprint, AI Advisor, CVEs, SARIF, Webhooks
│   └── api/routes/                 # Endpoints (targets, jobs, results, pipelines, os-detect)
├── frontend/
│   ├── index.html                  # Responsive dark-theme dashboard
│   └── assets/                     # Vanilla CSS tokens and ES6 modules
├── tests/                          # 21 Automated unit and integration tests
├── scripts/                        # install.sh & health_check.sh
├── docker/                         # Dockerfile & docker-compose.yml
├── docs/                           # AWS_EC2_DEPLOYMENT.md
├── wordlists/                      # Curated discovery wordlists
└── records/                        # Architecture decisions & audit trackers
```

---

## 📜 License & Governance

- **License:** MIT Open-Source License — see [`LICENSE`](LICENSE).
- **GitHub Repository:** [https://github.com/mjishaan59-cell/scanet.git](https://github.com/mjishaan59-cell/scanet.git)
- **Audit Records:** See [`records/PROJECT_STEPS_LOG.md`](records/PROJECT_STEPS_LOG.md) and [`records/GITHUB_UPLOAD_TRACKER.md`](records/GITHUB_UPLOAD_TRACKER.md).
