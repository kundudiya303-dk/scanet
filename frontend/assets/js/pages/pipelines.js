/**
 * scanet — Chained Reconnaissance Pipelines & Playbooks Page
 * Live API-backed multi-stage attack surface workflow execution.
 */
import { api } from '../api.js';

export async function renderPipelines(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Reconnaissance Pipelines &amp; Playbooks</h2>
                <p style="color: var(--color-text-muted);">Execute multi-tool automated attack surface workflows in sequence.</p>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <label style="font-size: 0.82rem; color: var(--color-text-muted);">Target Scope:</label>
                <select id="pipeline-target-select" class="input" style="width: auto; padding: 0.4rem 0.8rem; font-size: 0.85rem;">
                    <option value="">Loading targets...</option>
                </select>
            </div>
        </div>

        <div id="pipeline-status-card" class="card" style="margin-bottom: 2rem; border-left: 4px solid var(--color-emerald); display: none;">
            <div class="card-title">
                <span id="active-pipe-title">Pipeline Execution in Progress</span>
                <span class="badge badge-emerald"><span class="badge-pulse"></span> EXECUTING</span>
            </div>
            <div id="active-pipe-details" style="font-size: 0.88rem; color: var(--color-text-muted); margin-bottom: 1rem;"></div>
            <div id="pipe-stages-list" style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1.25rem;"></div>
            <div style="display: flex; gap: 0.75rem;">
                <a href="#/jobs" class="btn btn-primary" style="font-size: 0.82rem;">▷ Monitor Live Stream in Job Center</a>
                <button class="btn btn-secondary" id="btn-close-pipeline-status" style="font-size: 0.82rem;">Dismiss</button>
            </div>
        </div>

        <div class="card-grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); margin-bottom: 2rem;">
            <!-- Pipeline 1 -->
            <div class="card" style="border-left: 4px solid var(--color-accent); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.1rem; margin: 0;">Full Attack Surface Recon</h3>
                        <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">6 Tools</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-bottom: 1rem; line-height: 1.45;">
                        Passive Subdomain Discovery ➔ DNS Resolution ➔ Fast Port Screening ➔ Nmap Services ➔ HTTPX Probing ➔ Nuclei Audit.
                    </p>
                    <div style="font-size: 0.78rem; background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; font-family: monospace; color: #38bdf8;">
                        subfinder ➔ dnsx ➔ naabu ➔ nmap ➔ httpx ➔ nuclei
                    </div>
                </div>
                <button class="btn btn-primary btn-launch-pipe" data-preset="full_recon" data-name="Full Attack Surface Recon" data-primary-tool="nmap">Launch Full Pipeline</button>
            </div>

            <!-- Pipeline 2 -->
            <div class="card" style="border-left: 4px solid #10b981; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.1rem; margin: 0;">Web App Security Audit</h3>
                        <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">4 Tools</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-bottom: 1rem; line-height: 1.45;">
                        Deep Crawler ➔ Web Directory Fuzzing ➔ TLS &amp; Security Headers ➔ Misconfiguration Auditing.
                    </p>
                    <div style="font-size: 0.78rem; background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; font-family: monospace; color: #34d399;">
                        katana ➔ ffuf ➔ httpx ➔ nuclei
                    </div>
                </div>
                <button class="btn btn-secondary btn-launch-pipe" data-preset="web_security" data-name="Web App Security Audit" data-primary-tool="httpx">Launch Web Pipeline</button>
            </div>

            <!-- Pipeline 3 -->
            <div class="card" style="border-left: 4px solid #f59e0b; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.1rem; margin: 0;">Network Route &amp; Diagnostics</h3>
                        <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">3 Tools</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-bottom: 1rem; line-height: 1.45;">
                        MTR Hop Latency ➔ All-Port Screening ➔ Service Version Probing ➔ Subnet CIDR Calculation.
                    </p>
                    <div style="font-size: 0.78rem; background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; font-family: monospace; color: #fbbf24;">
                        mtr ➔ naabu ➔ nmap ➔ subnet
                    </div>
                </div>
                <button class="btn btn-secondary btn-launch-pipe" data-preset="network_diagnostic" data-name="Network Diagnostics" data-primary-tool="nmap">Launch Diagnostics</button>
            </div>

            <!-- Pipeline 4 -->
            <div class="card" style="border-left: 4px solid #06b6d4; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <h3 style="font-size: 1.1rem; margin: 0;">Stealth Passive OSINT</h3>
                        <span class="badge" style="background: rgba(6, 182, 212, 0.2); color: #22d3ee;">100% Passive</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.88rem; margin-bottom: 1rem; line-height: 1.45;">
                        Zero target packets. Collects Subfinder records, crt.sh Cert Transparency, WHOIS, and IP Geolocation / ASN.
                    </p>
                    <div style="font-size: 0.78rem; background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1.25rem; font-family: monospace; color: #22d3ee;">
                        subfinder ➔ crt.sh ➔ ip-api ➔ rdap
                    </div>
                </div>
                <button class="btn btn-secondary btn-launch-pipe" data-preset="passive_osint" data-name="Passive OSINT Recon" data-primary-tool="osint">Launch OSINT</button>
            </div>
        </div>
    `;

    await loadTargetDropdown();
    setupPipelineHandlers();

    document.getElementById('btn-close-pipeline-status').addEventListener('click', () => {
        document.getElementById('pipeline-status-card').style.display = 'none';
    });
}

async function loadTargetDropdown() {
    const sel = document.getElementById('pipeline-target-select');
    try {
        const data = await api.getTargets();
        const targets = data.targets || [];
        if (targets.length === 0) {
            sel.innerHTML = '<option value="">No targets registered yet</option>';
            return;
        }
        sel.innerHTML = targets.map(t =>
            `<option value="${t.id}" data-val="${escapeHtml(t.value)}">${escapeHtml(t.name)} (${escapeHtml(t.value)})</option>`
        ).join('');
    } catch {
        sel.innerHTML = '<option value="">Failed to load targets</option>';
    }
}

function setupPipelineHandlers() {
    document.querySelectorAll('.btn-launch-pipe').forEach(btn => {
        btn.addEventListener('click', async () => {
            const presetId = btn.getAttribute('data-preset');
            const pipeName = btn.getAttribute('data-name');
            const primaryTool = btn.getAttribute('data-primary-tool') || 'nmap';
            const targetSel = document.getElementById('pipeline-target-select');
            const targetId = targetSel.value;

            if (!targetId) {
                alert('Please select or register an authorized target first.');
                return;
            }

            const targetVal = targetSel.options[targetSel.selectedIndex]?.getAttribute('data-val') || '';

            btn.disabled = true;
            btn.textContent = 'Launching...';

            try {
                const res = await api.executePipeline(presetId, { target_id: targetId });

                // Show status card
                const statusCard = document.getElementById('pipeline-status-card');
                const titleEl = document.getElementById('active-pipe-title');
                const detailsEl = document.getElementById('active-pipe-details');
                const stagesList = document.getElementById('pipe-stages-list');

                titleEl.textContent = `${pipeName} — Active Execution`;
                detailsEl.innerHTML = `Target: <strong>${escapeHtml(targetVal)}</strong> | Total Workflow Stages: <strong>${res.total_stages}</strong>`;

                // Render sequential stage tracker
                stagesList.innerHTML = `
                    <div style="padding: 0.65rem 0.85rem; border-radius: 6px; background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); display: flex; justify-content: space-between; align-items: center;">
                        <span>Stage 1: Initial Discovery Probe (${res.current_stage})</span>
                        <span class="badge badge-emerald">Dispatched ✓</span>
                    </div>
                    <div style="padding: 0.65rem 0.85rem; border-radius: 6px; background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); display: flex; justify-content: space-between; align-items: center;">
                        <span>Stage 2: Port &amp; Service Fingerprinting (nmap / socket engine)</span>
                        <span class="badge badge-indigo">Queued ⚡</span>
                    </div>
                    <div style="padding: 0.65rem 0.85rem; border-radius: 6px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); display: flex; justify-content: space-between; align-items: center;">
                        <span>Stage 3: Vulnerability &amp; Risk Correlation (MITRE ATT&amp;CK / CVE)</span>
                        <span class="badge" style="background: rgba(255,255,255,0.1); color: var(--color-text-muted);">Pending</span>
                    </div>
                `;

                statusCard.style.display = 'block';

                // Save preselection for Live Job Center
                sessionStorage.setItem('scanet_preselected_target', targetVal);
                sessionStorage.setItem('scanet_preselected_tool', primaryTool);

            } catch (err) {
                alert(`Pipeline launch failed: ${err.message}`);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Launch Pipeline';
            }
        });
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[m]);
}
