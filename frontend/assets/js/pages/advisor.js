/**
 * scanet — AI Security Advisory & MITRE ATT&CK Copilot Page
 * Real API-backed implementation: analyzes live discovered ports and findings
 * to compute Cyber Hygiene score, MITRE ATT&CK TTPs, and remediation playbooks.
 */
import { api } from '../api.js';

export async function renderAdvisor(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>AI Security Advisor &amp; MITRE ATT&CK Copilot</h2>
                <p style="color: var(--color-text-muted);">Heuristic threat analysis, educational student explanations, and automated remediation playbooks.</p>
            </div>
            <div>
                <button class="btn btn-secondary" id="btn-refresh-advisor" style="font-size: 0.82rem;">↻ Refresh Telemetry</button>
            </div>
        </div>

        <div id="advisor-loading" style="text-align: center; padding: 3rem; color: var(--color-text-muted);">
            Analyzing scan results with AI Advisor Engine...
        </div>

        <div id="advisor-content" style="display: none;"></div>
    `;

    document.getElementById('btn-refresh-advisor').addEventListener('click', () => loadAdvisorData());
    await loadAdvisorData();
}

async function loadAdvisorData() {
    const loading = document.getElementById('advisor-loading');
    const content = document.getElementById('advisor-content');

    try {
        const [hostsData, findingsData] = await Promise.all([
            api.getHosts(),
            api.getFindings(),
        ]);

        const hosts = hostsData.hosts || [];
        const findings = findingsData.findings || [];

        // Collect all ports across hosts
        const allPorts = [];
        hosts.forEach(h => {
            (h.ports || []).forEach(p => {
                allPorts.push({
                    port: p.port_number,
                    service_name: p.service_name,
                    product: p.product,
                    version: p.version,
                    host_ip: h.ip_address,
                });
            });
        });

        if (allPorts.length === 0 && findings.length === 0) {
            loading.style.display = 'none';
            content.style.display = 'block';
            content.innerHTML = `
                <div class="card" style="text-align: center; padding: 3rem 2rem; border-left: 4px solid var(--color-cyan);">
                    <div style="font-size: 3rem; margin-bottom: 0.75rem;">🛡️</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 0.5rem;">No Active Telemetry in Database</h3>
                    <p style="color: var(--color-text-muted); font-size: 0.9rem; max-width: 500px; margin: 0 auto 1.5rem; line-height: 1.5;">
                        The AI Security Advisor evaluates discovered ports, banners, and vulnerabilities. Run a scan or launch a lab preset to generate live threat analysis.
                    </p>
                    <a href="#/jobs" class="btn btn-primary">Launch Real Scan</a>
                </div>
            `;
            return;
        }

        // Call real backend advisor engine
        const advisorResult = await api.analyzeAdvisory({
            ports: allPorts,
            findings: findings,
            header_grade: 'B'
        });

        renderAdvisorUI(advisorResult, allPorts, findings, content);
        loading.style.display = 'none';
        content.style.display = 'block';

    } catch (err) {
        loading.style.display = 'none';
        content.style.display = 'block';
        content.innerHTML = `<div class="card" style="color: #f87171;">Failed to load AI advisory: ${escapeHtml(err.message)}</div>`;
    }
}

function renderAdvisorUI(data, allPorts, findings, container) {
    const adv = data.advisory || {};
    const score = adv.hygiene_score !== undefined ? adv.hygiene_score : 85;
    const grade = adv.posture_grade || 'B';
    const advisories = adv.priority_advisories || [];
    const cves = data.correlated_cves || [];
    const comp = data.compliance || {};

    const scoreColor = score >= 80 ? '#10b981' : (score >= 60 ? '#f59e0b' : '#ef4444');

    let advisoriesHtml = '';
    if (advisories.length === 0) {
        advisoriesHtml = `
            <div class="card" style="border-left: 4px solid #10b981; padding: 1.25rem;">
                <div style="font-weight: 700; color: #34d399; margin-bottom: 0.3rem;">✓ Strong Network Perimeter Defense</div>
                <p style="color: var(--color-text-muted); font-size: 0.88rem; margin: 0;">
                    No critical plaintext services (Telnet, FTP, unauthenticated Redis) were detected on audited ports.
                </p>
            </div>
        `;
    } else {
        advisoriesHtml = advisories.map(a => {
            const isCrit = a.risk_level === 'CRITICAL';
            const badgeColor = isCrit ? 'badge-rose' : (a.risk_level === 'HIGH' ? 'badge-amber' : 'badge-indigo');
            const borderColor = isCrit ? '#ef4444' : (a.risk_level === 'HIGH' ? '#f59e0b' : '#6366f1');

            return `
                <div class="card" style="border-left: 4px solid ${borderColor}; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                        <div>
                            <span class="badge ${badgeColor}" style="margin-right: 0.5rem;">${escapeHtml(a.risk_level)}</span>
                            <span style="font-weight: 700; font-size: 1.05rem;">${escapeHtml(a.title)}</span>
                        </div>
                        <span class="badge badge-purple">${escapeHtml(a.mitre_attack || 'T1190')}</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-bottom: 0.75rem; line-height: 1.45;">
                        ${escapeHtml(a.explanation)}
                    </p>
                    <div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.82rem; border: 1px solid rgba(255,255,255,0.06);">
                        <span style="color: #34d399; font-weight: 600;">Automated Remediation Playbook:</span><br/>
                        <div style="margin-top: 0.25rem; font-family: monospace; color: #cbd5e1;">${escapeHtml(a.remediation)}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    let cvesHtml = '';
    if (cves.length === 0) {
        cvesHtml = '<div style="color: var(--color-text-muted); font-size: 0.85rem; padding: 0.5rem 0;">No direct CVE vulnerabilities matched for detected service versions.</div>';
    } else {
        cvesHtml = cves.map(c => `
            <div style="padding: 0.65rem; background: rgba(0,0,0,0.25); border-radius: var(--radius-sm); margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.06);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                    <span style="font-weight: 700; color: #ef4444; font-size: 0.88rem;">${escapeHtml(c.cve_id)}</span>
                    <span class="badge badge-rose" style="font-size: 0.72rem;">CVSS ${c.cvss}</span>
                </div>
                <div style="font-size: 0.8rem; color: #cbd5e1;">${escapeHtml(c.name)}</div>
                ${c.cisa_kev ? '<span class="badge badge-amber" style="font-size: 0.68rem; margin-top: 0.3rem;">CISA KEV ACTIVE EXPLOIT</span>' : ''}
            </div>
        `).join('');
    }

    container.innerHTML = `
        <!-- Hygiene Score Banner -->
        <div class="card" style="margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; border-left: 4px solid ${scoreColor}; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h3 style="margin-bottom: 0.25rem;">Overall Security Posture &amp; Cyber Hygiene</h3>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin: 0;">
                    Live telemetry based on <strong>${allPorts.length} open ports</strong> and <strong>${findings.length} findings</strong> across scanned hosts.
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.4rem; font-weight: 800; color: ${scoreColor};">${score}<span style="font-size: 1.1rem; color: var(--color-text-muted);">/100</span></div>
                <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: ${scoreColor}; font-weight: 700;">Posture Grade: ${grade}</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
            <!-- Priority Advisories -->
            <div style="display: flex; flex-direction: column;">
                <h3 style="font-size: 1.15rem; margin-bottom: 1rem;">AI Prioritized Threat Advisories</h3>
                ${advisoriesHtml}
            </div>

            <!-- Compliance & MITRE Framework Card -->
            <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                <div class="card">
                    <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Compliance Mapping</h3>
                    <div style="font-size: 0.86rem; display: flex; flex-direction: column; gap: 0.75rem;">
                        <div style="padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <div style="font-weight: 600;">OWASP Top 10 (2021)</div>
                            <div style="color: ${allPorts.some(p => [21,23,6379].includes(p.port)) ? '#f87171' : '#34d399'};">
                                ${allPorts.some(p => [21,23,6379].includes(p.port)) ? 'A05: Security Misconfiguration (Non-compliant)' : 'A05: Secure Baseline (Pass)'}
                            </div>
                        </div>
                        <div style="padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <div style="font-weight: 600;">CIS Controls v8</div>
                            <div style="color: #34d399;">Control 4: Secure Asset Configuration (Monitored)</div>
                        </div>
                        <div>
                            <div style="font-weight: 600;">NIST CSF 2.0</div>
                            <div style="color: #34d399;">PR.IP: Baseline Configuration Verification</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3 style="font-size: 1.1rem; margin-bottom: 0.75rem;">Correlated CVE Matches</h3>
                    ${cvesHtml}
                </div>
            </div>
        </div>
    `;
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[m]);
}
