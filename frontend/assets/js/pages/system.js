/** scanet — System Health Page */
import { api } from '../api.js';

export async function renderSystem(container) {
    container.innerHTML = `
        <h1 style="font-size:1.5rem;font-weight:700;margin-bottom:1.5rem">System Health</h1>
        <div id="tools-grid" class="card"><div class="card-title">Tool Status</div><p class="text-muted text-sm">Loading...</p></div>
    `;
    try {
        const data = await api.getTools();
        const rows = data.tools.map(t => `
            <tr>
                <td class="text-mono">${t.tool_name}</td>
                <td><span class="badge badge-muted">${t.category}</span></td>
                <td><span class="badge badge-muted">Tier ${t.tier}</span></td>
                <td>${t.installed
                    ? `<span class="badge badge-success">Installed</span>`
                    : `<span class="badge badge-danger">Missing</span>`}
                </td>
                <td class="text-mono text-xs text-muted">${t.path || '—'}</td>
            </tr>`).join('');

        document.getElementById('tools-grid').innerHTML = `
            <div class="card-title">Tool Status (${data.installed_count}/${data.total_count} installed)</div>
            <div class="table-container">
                <table>
                    <thead><tr><th>Tool</th><th>Category</th><th>Tier</th><th>Status</th><th>Path</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>`;
    } catch (err) {
        document.getElementById('tools-grid').innerHTML = `<p class="text-sm" style="color:var(--color-danger)">Error: ${err.message}</p>`;
    }
}
