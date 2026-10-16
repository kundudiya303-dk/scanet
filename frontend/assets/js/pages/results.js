/**
 * scanet — Results Explorer & Multi-Format Report Center
 * Real API-backed implementation: loads discovered hosts, ports, and findings from DB.
 */
import { api } from '../api.js';

export async function renderResults(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Normalized Results &amp; Audit Findings</h2>
                <p style="color: var(--color-text-muted);">Inspect discovered hosts, open ports, identified services, and vulnerability findings.</p>
            </div>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <button class="btn btn-emerald" id="btn-export-pptx" style="box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);">📊 Export PPT Slides</button>
                <button class="btn btn-primary" id="btn-export-sarif">📥 Export SARIF</button>
                <button class="btn btn-secondary" id="btn-export-json">📥 Export JSON</button>
            </div>
        </div>

        <!-- Severity Summary Bar (real counts) -->
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 2rem;">
            <div class="card" style="border-left: 4px solid var(--color-rose); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">CRITICAL</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #f87171;" id="count-critical">—</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-amber); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">HIGH</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #fbbf24;" id="count-high">—</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-primary); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">MEDIUM</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8;" id="count-medium">—</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-emerald); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">LOW</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #34d399;" id="count-low">—</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-cyan); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">INFO</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #22d3ee;" id="count-info">—</div>
            </div>
        </div>

        <!-- Discovered Hosts & Ports Table -->
        <div class="card" style="margin-bottom: 2rem;">
            <div class="card-title">
                <span id="hosts-table-label">Discovered Hosts &amp; Service Fingerprints</span>
                <span class="badge badge-emerald">Live DB Results</span>
            </div>
            <div id="hosts-table-wrap" class="table-container">
                <div style="text-align:center; padding:1.5rem; color:var(--color-text-muted);">Loading scan results...</div>
            </div>
        </div>

        <!-- Security Findings Table -->
        <div class="card">
            <div class="card-title">
                <span id="findings-table-label">Security Findings</span>
                <span class="badge badge-rose">AI-Prioritized</span>
            </div>
            <div id="findings-table-wrap" class="table-container">
                <div style="text-align:center; padding:1.5rem; color:var(--color-text-muted);">Loading findings...</div>
            </div>
        </div>
    `;

    // Wire export buttons
    document.getElementById('btn-export-pptx').addEventListener('click', () => {
        window.open(api.exportResults('pptx'), '_blank');
    });
    document.getElementById('btn-export-sarif').addEventListener('click', () => {
        window.open(api.exportResults('sarif'), '_blank');
    });
    document.getElementById('btn-export-json').addEventListener('click', () => {
        window.open(api.exportResults('json'), '_blank');
    });

    await loadResults();
}


async function loadResults() {
    try {
        const [hostsData, findingsData] = await Promise.all([
            api.getHosts(),
            api.getFindings(),
        ]);

        // Populate severity counters
        const findings = findingsData.findings || [];
        document.getElementById('count-critical').textContent = findings.filter(f => f.severity === 'critical').length;
        document.getElementById('count-high').textContent     = findings.filter(f => f.severity === 'high').length;
        document.getElementById('count-medium').textContent   = findings.filter(f => f.severity === 'medium').length;
        document.getElementById('count-low').textContent      = findings.filter(f => f.severity === 'low').length;
        document.getElementById('count-info').textContent     = findings.filter(f => f.severity === 'info').length;

        // Hosts table
        const hostsWrap = document.getElementById('hosts-table-wrap');
        const hosts     = hostsData.hosts || [];
        document.getElementById('hosts-table-label').textContent =
            `Discovered Hosts & Service Fingerprints (${hosts.length} hosts)`;

        if (hosts.length === 0) {
            hostsWrap.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--color-text-muted);">
                No scan results yet. Run a scan job from the <a href="#/jobs" style="color:var(--color-primary);">Scan Launcher</a>.
            </div>`;
        } else {
            const rows = [];
            for (const h of hosts) {
                if (h.ports.length === 0) {
                    rows.push(`<tr>
                        <td><code>${escapeHtml(h.ip_address)}</code></td>
                        <td colspan="4" style="color:var(--color-text-muted);">No open ports detected</td>
                        <td><span class="badge badge-emerald">Low</span></td>
                    </tr>`);
                } else {
                    for (const p of h.ports) {
                        rows.push(`<tr>
                            <td><code>${escapeHtml(h.ip_address)}</code>${h.hostname ? `<br><span style="font-size:0.75rem;color:var(--color-text-muted);">${escapeHtml(h.hostname)}</span>` : ''}</td>
                            <td><code>${p.port_number}/${escapeHtml(p.protocol)}</code></td>
                            <td><strong>${escapeHtml(p.service_name || 'unknown')}</strong></td>
                            <td>${escapeHtml(p.product || '')} ${escapeHtml(p.version || '')}</td>
                            <td>${escapeHtml(h.os_fingerprint || '—')}</td>
                            <td>${portRiskBadge(p.port_number)}</td>
                        </tr>`);
                    }
                }
            }
            hostsWrap.innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Host IP</th>
                            <th>Port / Protocol</th>
                            <th>Service</th>
                            <th>Product &amp; Version</th>
                            <th>Detected OS</th>
                            <th>Risk</th>
                        </tr>
                    </thead>
                    <tbody>${rows.join('')}</tbody>
                </table>
            `;
        }

        // Findings table
        const findingsWrap = document.getElementById('findings-table-wrap');
        document.getElementById('findings-table-label').textContent =
            `Security Findings (${findings.length} total)`;

        if (findings.length === 0) {
            findingsWrap.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--color-text-muted);">
                No security findings recorded yet. Run a full scan or web audit to populate findings.
            </div>`;
        } else {
            const frows = findings.map(f => `<tr>
                <td>${severityBadge(f.severity)}</td>
                <td><span class="badge badge-indigo">${escapeHtml(f.category)}</span></td>
                <td><strong>${escapeHtml(f.title)}</strong></td>
                <td style="max-width:260px; font-size:0.82rem; color:var(--color-text-muted);">${escapeHtml(f.description)}</td>
                <td style="max-width:200px; font-size:0.82rem;">${escapeHtml(f.remediation || '—')}</td>
                <td style="font-size:0.78rem; color:var(--color-text-muted);">${f.created_at ? new Date(f.created_at).toLocaleDateString() : '—'}</td>
            </tr>`).join('');

            findingsWrap.innerHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Category</th>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Remediation</th>
                            <th>Detected</th>
                        </tr>
                    </thead>
                    <tbody>${frows}</tbody>
                </table>
            `;
        }

    } catch (err) {
        const wrap = document.getElementById('hosts-table-wrap');
        wrap.innerHTML = `<div style="color:#f87171; padding:1rem;">Failed to load results: ${escapeHtml(err.message)}</div>`;
    }
}


function portRiskBadge(port) {
    const critical = [21, 23, 445, 3389, 6379, 5900, 2375, 27017, 11211];
    const high     = [22, 3306, 5432, 1433, 8080, 8443, 9200];
    if (critical.includes(port)) return '<span class="badge badge-rose">Critical</span>';
    if (high.includes(port))     return '<span class="badge badge-amber">High</span>';
    return '<span class="badge badge-emerald">Low</span>';
}


function severityBadge(sev) {
    const map = {
        critical: 'badge-rose',
        high:     'badge-amber',
        medium:   'badge-indigo',
        low:      'badge-cyan',
        info:     'badge-emerald',
    };
    return `<span class="badge ${map[sev] || 'badge-indigo'}">${escapeHtml(sev?.toUpperCase() || 'INFO')}</span>`;
}


function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}
