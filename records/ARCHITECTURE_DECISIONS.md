# scanet — Architecture Decision Records (ADR)

This document formalizes critical design and engineering decisions made during the development of `scanet`.

---

### ADR-001: Backend Framework Selection — FastAPI over Django/Flask
- **Status:** Accepted
- **Context:** `scanet` needs to coordinate asynchronous subprocesses, stream real-time command output via Server-Sent Events (SSE), and maintain minimal RAM consumption on low-spec VMs ($< 1\text{–}2\text{ GB}$ RAM).
- **Decision:** Use Python 3.10+ with **FastAPI** and **Uvicorn**.
- **Rationale:** Native `asyncio` execution prevents blocking the web server during scans; automatic OpenAPI/Swagger documentation simplifies frontend integration; resident memory overhead is minimal ($\sim 95\text{ MB}$ compared to $> 250\text{ MB}$ for Django).

---

### ADR-002: Task Execution Architecture — Async Process Groups over Celery/Redis
- **Status:** Accepted
- **Context:** Traditional background workers (Celery) require external message brokers (Redis or RabbitMQ), adding 2–3 background services and significant RAM overhead.
- **Decision:** Implement native asynchronous process management using `asyncio.create_subprocess_exec` configured with dedicated Linux process groups (`os.setsid`).
- **Rationale:** Reduces deployment to a single self-contained application without message-broker daemons; allows deterministic cancellation of entire process trees using `os.killpg(pgid, signal.SIGTERM)`.

---

### ADR-003: Database Engine — SQLite with Write-Ahead Logging (WAL)
- **Status:** Accepted
- **Context:** An educational toolkit must be easily portable, quick to set up, and free of heavyweight database installation requirements.
- **Decision:** Use **SQLite** configured with `PRAGMA journal_mode=WAL` and foreign key enforcement.
- **Rationale:** Zero external database server to install or maintain; WAL mode allows concurrent readers while a scan writes results; database file can be backed up or inspected directly.

---

### ADR-004: Frontend Architecture — Modern Vanilla CSS & ES6 Modules
- **Status:** Accepted
- **Context:** Heavy single-page frameworks (Next.js, complex React toolchains) introduce multi-hundred megabyte `node_modules` folders, slow compilation times, and dependency churn.
- **Decision:** Use modern **Vanilla CSS** (design tokens, CSS Grid/Flexbox) with modular **Vanilla JavaScript (ES6 Modules)** and native `EventSource` for SSE streaming.
- **Rationale:** Near-zero build time, immediate browser rendering, extremely low memory usage on client and server, and simplified deployment without Node.js runtime dependencies.

---

### ADR-005: Command Execution Security — Structured Vector Arguments
- **Status:** Accepted
- **Context:** Wrapping CLI security tools is vulnerable to Command Injection (CWE-78) if user input is concatenated into shell strings.
- **Decision:** Strictly ban `shell=True`, `/bin/sh`, and raw string formatting for command construction. Enforce argument arrays (`execve`-style parameter lists).
- **Rationale:** Completely eliminates shell metacharacter interpretation (`;`, `&&`, `|`, `` ` ``), preventing command injection by design.

---

### ADR-006: Target Scope & Cloud Metadata Guardrails
- **Status:** Accepted
- **Context:** Educational platforms deployed on cloud nodes (e.g., AWS EC2) run the risk of unauthorized scanning or SSRF attacks targeting instance metadata (`169.254.169.254`).
- **Decision:** Programmatically enforce target validation: restrict scans strictly to whitelisted private ranges (RFC 1918) or approved domains; permanently hard-block `169.254.169.254`, `127.0.0.0/8`, and link-local ranges.
- **Rationale:** Guarantees compliance with cloud provider policies and prevents students or attackers from weaponizing the server against internal infrastructure.

---

### ADR-007: Chained Multi-Tool Reconnaissance Pipelines (Playbooks)
- **Status:** Accepted
- **Context:** Individual manual tool executions are inefficient for holistic attack surface discovery. Students and security analysts require reproducible end-to-end workflows (e.g., Subdomain Discovery -> DNS Resolution -> Port Scanning -> HTTP Inspection -> Vulnerability Auditing).
- **Decision:** Implement sequential multi-stage pipeline orchestration (`PipelineManager`) that automatically feeds outputs of discovery tools into downstream analyzers.
- **Rationale:** Mimics modern attack surface frameworks (reNgine, reconFTW) while maintaining process-group safety, deterministic timeouts, and granular stage progress tracking.

---

### ADR-008: AI Security Advisory & Heuristic Rule Expert System
- **Status:** Accepted
- **Context:** Raw tool outputs (e.g., port numbers, raw HTTP headers) are overwhelming for students and lack contextualized risk explanations. However, requiring mandatory third-party LLM API keys (OpenAI/Anthropic) breaks self-contained offline lab deployments.
- **Decision:** Build a zero-dependency offline **Heuristic Expert Advisory Engine** (`AISecurityAdvisor`) that maps open ports and misconfigurations to **MITRE ATT&CK TTPs**, CVSS scores, and educational remediation playbooks, while providing a pluggable hook for local offline models (Ollama).
- **Rationale:** Guarantees 100% functionality in offline university intranet environments with zero token costs and zero latency, while still providing high-impact intelligent guidance.

---

### ADR-009: OASIS SARIF v2.1.0 Standard Compliance for DevSecOps
- **Status:** Accepted
- **Context:** University capstone projects and modern security platforms must integrate seamlessly with enterprise CI/CD pipelines and security dashboards (GitHub Security, GitLab, DefectDojo).
- **Decision:** Implement native OASIS SARIF v2.1.0 generation in `backend/analyzers/sarif_exporter.py` alongside standard JSON, HTML, PDF, and CSV exports.
- **Rationale:** Enables direct automated upload of scanet findings into GitHub Code Scanning Alerts and modern DevSecOps vulnerability management systems.

---

### ADR-010: Unprivileged Multi-Vector OS Detection Engine
- **Status:** Accepted
- **Context:** Traditional raw socket OS fingerprinting (e.g., Nmap `-O`) requires root privileges (`CAP_NET_RAW` or `sudo`), which compromises web service process security, causes container failures, and triggers cloud hypervisor abuse alarms.
- **Decision:** Implement a layered, unprivileged heuristic OS detection engine (`OSFingerprintEngine`) combining IP TTL distance analysis, service banner regex extraction (SSH, HTTP Server, FTP, SMB), and open port portfolio profiling (Windows NetBIOS/SMB/RDP vs Linux SSH/NFS).
- **Rationale:** Delivers high-accuracy operating system identification with zero root privilege requirements, zero raw socket dependencies, and full container/cloud compatibility.


