"""
scanet API — AI Security Advisory, MITRE ATT&CK & Compliance Routes
Provides heuristic & AI remediation advice, CVE correlation, and compliance mapping.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from analyzers.ai_advisor import AISecurityAdvisor, PORT_RISK_KNOWLEDGE
from analyzers.cve_correlator import correlate_service_cves
from analyzers.compliance import map_findings_to_compliance
from typing import Dict, Any

router = APIRouter()
advisor_engine = AISecurityAdvisor()


@router.post("/analyze")
async def analyze_scan_results(payload: dict):
    """
    Analyzes normalized scan results:
    - Calculates Cyber Hygiene Score (0 - 100)
    - Generates student-friendly remediation steps
    - Maps findings to MITRE ATT&CK TTPs
    - Correlates known CVEs and CISA KEV entries
    - Audits compliance against OWASP Top 10 and CIS Controls
    """
    ports = payload.get("ports", [])
    header_grade = payload.get("header_grade", "B")
    findings = payload.get("findings", [])

    # 1. Run Heuristic AI Advisory Analysis
    advisory_report = advisor_engine.analyze_findings({
        "ports": ports,
        "header_grade": header_grade
    })

    # 2. Correlate detected software versions with CVEs
    correlated_cves = []
    for p in ports:
        product = p.get("product") or p.get("service_name")
        version = p.get("version", "")
        if product:
            cves = correlate_service_cves(product, version)
            correlated_cves.extend(cves)

    # 3. Map to Compliance Frameworks
    compliance_report = map_findings_to_compliance(findings, header_grade)

    return {
        "status": "success",
        "advisory": advisory_report,
        "correlated_cves": correlated_cves,
        "compliance": compliance_report
    }


@router.get("/mitre-knowledge")
async def get_mitre_knowledge():
    """
    Returns the built-in MITRE ATT&CK port knowledge base.
    """
    return PORT_RISK_KNOWLEDGE
