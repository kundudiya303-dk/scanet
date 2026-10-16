/**
 * scanet — Target & Scope Manager Page
 * Real API-backed implementation: loads from DB, creates via POST, deletes via DELETE.
 */
import { api } from '../api.js';

export async function renderTargets(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Target &amp; Scope Authorization Manager</h2>
                <p style="color: var(--color-text-muted);">Manage approved IP addresses, CIDR blocks, and domains for ethical lab reconnaissance.</p>
            </div>
        </div>

        <!-- Add Target Card -->
        <div class="card" style="margin-bottom: 2rem; border-left: 4px solid var(--color-primary);">
            <div class="card-title">Register New Target Scope</div>
            <div id="target-form-error" style="display:none; color:#f87171; font-size:0.85rem; margin-bottom:0.75rem; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); padding:0.5rem 0.75rem; border-radius:6px;"></div>
            <div id="target-form-success" style="display:none; color:#34d399; font-size:0.85rem; margin-bottom:0.75rem; background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.3); padding:0.5rem 0.75rem; border-radius:6px;"></div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr auto; gap: 1rem; align-items: end;">
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Friendly Name</label>
                    <input type="text" class="input" id="target-name" placeholder="e.g. Web Lab Server" />
                </div>
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Target Value (IP / CIDR / Domain)</label>
                    <input type="text" class="input" id="target-value" placeholder="e.g. 192.168.1.100" />
                </div>
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Target Type</label>
                    <select class="input" id="target-type" style="cursor: pointer;">
                        <option value="ip">IPv4 Single Host</option>
                        <option value="cidr">CIDR Subnet Block</option>
                        <option value="domain">Domain / FQDN</option>
                    </select>
                </div>
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Created By</label>
                    <input type="text" class="input" id="target-createdby" placeholder="admin" value="admin" />
                </div>
                <div>
                    <button class="btn btn-emerald" id="btn-add-target">Verify &amp; Register</button>
                </div>
            </div>
        </div>

        <!-- Targets Table -->
        <div class="card">
            <div class="card-title">
                <span id="targets-count-label">Whitelisted Targets</span>
                <span class="badge badge-emerald"><span class="badge-pulse"></span> SCOPE ENFORCED</span>
            </div>
            <div id="targets-table-wrap" class="table-container">
                <div style="text-align:center; padding: 2rem; color: var(--color-text-muted);">Loading targets...</div>
            </div>
        </div>
    `;

    await loadTargets();

    document.getElementById('btn-add-target').addEventListener('click', async () => {
        const name      = document.getElementById('target-name').value.trim();
        const value     = document.getElementById('target-value').value.trim();
        const type      = document.getElementById('target-type').value;
        const createdBy = document.getElementById('target-createdby').value.trim() || 'admin';

        clearMessages();

        if (!name || !value) {
            showError('Please fill in both the Friendly Name and Target Value fields.');
            return;
        }

        const btn = document.getElementById('btn-add-target');
        btn.disabled = true;
        btn.textContent = 'Registering...';

        try {
            const res = await api.createTarget({ name, value, target_type: type, created_by: createdBy });
            showSuccess(`Target "${res.name}" (${res.value}) registered successfully with ID: ${res.target_id}`);
            document.getElementById('target-name').value = '';
            document.getElementById('target-value').value = '';
            await loadTargets();
        } catch (err) {
            showError(err.message || 'Registration failed. Check the value and try again.');
        } finally {
            btn.disabled = false;
            btn.textContent = 'Verify & Register';
        }
    });
}

async function loadTargets() {
    const wrap = document.getElementById('targets-table-wrap');
    try {
        const data = await api.getTargets();
        const targets = data.targets || [];
        document.getElementById('targets-count-label').textContent =
            `Whitelisted Targets (${targets.length} registered)`;

        if (targets.length === 0) {
            wrap.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--color-text-muted);">
                No targets registered yet. Add your first authorized target above.
            </div>`;
            return;
        }

        const rows = targets.map(t => `
            <tr>
                <td><strong>${escapeHtml(t.name)}</strong></td>
                <td><code>${escapeHtml(t.value)}</code></td>
                <td><span class="badge ${typeBadge(t.target_type)}">${escapeHtml(t.target_type)}</span></td>
                <td><span class="badge ${t.is_approved ? 'badge-emerald' : 'badge-amber'}">${t.is_approved ? 'Approved' : 'Pending'}</span></td>
                <td>${escapeHtml(t.created_by || 'admin')}</td>
                <td>${t.created_at ? new Date(t.created_at).toLocaleString() : '—'}</td>
                <td style="display:flex; gap:0.4rem;">
                    <button class="btn btn-secondary" style="font-size:0.78rem; padding:0.3rem 0.6rem;"
                        onclick="window.location.hash='#/jobs'">
                        Scan Target
                    </button>
                    <button class="btn" style="font-size:0.78rem; padding:0.3rem 0.6rem; background:rgba(239,68,68,0.15); color:#f87171; border:1px solid rgba(239,68,68,0.3);"
                        data-delete-id="${escapeHtml(t.id)}" data-delete-name="${escapeHtml(t.name)}">
                        Remove
                    </button>
                </td>
            </tr>
        `).join('');

        wrap.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Friendly Name</th>
                        <th>Value</th>
                        <th>Type</th>
                        <th>Approval Status</th>
                        <th>Created By</th>
                        <th>Registered At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        `;

        // Attach delete handlers
        wrap.querySelectorAll('[data-delete-id]').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id   = btn.getAttribute('data-delete-id');
                const name = btn.getAttribute('data-delete-name');
                if (!confirm(`Remove target "${name}"? All associated jobs will remain in audit history.`)) return;
                try {
                    await api.deleteTarget(id);
                    await loadTargets();
                } catch (err) {
                    showError(`Delete failed: ${err.message}`);
                }
            });
        });

    } catch (err) {
        wrap.innerHTML = `<div style="color:#f87171; padding:1rem;">Failed to load targets: ${escapeHtml(err.message)}</div>`;
    }
}

function typeBadge(type) {
    if (type === 'ip')     return 'badge-indigo';
    if (type === 'cidr')   return 'badge-amber';
    if (type === 'domain') return 'badge-cyan';
    return 'badge-indigo';
}

function showError(msg) {
    const el = document.getElementById('target-form-error');
    el.textContent = msg;
    el.style.display = 'block';
}

function showSuccess(msg) {
    const el = document.getElementById('target-form-success');
    el.textContent = msg;
    el.style.display = 'block';
}

function clearMessages() {
    document.getElementById('target-form-error').style.display = 'none';
    document.getElementById('target-form-success').style.display = 'none';
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
