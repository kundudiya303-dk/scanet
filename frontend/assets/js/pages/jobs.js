/**
 * scanet — Scan Launcher & Live Job Execution Center
 * Real API-backed implementation:
 *  - Loads targets from DB for target selector
 *  - Dispatches real scan jobs via POST /api/v1/jobs
 *  - Streams live SSE output from the running process
 *  - Lists real job history from DB
 */
import { api } from '../api.js';

export async function renderJobs(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem;">
            <h2>Scan Launcher &amp; Live Process Center</h2>
            <p style="color: var(--color-text-muted);">Configure tool parameters, preview the CLI vector, and stream real-time scan output.</p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
            <!-- Scan Configuration Panel -->
            <div class="card" style="border-left: 4px solid var(--color-cyan);">
                <div class="card-title">1. Configure Scan Job</div>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div>
                        <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Select Authorized Target</label>
                        <select class="input" id="job-target-select">
                            <option value="">Loading targets...</option>
                        </select>
                    </div>

                    <div>
                        <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Select Security Tool</label>
                        <select class="input" id="job-tool-select">
                            <option value="nmap">Nmap — Deep Service &amp; Version Scan</option>
                            <option value="naabu">Naabu — High-Speed Port Discovery</option>
                            <option value="rustscan">RustScan — Adaptive Fast Sweep</option>
                            <option value="ffuf">FFUF — Fast Directory Fuzzing</option>
                            <option value="gobuster">Gobuster — Directory Fuzzer</option>
                            <option value="katana">Katana — Web Crawler &amp; API Routes</option>
                            <option value="nuclei">Nuclei — Vulnerability &amp; Misconfig Templates</option>
                            <option value="subfinder">Subfinder — Passive Subdomain Recon</option>
                            <option value="dnsx">dnsx — Multi-Record DNS Resolver</option>
                            <option value="httpx">HTTPX — HTTP Tech &amp; TLS Surface</option>
                            <option value="mtr">MTR — Hop-by-Hop Route Diagnostics</option>
                            <option value="osint">OSINT Engine — Passive Geo/ASN/crt.sh</option>
                        </select>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Timing / Speed</label>
                            <select class="input" id="job-speed-select">
                                <option value="3">Normal (T3 - Safe)</option>
                                <option value="2">Polite (T2 - Low Bandwidth)</option>
                                <option value="4">Aggressive (T4 - High Speed)</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Port Range</label>
                            <select class="input" id="job-ports-select">
                                <option value="top-100">Top 100 Common Ports</option>
                                <option value="top-1000">Top 1,000 Standard Ports</option>
                                <option value="top-65535">All 65,535 Ports (-p-)</option>
                            </select>
                        </div>
                    </div>

                    <div id="job-launch-error" style="display:none; color:#f87171; font-size:0.82rem; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); padding:0.5rem 0.75rem; border-radius:6px;"></div>

                    <div style="display: flex; gap: 0.75rem; margin-top: 0.25rem;">
                        <button class="btn btn-primary" style="flex: 1;" id="btn-launch-scan">▶ Launch Real Scan</button>
                        <button class="btn btn-secondary" id="btn-clear-term">Clear Console</button>
                    </div>
                </div>
            </div>

            <!-- Live CLI Preview -->
            <div class="card" style="border-left: 4px solid var(--color-primary);">
                <div class="card-title">
                    <span>2. Live CLI Vector Preview</span>
                    <span class="badge badge-indigo">Zero shell injection</span>
                </div>
                <div style="font-size: 0.82rem; color: var(--color-text-muted); margin-bottom: 0.75rem;">
                    Command dispatched via process-group isolation (no shell=True):
                </div>
                <div id="cmd-preview-box" style="background: #050811; border: 1px solid rgba(99, 102, 241, 0.3); padding: 0.85rem 1rem; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 0.88rem; color: #38bdf8; margin-bottom: 1rem; word-break: break-all;">
                    nmap -sT -sV -T3 --top-ports 100 -oX - &lt;target&gt;
                </div>
                <div id="active-job-info" style="display:none; background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.25); padding:0.75rem; border-radius:6px; font-size:0.83rem;">
                    <strong style="color:#34d399;">Active Job:</strong>
                    <span id="active-job-id" style="font-family:var(--font-mono); color:#94a3b8;"></span>
                </div>
            </div>
        </div>

        <!-- Live Terminal Stream -->
        <div class="card" style="margin-bottom: 2rem;">
            <div class="card-title">
                <span>Real-Time Output Stream (SSE)</span>
                <span class="badge badge-cyan" id="stream-badge"><span class="badge-pulse"></span> IDLE</span>
            </div>
            <div class="terminal" id="terminal-screen" style="min-height:220px;">[scanet-engine] Ready. Configure a target and tool above, then click Launch Real Scan.
[scanet-engine] Process isolation: os.setsid process-group termination active.
[scanet-engine] Scope guardrail: Hard-blocked IMDS and loopback ranges enforced.</div>
        </div>

        <!-- Job History Table -->
        <div class="card">
            <div class="card-title">
                <span id="jobs-history-label">Scan Job History</span>
                <button class="btn btn-secondary" id="btn-refresh-jobs" style="font-size:0.8rem; padding:0.3rem 0.75rem;">↻ Refresh</button>
            </div>
            <div id="jobs-table-wrap" class="table-container">
                <div style="text-align:center; padding:1.5rem; color:var(--color-text-muted);">Loading job history...</div>
            </div>
        </div>
    `;

    await loadTargetDropdown();
    await loadJobHistory();
    setupCommandPreview();

    document.getElementById('btn-launch-scan').addEventListener('click', launchScan);
    document.getElementById('btn-clear-term').addEventListener('click', () => {
        document.getElementById('terminal-screen').textContent = '[scanet-engine] Terminal cleared.';
    });
    document.getElementById('btn-refresh-jobs').addEventListener('click', loadJobHistory);
    document.getElementById('job-tool-select').addEventListener('change', updateCmdPreview);
    document.getElementById('job-target-select').addEventListener('change', updateCmdPreview);
    document.getElementById('job-speed-select').addEventListener('change', updateCmdPreview);
    document.getElementById('job-ports-select').addEventListener('change', updateCmdPreview);
}


async function loadTargetDropdown() {
    const sel = document.getElementById('job-target-select');
    try {
        const data = await api.getTargets();
        const targets = data.targets || [];
        if (targets.length === 0) {
            sel.innerHTML = '<option value="">No authorized targets registered. Add one in the Targets page.</option>';
            return;
        }
        sel.innerHTML = targets.map(t =>
            `<option value="${escapeHtml(t.id)}" data-value="${escapeHtml(t.value)}">${escapeHtml(t.name)} (${escapeHtml(t.value)})</option>`
        ).join('');

        // Handle preselected target from lab presets or navigation
        const preselectedVal = sessionStorage.getItem('scanet_preselected_target');
        const preselectedTool = sessionStorage.getItem('scanet_preselected_tool');

        if (preselectedVal) {
            for (let i = 0; i < sel.options.length; i++) {
                if (sel.options[i].getAttribute('data-value') === preselectedVal || sel.options[i].value === preselectedVal) {
                    sel.selectedIndex = i;
                    break;
                }
            }
            sessionStorage.removeItem('scanet_preselected_target');
            const errEl = document.getElementById('job-launch-error');
            if (errEl) {
                errEl.style.display = 'block';
                errEl.style.color = '#34d399';
                errEl.style.background = 'rgba(52,211,153,0.1)';
                errEl.style.border = '1px solid rgba(52,211,153,0.3)';
                errEl.textContent = `✓ Lab preset target loaded: "${preselectedVal}". Ready to launch!`;
            }
        }

        if (preselectedTool) {
            const toolSel = document.getElementById('job-tool-select');
            if (toolSel) toolSel.value = preselectedTool;
            sessionStorage.removeItem('scanet_preselected_tool');
        }

        updateCmdPreview();
    } catch {
        sel.innerHTML = '<option value="">Failed to load targets. Is the backend running?</option>';
    }
}


async function loadJobHistory() {
    const wrap  = document.getElementById('jobs-table-wrap');
    const label = document.getElementById('jobs-history-label');
    try {
        const data = await api.getJobs();
        const jobs = data.jobs || [];
        label.textContent = `Scan Job History (${jobs.length} jobs)`;

        if (jobs.length === 0) {
            wrap.innerHTML = '<div style="text-align:center; padding:1.5rem; color:var(--color-text-muted);">No jobs run yet. Launch your first scan above.</div>';
            return;
        }

        const rows = jobs.map(j => `
            <tr>
                <td><code style="font-size:0.78rem;">${escapeHtml(j.id.slice(0, 8))}...</code></td>
                <td><strong>${escapeHtml(j.target_name || j.target_value || '—')}</strong><br><span style="font-size:0.78rem; color:var(--color-text-muted);">${escapeHtml(j.target_value || '')}</span></td>
                <td><span class="badge badge-indigo">${escapeHtml(j.tool_name)}</span></td>
                <td>${statusBadge(j.status)}</td>
                <td>${j.started_at ? new Date(j.started_at).toLocaleString() : '—'}</td>
                <td>${j.completed_at ? new Date(j.completed_at).toLocaleString() : '—'}</td>
                <td>
                    ${j.status === 'running'
                        ? `<button class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.5rem;" data-cancel-id="${escapeHtml(j.id)}">■ Cancel</button>`
                        : `<button class="btn btn-secondary" style="font-size:0.75rem; padding:0.25rem 0.5rem;" data-stream-id="${escapeHtml(j.id)}">View Output</button>`
                    }
                </td>
            </tr>
        `).join('');

        wrap.innerHTML = `
            <table>
                <thead>
                    <tr><th>Job ID</th><th>Target</th><th>Tool</th><th>Status</th><th>Started</th><th>Completed</th><th>Actions</th></tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        `;

        // Cancel handlers
        wrap.querySelectorAll('[data-cancel-id]').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-cancel-id');
                await api.cancelJob(id);
                await loadJobHistory();
            });
        });

        // View output handlers (re-attach SSE stream)
        wrap.querySelectorAll('[data-stream-id]').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-stream-id');
                streamJobOutput(id);
            });
        });

    } catch (err) {
        wrap.innerHTML = `<div style="color:#f87171; padding:1rem;">Failed to load jobs: ${escapeHtml(err.message)}</div>`;
    }
}


async function launchScan() {
    const targetId = document.getElementById('job-target-select').value;
    const toolName = document.getElementById('job-tool-select').value;
    const speed    = document.getElementById('job-speed-select').value;
    const ports    = document.getElementById('job-ports-select').value;
    const errEl    = document.getElementById('job-launch-error');
    const btn      = document.getElementById('btn-launch-scan');
    const term     = document.getElementById('terminal-screen');

    errEl.style.display = 'none';

    if (!targetId) {
        errEl.textContent = 'Please select an authorized target from the dropdown.';
        errEl.style.display = 'block';
        return;
    }

    btn.disabled    = true;
    btn.textContent = 'Dispatching...';
    term.textContent = `[scanet-engine] Dispatching job: tool=${toolName}, speed=T${speed}, ports=${ports}...\n`;
    document.getElementById('stream-badge').innerHTML = '<span class="badge-pulse"></span> LAUNCHING';

    try {
        const res = await api.createJob({
            target_id:    targetId,
            tool_name:    toolName,
            profile_name: `speed-T${speed}`,
            parameters:   { speed, ports },
        });

        term.textContent += `[scanet-engine] Job ID: ${res.job_id}\n`;
        term.textContent += `[scanet-engine] Command: ${res.command}\n`;
        term.textContent += `[scanet-engine] Status: ${res.status}\n`;
        term.textContent += `[scanet-engine] Streaming output via SSE...\n\n`;

        document.getElementById('active-job-info').style.display = 'block';
        document.getElementById('active-job-id').textContent = res.job_id;
        document.getElementById('stream-badge').innerHTML = '<span class="badge-pulse"></span> STREAMING';

        streamJobOutput(res.job_id);
        await loadJobHistory();

    } catch (err) {
        errEl.textContent = `Launch failed: ${err.message}`;
        errEl.style.display = 'block';
        term.textContent += `[scanet-engine] ERROR: ${err.message}\n`;
        document.getElementById('stream-badge').innerHTML = '<span class="badge-pulse"></span> ERROR';
    } finally {
        btn.disabled    = false;
        btn.textContent = '▶ Launch Real Scan';
    }
}


function streamJobOutput(jobId) {
    const term   = document.getElementById('terminal-screen');
    const badge  = document.getElementById('stream-badge');
    badge.innerHTML = '<span class="badge-pulse"></span> STREAMING';

    const es = api.streamJob(jobId, (line) => {
        term.textContent += line + '\n';
        term.scrollTop = term.scrollHeight;
    });

    es.onerror = () => {
        es.close();
        badge.innerHTML = 'DONE';
        loadJobHistory();
    };
}


function setupCommandPreview() {
    updateCmdPreview();
}


function updateCmdPreview() {
    const tool   = document.getElementById('job-tool-select')?.value || 'nmap';
    const speed  = document.getElementById('job-speed-select')?.value || '3';
    const ports  = document.getElementById('job-ports-select')?.value || 'top-100';
    const sel    = document.getElementById('job-target-select');
    const target = sel?.options[sel.selectedIndex]?.getAttribute('data-value') || '<target>';
    const box    = document.getElementById('cmd-preview-box');
    if (!box) return;

    const portArg  = ports === 'top-65535' ? '-p-' : `--top-ports ${ports === 'top-100' ? '100' : '1000'}`;
    const previews = {
        nmap:      `nmap -sT -sV -T${speed} ${portArg} -oX - ${target}`,
        naabu:     `naabu -host ${target} ${portArg.replace('--top-ports', '-top-ports')} -json -silent`,
        rustscan:  `rustscan -a ${target} --top --ulimit 5000 -- -sV`,
        ffuf:      `ffuf -u https://${target}/FUZZ -w /opt/scanet/wordlists/common.txt -rate 50 -of json`,
        gobuster:  `gobuster dir -u https://${target} -w /opt/scanet/wordlists/common.txt -q`,
        katana:    `katana -u https://${target} -jc -depth 2 -concurrency 10 -silent`,
        nuclei:    `nuclei -target ${target} -tags misconfig,exposure -severity info,low,medium,high -jsonl`,
        subfinder: `subfinder -d ${target} -silent -json`,
        dnsx:      `dnsx -d ${target} -a -cname -resp -json`,
        httpx:     `httpx -u ${target} -title -tech-detect -status-code -tls-probe -json`,
        mtr:       `mtr --report --report-cycles 5 ${target}`,
        osint:     `[OSINT Engine] Passive geolocation + ASN + crt.sh cert transparency lookup for: ${target}`,
    };

    // Set using textContent to prevent DOM XSS
    box.textContent = previews[tool] || `${tool} ${target}`;
}


function statusBadge(status) {
    const map = {
        running:   'badge-cyan',
        completed: 'badge-emerald',
        failed:    'badge-red',
        cancelled: 'badge-amber',
        queued:    'badge-indigo',
    };
    return `<span class="badge ${map[status] || 'badge-indigo'}">${escapeHtml(status)}</span>`;
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
