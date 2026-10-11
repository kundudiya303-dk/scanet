# scanet — Tool Integration Matrix & Status Registry

This registry tracks the implementation, adapter status, and verification of all supported tools in `scanet`.

---

## 1. Tool Implementation Matrix

| Tool Name | Category | Tier | Implementation Status | Adapter Location | Output Normalization | Verification Status |
|---|---|---|---|---|---|---|
| **Nmap** | Port Scanning & Services | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/nmap_adapter.py` | XML to JSON via `defusedxml` | Pending |
| **Naabu** | Fast Port Discovery | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/naabu_adapter.py` | Streaming JSON | Pending |
| **FFUF** | Web Directory Discovery | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/ffuf_adapter.py` | Native JSON (`-of json`) | Pending |
| **dnsx** | DNS Analysis & Resolution | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/dnsx_adapter.py` | Streaming JSON | Pending |
| **Subfinder** | Passive Subdomain Recon | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/subfinder_adapter.py` | Streaming JSON | Pending |
| **HTTPX** | HTTP Inspection & Tech | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/httpx_adapter.py` | Streaming JSON | Pending |
| **MTR** | Hop-by-Hop Diagnostics | **Tier 1 (Core)** | Planned (Phase 2) | `scanet/adapters/mtr_adapter.py` | Native JSON (`--json`) | Pending |
| **Native Headers** | HTTP Security Header Audit | **Tier 1 (Built-in)** | Planned (Phase 2) | `scanet/analyzers/headers.py` | Direct Grade (A+ to F) | Pending |
| **Native SSL** | Certificate Expiry & Chain | **Tier 1 (Built-in)** | Planned (Phase 2) | `scanet/analyzers/ssl_cert.py` | Direct JSON | Pending |
| **Native Subnet** | CIDR Math & Subnet Info | **Tier 1 (Built-in)** | Planned (Phase 2) | `scanet/analyzers/subnet.py` | Direct JSON | Pending |
| **Native Diff** | Scan Comparison Engine | **Tier 1 (Built-in)** | Planned (Phase 3) | `scanet/analyzers/diff.py` | Delta JSON | Pending |
| **testssl.sh** | Deep TLS Cipher Auditing | **Tier 2 (Ext)** | Planned (Post-MVP) | `scanet/adapters/testssl_adapter.py` | Native JSON | Pending |
| **Nuclei** | Curated Vulnerability Audit | **Tier 2 (Ext)** | Planned (Post-MVP) | `scanet/adapters/nuclei_adapter.py` | Streaming JSON | Pending |
| **WhatWeb** | CMS & Tech Fingerprint | **Tier 2 (Ext)** | Planned (Post-MVP) | `scanet/adapters/whatweb_adapter.py` | Native JSON | Pending |

---

## 2. Status Definitions
- **Planned:** Architecture defined, awaiting phase implementation.
- **In Development:** Adapter code under active construction.
- **Testing:** Implemented and undergoing unit testing and mock/live scan validation.
- **Production Ready:** Verified, unit-tested, and actively integrated into dashboard UI.
