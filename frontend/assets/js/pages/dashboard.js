/** scanet — Dashboard Page */
import { api } from '../api.js';

export async function renderDashboard(container) {
    container.innerHTML = `
        <h1 style="font-size:1.5rem;font-weight:700;margin-bottom:1.5rem">Dashboard</h1>
        <div class="stats-grid" id="stats-grid">
            <div class="card"><div class="stat-value" id="stat-tools">—</div><div class="stat-label">Tools Installed</div></div>
            <div class="card"><div class="stat-value" id="stat-jobs">—</div><div class="stat-label">Total Scan Jobs</div></div>
            <div class="card"><div class="stat-value" id="stat-targets">—</div><div class="stat-label">Authorized Targets</div></div>
            <div class="card"><div class="stat-value" id="stat-findings">—</div><div class="stat-label">Total Findings</div></div>
        </div>
        <div class="mt-lg grid-2">
            <div class="card">
                <div class="card-title">System Resources</div>
                <div id="resource-info" class="text-sm text-muted">Loading...</div>
            </div>
            <div class="card">
                <div class="card-title">Tool Health Status</div>
                <div id="tool-health" class="text-sm">Loading...</div>
            </div>
        </div>
    `;

    // Load data
    try {
        const [tools, resources, targets, jobs] = await Promise.all([
            api.getTools(), api.getResources(), api.getTargets(), api.getJobs()
        ]);

        document.getElementById('stat-tools').textContent    = `${tools.installed_count}/${tools.total_count}`;
        document.getElementById('stat-jobs').textContent     = jobs.total || 0;
        document.getElementById('stat-targets').textContent  = targets.total || 0;
        document.getElementById('stat-findings').textContent = '—';

        document.getElementById('resource-info').innerHTML = `
            <div>CPU: <strong>${resources.cpu_percent}%</strong></div>
            <div>RAM: <strong>${resources.ram.used_mb} MB</strong> / ${resources.ram.total_mb} MB (${resources.ram.percent}%)</div>
            <div>Disk: <strong>${resources.disk.free_gb} GB</strong> free</div>
            <div>OS: ${resources.platform.os} ${resources.platform.release} (${resources.platform.arch})</div>
        `;

        const installed = tools.tools.filter(t => t.installed);
        const missing   = tools.tools.filter(t => !t.installed);
        document.getElementById('tool-health').innerHTML = `
            <div>${installed.map(t => `<span class="badge badge-success" style="margin:2px">${t.tool_name}</span>`).join('')}</div>
            <div class="mt-md">${missing.map(t => `<span class="badge badge-muted" style="margin:2px">${t.tool_name}</span>`).join('')}</div>
        `;
    } catch (err) {
        document.getElementById('resource-info').textContent = `Error: ${err.message}`;
    }
}
