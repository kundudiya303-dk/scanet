/**
 * scanet — Web Security & Misconfiguration Auditor Page
 * Nikto & OWASP ZAP equivalent web security auditing interface.
 */
import { api } from '../api.js';

export async function renderWebAudit(container) {
    container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem;">
            <div>
                <h1 style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.4rem;">
                    Web Security & Misconfiguration Auditor
                </h1>
                <p style="color: var(--color-text-muted); font-size: 0.95rem; max-width: 720px;">
                    Lightweight unprivileged web scanner testing HTTP methods, sensitive file leaks (.env, .git), cookie security flags, CORS policies, and subdomain takeover signatures.
                </p>
            </div>
            <div style="display: flex; gap: 0.75rem;">
                <span class="badge badge-cyan">NIKTO / ZAP ENGINE</span>
                <span class="badge badge-emerald">ZERO-EXPLOIT SAFE</span>
            </div>
        </div>

        <!-- Target Input & Launch Bar -->
        <div class="card" style="margin-bottom: 2rem;">
            <div style="display: grid; grid-template-columns: 1fr auto; gap: 1rem; align-items: flex-end;">
                <div>
                    <label style="display: block; font-size: 0.85rem; font-weight: 600; color: var(--color-text-muted); margin-bottom: 0.4rem;">
                        Target Web URL (HTTP / HTTPS)
                    </label>
                    <input type="text" id="target-web-url" class="input" placeholder="http://127.0.0.1:8000 or http://target-lab.local" value="http://127.0.0.1:8000" />
                </div>
                <div>
                    <button id="btn-start-audit" class="btn btn-primary" style="height: 44px; padding: 0 1.5rem;">
                        ⚡ Start Web Audit
                    </button>
                </div>
            </div>
        </div>

        <!-- Audit Progress / Status Indicator (Hidden by default) -->
        <div id="audit-loading" class="card" style="display: none; text-align: center; padding: 2.5rem 1rem; margin-bottom: 2rem;">
            <div class="loader-spinner" style="margin: 0 auto 1rem;"></div>
            <h3 style="font-size: 1.1rem; margin-bottom: 0.3rem;">Auditing Web Security Surface...</h3>
            <p style="color: var(--color-text-muted); font-size: 0.85rem;">Probing HTTP methods, sensitive endpoints, cookie directives, and CORS headers...</p>
        </div>

        <!-- Audit Results Container -->
        <div id="audit-results-area" style="display: none;"></div>

        <!-- Secondary Subdomain Takeover & DNS Checker Card -->
        <div class="card" style="margin-top: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h3 style="font-size: 1.15rem; font-weight: 700;">Subdomain Takeover & DNS Dangling Record Checker</h3>
                    <p style="color: var(--color-text-muted); font-size: 0.85rem;">Inspects CNAME records for orphaned pointers to AWS S3, GitHub Pages, Heroku, Shopify, and Azure.</p>
                </div>
                <span class="badge badge-purple">AMASS / SUBJACK EQUIVALENT</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: flex-end;">
                <div>
                    <label style="font-size: 0.82rem; color: var(--color-text-muted); display: block; margin-bottom: 0.3rem;">Target Subdomain</label>
                    <input type="text" id="takeover-domain" class="input" placeholder="docs.example.com" />
                </div>
                <div>
                    <label style="font-size: 0.82rem; color: var(--color-text-muted); display: block; margin-bottom: 0.3rem;">Observed CNAME (Optional)</label>
                    <input type="text" id="takeover-cname" class="input" placeholder="example.github.io or s3.amazonaws.com" />
                </div>
                <div>
                    <button id="btn-check-takeover" class="btn btn-secondary" style="height: 44px;">
                        🔍 Verify Takeover
                    </button>
                </div>
            </div>
            <div id="takeover-result-box" style="margin-top: 1rem; display: none;"></div>
        </div>
    `;

    const btnStart = document.getElementById('btn-start-audit');
    const inputUrl = document.getElementById('target-web-url');
    const loadingArea = document.getElementById('audit-loading');
    const resultsArea = document.getElementById('audit-results-area');

    btnStart.addEventListener('click', async () => {
        const url = inputUrl.value.trim();
        if (!url) return;

        btnStart.disabled = true;
        loadingArea.style.display = 'block';
        resultsArea.style.display = 'none';

        try {
            const resp = await api.scanWebSecurity(url);
            renderAuditReport(resp.data, resultsArea);
            resultsArea.style.display = 'block';
        } catch (err) {
            resultsArea.innerHTML = `
                <div class="card" style="border-color: rgba(244, 63, 94, 0.4); background: rgba(244, 63, 94, 0.08);">
                    <h3 style="color: var(--color-rose); margin-bottom: 0.5rem;">Audit Failed</h3>
                    <p style="color: var(--color-text-muted); font-size: 0.9rem;">${err.message}</p>
                </div>
            `;
            resultsArea.style.display = 'block';
        } finally {
            btnStart.disabled = false;
            loadingArea.style.display = 'none';
        }
    });

    // Subdomain takeover event handler
    const btnTakeover = document.getElementById('btn-check-takeover');
    const inputDomain = document.getElementById('takeover-domain');
    const inputCname = document.getElementById('takeover-cname');
    const takeoverBox = document.getElementById('takeover-result-box');

    btnTakeover.addEventListener('click', async () => {
        const domain = inputDomain.value.trim();
        const cname = inputCname.value.trim();
        if (!domain) return;

        btnTakeover.disabled = true;
        takeoverBox.style.display = 'block';
        takeoverBox.innerHTML = '<span style="color:var(--color-cyan)">Testing CNAME signatures...</span>';

        try {
            const res = await api.checkTakeover(domain, cname);
            const data = res.data;
            if (data.is_vulnerable) {
                takeoverBox.innerHTML = `
                    <div style="padding: 1rem; border-radius: var(--radius-sm); background: rgba(244, 63, 94, 0.15); border: 1px solid var(--color-rose);">
                        <div style="color: var(--color-rose); font-weight: 700; margin-bottom: 0.3rem;">⚠️ POTENTIAL SUBDOMAIN TAKEOVER DETECTED (${data.provider})</div>
                        <p style="font-size: 0.85rem; color: #fff; margin-bottom: 0.4rem;">Fingerprint matched: <code>${data.fingerprint_matched}</code></p>
                        <p style="font-size: 0.8rem; color: var(--color-text-muted);">${data.remediation}</p>
                    </div>
                `;
            } else {
                takeoverBox.innerHTML = `
                    <div style="padding: 1rem; border-radius: var(--radius-sm); background: rgba(16, 185, 129, 0.12); border: 1px solid var(--color-emerald);">
                        <div style="color: var(--color-emerald); font-weight: 700;">✓ Domain Secure / No Takeover Signatures Found</div>
                        <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.2rem;">CNAME: ${data.cname || 'None detected'}</p>
                    </div>
                `;
            }
        } catch (e) {
            takeoverBox.innerHTML = `<span style="color:var(--color-rose)">Error: ${e.message}</span>`;
        } finally {
            btnTakeover.disabled = false;
        }
    });
}

function renderAuditReport(data, container) {
    const gradeColor = data.security_grade.startsWith('A') ? 'var(--color-emerald)' :
                       data.security_grade.startsWith('B') ? 'var(--color-cyan)' :
                       data.security_grade.startsWith('C') ? 'var(--color-amber)' : 'var(--color-rose)';

    container.innerHTML = `
        <!-- Grade & Overview Grid -->
        <div style="display: grid; grid-template-columns: 240px 1fr; gap: 1.5rem; margin-bottom: 2rem;">
            <!-- Grade Card -->
            <div class="card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; border-color: ${gradeColor};">
                <div style="font-size: 4.5rem; font-weight: 900; line-height: 1; color: ${gradeColor}; text-shadow: 0 0 25px ${gradeColor}; margin-bottom: 0.4rem;">
                    ${data.security_grade}
                </div>
                <div style="font-size: 0.95rem; font-weight: 700; color: ${gradeColor}; letter-spacing: 0.05em;">
                    ${data.security_rating}
                </div>
                <div style="font-size: 0.8rem; color: var(--color-text-muted); margin-top: 0.5rem;">
                    Security Score: ${data.security_score}/100
                </div>
            </div>

            <!-- Finding Breakdown & Telemetry -->
            <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.3rem;">Audit Target: ${data.target_url}</h3>
                    <p style="color: var(--color-text-muted); font-size: 0.85rem; margin-bottom: 1rem;">
                        Server Banner: <code style="color: var(--color-cyan);">${data.server_banner}</code> | HTTP Status: <strong>${data.status_code}</strong>
                    </p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                    <div style="padding: 0.75rem; border-radius: var(--radius-sm); background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.25);">
                        <div style="font-size: 0.75rem; color: var(--color-text-muted);">Critical</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-rose);">${data.counts.critical}</div>
                    </div>
                    <div style="padding: 0.75rem; border-radius: var(--radius-sm); background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.25);">
                        <div style="font-size: 0.75rem; color: var(--color-text-muted);">High</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-amber);">${data.counts.high}</div>
                    </div>
                    <div style="padding: 0.75rem; border-radius: var(--radius-sm); background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.25);">
                        <div style="font-size: 0.75rem; color: var(--color-text-muted);">Medium</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-cyan);">${data.counts.medium}</div>
                    </div>
                    <div style="padding: 0.75rem; border-radius: var(--radius-sm); background: rgba(255, 255, 255, 0.04); border: 1px solid var(--color-border);">
                        <div style="font-size: 0.75rem; color: var(--color-text-muted);">Low</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #fff;">${data.counts.low}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section 1: Sensitive File Exposure -->
        <div class="card" style="margin-bottom: 2rem;">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">📁 Sensitive Endpoints & File Exposures</h3>
            <p style="color: var(--color-text-muted); font-size: 0.85rem; margin-bottom: 1.25rem;">
                Probed common environment variables, version control artifacts, sitemaps, and server diagnostic scripts.
            </p>
            ${renderSensitiveFilesTable(data.sensitive_exposures)}
        </div>

        <!-- Section 2: HTTP Methods & CORS Policy -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
            <!-- HTTP Methods Card -->
            <div class="card">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">🔌 HTTP Methods Analysis</h3>
                <div style="font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 1rem;">
                    Advertised Methods: <strong>${data.methods_audit.allowed_methods.join(', ') || 'Standard GET/POST'}</strong>
                </div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    ${data.methods_audit.tested_methods.map(m => {
                        const isInsecure = data.methods_audit.insecure_methods.includes(m);
                        const isAllowed = data.methods_audit.allowed_methods.includes(m) || ['GET', 'POST', 'HEAD'].includes(m);
                        const cls = isInsecure ? 'badge-rose' : (isAllowed ? 'badge-cyan' : 'badge-emerald');
                        return `<span class="badge ${cls}">${m} ${isInsecure ? '⚠️' : ''}</span>`;
                    }).join('')}
                </div>
            </div>

            <!-- CORS Card -->
            <div class="card">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">🌐 Cross-Origin (CORS) Policy</h3>
                <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 0.8rem;">
                    Origin Header: <code>${data.cors_audit.allow_origin}</code> | Credentials: <code>${data.cors_audit.allow_credentials}</code>
                </p>
                <div>
                    ${data.cors_audit.is_misconfigured 
                        ? '<span class="badge badge-rose">⚠️ MISCONFIGURED CORS DETECTED</span>' 
                        : '<span class="badge badge-emerald">✓ STRICT CORS CONFIGURED</span>'}
                </div>
            </div>
        </div>

        <!-- Section 3: Comprehensive Findings & Remediations -->
        <div class="card">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem;">🛡️ Actionable Remediation Guidance</h3>
            ${renderFindingsList(data.all_findings)}
        </div>
    `;
}

function renderSensitiveFilesTable(files) {
    if (!files || files.length === 0) {
        return `
            <div style="padding: 1.5rem; text-align: center; color: var(--color-emerald); background: rgba(16, 185, 129, 0.08); border-radius: var(--radius-sm); border: 1px solid rgba(16, 185, 129, 0.2);">
                ✓ No sensitive files or source code repositories exposed (.env, .git, backups verified protected).
            </div>
        `;
    }

    return `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th>Resource Path</th>
                    <th>Classification</th>
                    <th>Status</th>
                    <th>Severity</th>
                    <th>Risk & Action</th>
                </tr>
            </thead>
            <tbody>
                ${files.map(f => `
                    <tr>
                        <td><code>${f.path}</code></td>
                        <td>${f.name}</td>
                        <td><span class="badge ${f.status === 200 ? 'badge-rose' : 'badge-amber'}">HTTP ${f.status}</span></td>
                        <td><span class="badge badge-${f.severity === 'CRITICAL' ? 'rose' : (f.severity === 'HIGH' ? 'amber' : 'cyan')}">${f.severity}</span></td>
                        <td style="font-size: 0.85rem; color: var(--color-text-muted);">${f.risk}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function renderFindingsList(findings) {
    if (!findings || findings.length === 0) {
        return '<p style="color: var(--color-emerald);">No security issues discovered. Target passed all baseline web checks.</p>';
    }

    return findings.map(f => {
        const sevColor = f.severity === 'CRITICAL' ? 'var(--color-rose)' :
                         f.severity === 'HIGH' ? 'var(--color-amber)' :
                         f.severity === 'MEDIUM' ? 'var(--color-cyan)' : 'var(--color-text-dim)';
        return `
            <div style="padding: 1rem; margin-bottom: 0.75rem; border-radius: var(--radius-sm); background: rgba(255, 255, 255, 0.02); border-left: 4px solid ${sevColor}; border: 1px solid rgba(255, 255, 255, 0.06); border-left-width: 4px; border-left-color: ${sevColor};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                    <strong style="color: #fff; font-size: 0.95rem;">${f.title}</strong>
                    <span class="badge" style="background: rgba(255,255,255,0.08); color: ${sevColor};">${f.severity}</span>
                </div>
                <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 0.4rem;">${f.description}</p>
                <div style="font-size: 0.82rem; color: var(--color-cyan);"><strong>Remediation:</strong> ${f.remediation}</div>
            </div>
        `;
    }).join('');
}
