# scanet 🔍

> **A Lightweight, Modular, Web-Based Cybersecurity Reconnaissance Toolkit**  
> Built for university labs, security education, and controlled infrastructure auditing.

---

## What is scanet?

`scanet` is a unified web platform that brings together essential open-source network reconnaissance, web discovery, DNS analysis, and HTTP inspection tools into a single clean graphical interface — removing the need to juggle multiple terminal windows and command-line flags.

It runs efficiently on low-resource virtual machines and cloud instances (1–2 GB RAM), making it ideal for academic environments.

---

## Features

- 🔌 **Modular Tool Adapters** — Nmap, Naabu, FFUF, dnsx, Subfinder, HTTPX, MTR
- 🔒 **Scope Enforcement** — Strict target whitelisting; blocks unauthorized scans
- 📡 **Live Job Streaming** — Real-time output via Server-Sent Events (SSE)
- 🧩 **Normalized Results Schema** — Unified JSON structure across all tools
- 📊 **Interactive Dashboard** — Status, metrics, topology graphs, and findings
- 📝 **Multi-Format Reports** — HTML, JSON, CSV, PDF, and SARIF export
- 🛡️ **Security-First** — Zero shell injection, SSRF protection, RBAC roles
- 🔁 **Auto-tracked Changes** — Every step documented in `records/`

---

## Project Structure

```
scanet/
├── backend/          # FastAPI backend, adapters, engine, database
├── frontend/         # Vanilla HTML/CSS/JS dashboard
├── wordlists/        # Curated wordlists for directory discovery
├── scripts/          # Install, health-check, and setup scripts
├── docker/           # Dockerfile and docker-compose configuration
├── tests/            # Unit, API, and integration tests
├── records/          # Audit trail, architecture decisions, change log
└── docs/             # Extended documentation
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/mjishaan59-cell/scanet.git
cd scanet

# 2. Run the installation script
chmod +x scripts/install.sh
./scripts/install.sh

# 3. Start the development server
cd backend
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 4. Open in browser
# http://localhost:8000
```

---

## Supported Platforms

| OS | Architecture | Status |
|---|---|---|
| Ubuntu 22.04 / 24.04 LTS | x86_64 / ARM64 | ✅ Supported |
| Debian 11 / 12 | x86_64 / ARM64 | ✅ Supported |
| Kali Linux 2024.x | x86_64 / ARM64 | ✅ Supported |
| Amazon Linux 2023 | x86_64 / ARM64 | ✅ Supported |
| Fedora 39 / 40 | x86_64 / ARM64 | ✅ Supported |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+ · FastAPI · Uvicorn · asyncio |
| Database | SQLite (WAL Mode) |
| Frontend | Vanilla HTML · CSS (Design Tokens) · ES6 Modules |
| Real-time | Server-Sent Events (SSE) |
| Process Mgmt | asyncio.create_subprocess_exec · Process Groups |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Repository

🔗 [github.com/mjishaan59-cell/scanet](https://github.com/mjishaan59-cell/scanet)
