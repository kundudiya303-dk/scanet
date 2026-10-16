/**
 * scanet — Interactive Attack Surface Topology Graph
 * Dynamically rendered from real database scan results:
 * Target -> Host IPs -> Open Ports -> Findings.
 */
import { api } from '../api.js';

export async function renderTopology(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Attack Surface Topology Graph</h2>
                <p style="color: var(--color-text-muted);">Visual force-directed map of targets, live hosts, open ports, and correlated vulnerabilities.</p>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <select id="topo-target-select" class="input" style="width: auto; padding: 0.4rem 0.8rem; font-size: 0.85rem;">
                    <option value="">All Targets</option>
                </select>
                <button class="btn btn-secondary" id="btn-refresh-topo" style="font-size: 0.82rem; padding: 0.4rem 0.8rem;">↻ Refresh</button>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 1fr; gap: 1.5rem;">
            <!-- Interactive Canvas Area -->
            <div class="card" style="min-height: 540px; display: flex; flex-direction: column; position: relative; overflow: hidden; background: radial-gradient(circle at 50% 50%, #151d30 0%, #080d1a 100%); border: 1px solid rgba(99, 102, 241, 0.25);">
                <!-- Visual Map Legend -->
                <div style="position: absolute; top: 1rem; left: 1rem; display: flex; gap: 0.5rem; z-index: 10; flex-wrap: wrap;">
                    <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">● Target Scope</span>
                    <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">● Live Host</span>
                    <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">● Port / Service</span>
                    <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171;">● Risk / Finding</span>
                </div>

                <!-- Live Node Count Counter Badge -->
                <div style="position: absolute; top: 1rem; right: 1rem; z-index: 10;">
                    <span id="topo-node-counter" class="badge badge-cyan">0 NODES DISCOVERED</span>
                </div>

                <div id="topo-canvas-wrap" style="flex: 1; display: flex; align-items: center; justify-content: center; position: relative; margin-top: 2.5rem; min-height: 460px;">
                    <div style="color: var(--color-text-muted); font-size: 0.9rem;">Loading live topology graph...</div>
                </div>
            </div>

            <!-- Graph Inspector Panel -->
            <div class="card" style="border-left: 4px solid var(--color-cyan);">
                <div class="card-title">Node Inspector</div>
                <div id="topo-inspector-content" style="margin-top: 1rem; font-size: 0.9rem;">
                    <p style="color: var(--color-text-muted); font-size: 0.85rem;">Click any node on the graph to inspect discovered asset details and risk attributes.</p>
                </div>
            </div>
        </div>
    `;

    await loadTargetDropdown();
    await loadTopologyGraph();

    document.getElementById('btn-refresh-topo').addEventListener('click', () => loadTopologyGraph());
    document.getElementById('topo-target-select').addEventListener('change', () => loadTopologyGraph());
}

async function loadTargetDropdown() {
    const sel = document.getElementById('topo-target-select');
    try {
        const data = await api.getTargets();
        const targets = data.targets || [];
        sel.innerHTML = '<option value="">All Targets</option>' + targets.map(t =>
            `<option value="${t.id}">${escapeHtml(t.name)} (${escapeHtml(t.value)})</option>`
        ).join('');
    } catch (e) {
        // targets fallback
    }
}

async function loadTopologyGraph() {
    const targetId = document.getElementById('topo-target-select').value;
    const canvas = document.getElementById('topo-canvas-wrap');
    const counter = document.getElementById('topo-node-counter');

    try {
        const graphData = await api.getTopology(targetId);
        const nodes = graphData.elements?.nodes || [];
        const edges = graphData.elements?.edges || [];

        counter.textContent = `${nodes.length} NODES / ${edges.length} EDGES`;

        if (nodes.length === 0) {
            canvas.innerHTML = `
                <div style="text-align: center; max-width: 420px; padding: 2rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; color: var(--color-cyan);">🌐</div>
                    <h3 style="font-size: 1.15rem; margin-bottom: 0.5rem;">No Attack Surface Discovered Yet</h3>
                    <p style="color: var(--color-text-muted); font-size: 0.85rem; line-height: 1.5; margin-bottom: 1.25rem;">
                        Scanet builds attack surface topology dynamically from completed scan results. Launch a scan or load a lab preset to generate live nodes.
                    </p>
                    <a href="#/jobs" class="btn btn-primary" style="font-size: 0.85rem;">Launch First Scan</a>
                </div>
            `;
            return;
        }

        renderDynamicSvgGraph(nodes, edges, canvas);
    } catch (err) {
        canvas.innerHTML = `<div style="color: #f87171; padding: 1.5rem;">Failed to load graph: ${escapeHtml(err.message)}</div>`;
    }
}

function renderDynamicSvgGraph(nodes, edges, container) {
    const width = 760;
    const height = 460;
    const centerX = width / 2;
    const centerY = height / 2;

    // Categorize nodes
    const targets = nodes.filter(n => n.data.type === 'target');
    const hosts = nodes.filter(n => n.data.type === 'host');
    const ports = nodes.filter(n => n.data.type.startsWith('port'));
    const findings = nodes.filter(n => n.data.type === 'finding');

    const positions = {};

    // 1. Position Targets (top / center-upper)
    targets.forEach((t, i) => {
        const x = targets.length === 1 ? centerX : centerX - 180 + (i * (360 / (targets.length - 1 || 1)));
        positions[t.data.id] = { x, y: 70, r: 24, node: t };
    });

    // 2. Position Hosts (middle tier)
    hosts.forEach((h, i) => {
        const step = width / (hosts.length + 1);
        const x = step * (i + 1);
        positions[h.data.id] = { x, y: 190, r: 18, node: h };
    });

    // 3. Position Ports (lower tier)
    ports.forEach((p, i) => {
        const step = width / (ports.length + 1);
        const x = step * (i + 1);
        const y = 310 + ((i % 2) * 30);
        positions[p.data.id] = { x, y, r: 14, node: p };
    });

    // 4. Position Findings (bottom tier)
    findings.forEach((f, i) => {
        const step = width / (findings.length + 1);
        const x = step * (i + 1);
        positions[f.data.id] = { x, y: 410, r: 16, node: f };
    });

    // Generate SVG Lines
    let edgesSvg = '';
    edges.forEach(e => {
        const src = positions[e.data.source];
        const tgt = positions[e.data.target];
        if (src && tgt) {
            const isCritical = tgt.node.data.type === 'port_critical' || tgt.node.data.type === 'finding';
            const stroke = isCritical ? 'rgba(239,68,68,0.7)' : 'rgba(99,102,241,0.35)';
            const dash = isCritical ? 'stroke-dasharray="4"' : '';
            edgesSvg += `<line x1="${src.x}" y1="${src.y}" x2="${tgt.x}" y2="${tgt.y}" stroke="${stroke}" stroke-width="2" ${dash} />`;
        }
    });

    // Generate SVG Circles / Rectangles
    let nodesSvg = '';
    Object.keys(positions).forEach(id => {
        const pos = positions[id];
        const d = pos.node.data;
        const color = d.color || '#6366f1';
        const label = escapeHtml(d.label || id);

        if (d.type === 'finding') {
            nodesSvg += `
                <g class="graph-node-group" style="cursor: pointer;" data-node-id="${id}">
                    <rect x="${pos.x - 45}" y="${pos.y - 14}" width="90" height="28" rx="6" fill="${color}" stroke="#fff" stroke-width="1.5" opacity="0.9" />
                    <text x="${pos.x}" y="${pos.y + 4}" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">${escapeHtml(d.severity ? d.severity.toUpperCase() : 'ALERT')}</text>
                    <text x="${pos.x}" y="${pos.y + 26}" text-anchor="middle" fill="#f87171" font-size="8">${label.slice(0, 16)}</text>
                </g>
            `;
        } else {
            nodesSvg += `
                <g class="graph-node-group" style="cursor: pointer;" data-node-id="${id}">
                    <circle cx="${pos.x}" cy="${pos.y}" r="${pos.r}" fill="${color}" stroke="#fff" stroke-width="1.5" />
                    <text x="${pos.x}" y="${pos.y + 4}" text-anchor="middle" fill="#ffffff" font-size="${pos.r > 16 ? '10' : '8'}" font-weight="bold">${d.type === 'target' ? 'TARGET' : (d.type === 'host' ? 'HOST' : (d.port || 'PORT'))}</text>
                    <text x="${pos.x}" y="${pos.y + pos.r + 14}" text-anchor="middle" fill="#94a3b8" font-size="9">${label.slice(0, 18)}</text>
                </g>
            `;
        }
    });

    container.innerHTML = `
        <svg width="100%" height="460" viewBox="0 0 ${width} ${height}" style="overflow: visible;">
            ${edgesSvg}
            ${nodesSvg}
        </svg>
    `;

    // Click inspection handlers
    container.querySelectorAll('.graph-node-group').forEach(el => {
        el.addEventListener('click', () => {
            const nodeId = el.getAttribute('data-node-id');
            const pos = positions[nodeId];
            if (pos) {
                inspectNode(pos.node.data);
            }
        });
    });

    // Default select first node
    const firstNode = Object.values(positions)[0]?.node?.data;
    if (firstNode) inspectNode(firstNode);
}

function inspectNode(data) {
    const inspector = document.getElementById('topo-inspector-content');
    if (!inspector) return;

    if (data.type === 'target') {
        inspector.innerHTML = `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Entity Type:</span>
                <div style="font-weight: 700; color: #818cf8;">Target Scope Asset</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Target Name:</span>
                <div style="font-weight: 600;">${escapeHtml(data.label)}</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Scope Value:</span>
                <div><code>${escapeHtml(data.value || data.label)}</code></div>
            </div>
            <div style="margin-top: 1rem;">
                <span class="badge badge-indigo">Authorized Scan Scope</span>
            </div>
        `;
    } else if (data.type === 'host') {
        inspector.innerHTML = `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Entity Type:</span>
                <div style="font-weight: 700; color: #34d399;">Active Host Node</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">IPv4 Address:</span>
                <div style="font-weight: 600; font-family: monospace;">${escapeHtml(data.ip || data.label)}</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">OS Detection:</span>
                <div>${escapeHtml(data.os || 'Linux / Unprivileged Probed')}</div>
            </div>
            <div style="margin-top: 1rem;">
                <span class="badge badge-emerald">Host State: UP</span>
            </div>
        `;
    } else if (data.type.startsWith('port')) {
        inspector.innerHTML = `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Entity Type:</span>
                <div style="font-weight: 700; color: ${data.color || 'var(--color-cyan)'};">Open Service Listener</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Port & Protocol:</span>
                <div style="font-weight: 700; font-size: 1.1rem; color: #38bdf8;">TCP ${escapeHtml(String(data.port))}</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Service Name:</span>
                <div style="font-weight: 600;">${escapeHtml(data.service || 'unknown')}</div>
            </div>
            ${data.product ? `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Software Banner:</span>
                <div><code>${escapeHtml(data.product)} ${escapeHtml(data.version || '')}</code></div>
            </div>` : ''}
            <div style="margin-top: 1rem;">
                <span class="badge ${data.color === '#ef4444' ? 'badge-rose' : 'badge-cyan'}">${data.color === '#ef4444' ? 'High Risk Exposure' : 'Open Port'}</span>
            </div>
        `;
    } else if (data.type === 'finding') {
        inspector.innerHTML = `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Entity Type:</span>
                <div style="font-weight: 700; color: #f87171;">Security Finding / Advisory</div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Severity:</span>
                <div><span class="badge badge-rose">${escapeHtml(data.severity?.toUpperCase() || 'HIGH')}</span></div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Finding Title:</span>
                <div style="font-weight: 600;">${escapeHtml(data.label)}</div>
            </div>
            ${data.description ? `
            <div style="margin-bottom: 0.75rem;">
                <span style="color: var(--color-text-muted); font-size: 0.8rem;">Description:</span>
                <div style="font-size: 0.82rem; line-height: 1.4; color: #cbd5e1;">${escapeHtml(data.description)}</div>
            </div>` : ''}
            ${data.remediation ? `
            <div style="margin-top: 0.75rem; background: rgba(52,211,153,0.08); padding: 0.6rem; border-radius: 6px; border: 1px solid rgba(52,211,153,0.25);">
                <span style="color: #34d399; font-weight: 600; font-size: 0.78rem;">Remediation:</span>
                <div style="font-size: 0.8rem; margin-top: 0.2rem;">${escapeHtml(data.remediation)}</div>
            </div>` : ''}
        `;
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[m]);
}
