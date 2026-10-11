/**
 * scanet — Interactive Attack Surface Topology Graph
 */
export async function renderTopology(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Attack Surface Topology Graph</h2>
                <p style="color: var(--color-text-muted);">Visual force-directed map of targets, subdomains, live hosts, open ports, and vulnerabilities.</p>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-secondary" onclick="alert('Resetting zoom and center position.')">Reset View</button>
                <button class="btn btn-secondary" onclick="alert('Exporting high-resolution topology snapshot.')">Export PNG</button>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 3fr 1fr; gap: 1.5rem;">
            <!-- Interactive Canvas Area -->
            <div class="card" style="min-height: 520px; display: flex; flex-direction: column; position: relative; overflow: hidden; background: radial-gradient(circle at 50% 50%, #1a2234 0%, #0d121f 100%);">
                <!-- Visual Map Nodes Simulation -->
                <div style="position: absolute; top: 1rem; left: 1rem; display: flex; gap: 0.5rem;">
                    <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">● Target</span>
                    <span class="badge" style="background: rgba(6, 182, 212, 0.2); color: #22d3ee;">● Subdomain</span>
                    <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">● Host IP</span>
                    <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">● Port/Service</span>
                    <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171;">● Vulnerability</span>
                </div>

                <div style="flex: 1; display: flex; align-items: center; justify-content: center; position: relative; margin-top: 2rem;">
                    <!-- SVG Graph Visualization -->
                    <svg width="100%" height="440" viewBox="0 0 700 400" style="overflow: visible;">
                        <!-- Edges -->
                        <line x1="350" y1="60" x2="200" y2="150" stroke="#334155" stroke-width="2" />
                        <line x1="350" y1="60" x2="500" y2="150" stroke="#334155" stroke-width="2" />
                        <line x1="200" y1="150" x2="150" y2="250" stroke="#334155" stroke-width="2" />
                        <line x1="200" y1="150" x2="270" y2="250" stroke="#334155" stroke-width="2" />
                        <line x1="500" y1="150" x2="430" y2="250" stroke="#334155" stroke-width="2" />
                        <line x1="500" y1="150" x2="570" y2="250" stroke="#ef4444" stroke-width="2" stroke-dasharray="4" />
                        <line x1="570" y1="250" x2="570" y2="340" stroke="#ef4444" stroke-width="2" />

                        <!-- Nodes -->
                        <!-- Root Target -->
                        <circle cx="350" cy="60" r="24" fill="#6366f1" />
                        <text x="350" y="65" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">TARGET</text>
                        <text x="350" y="98" text-anchor="middle" fill="#94a3b8" font-size="11">target.lab</text>

                        <!-- Subdomain 1 -->
                        <circle cx="200" cy="150" r="18" fill="#06b6d4" />
                        <text x="200" y="154" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">SUB</text>
                        <text x="200" y="180" text-anchor="middle" fill="#94a3b8" font-size="10">api.target.lab</text>

                        <!-- Subdomain 2 -->
                        <circle cx="500" cy="150" r="18" fill="#06b6d4" />
                        <text x="500" y="154" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="bold">SUB</text>
                        <text x="500" y="180" text-anchor="middle" fill="#94a3b8" font-size="10">auth.target.lab</text>

                        <!-- Port Nodes -->
                        <circle cx="150" cy="250" r="14" fill="#3b82f6" />
                        <text x="150" y="254" text-anchor="middle" fill="#ffffff" font-size="8">80</text>
                        <text x="150" y="275" text-anchor="middle" fill="#94a3b8" font-size="9">HTTP</text>

                        <circle cx="270" cy="250" r="14" fill="#3b82f6" />
                        <text x="270" y="254" text-anchor="middle" fill="#ffffff" font-size="8">443</text>
                        <text x="270" y="275" text-anchor="middle" fill="#94a3b8" font-size="9">HTTPS</text>

                        <circle cx="430" cy="250" r="14" fill="#3b82f6" />
                        <text x="430" y="254" text-anchor="middle" fill="#ffffff" font-size="8">22</text>
                        <text x="430" y="275" text-anchor="middle" fill="#94a3b8" font-size="9">SSH</text>

                        <!-- Exposed Critical Port -->
                        <circle cx="570" cy="250" r="16" fill="#ef4444" />
                        <text x="570" y="254" text-anchor="middle" fill="#ffffff" font-size="8" font-weight="bold">6379</text>
                        <text x="570" y="275" text-anchor="middle" fill="#f87171" font-size="9">REDIS</text>

                        <!-- Critical Finding -->
                        <rect x="510" y="325" width="120" height="30" rx="6" fill="#dc2626" />
                        <text x="570" y="344" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="bold">Unauth Access</text>
                    </svg>
                </div>
            </div>

            <!-- Graph Inspector Panel -->
            <div class="card">
                <h3>Node Inspector</h3>
                <div style="margin-top: 1rem; font-size: 0.9rem;">
                    <div style="margin-bottom: 0.75rem;">
                        <span style="color: var(--color-text-muted);">Selected Entity:</span>
                        <div style="font-weight: 600; color: #f87171; margin-top: 0.2rem;">Port 6379/tcp (Redis)</div>
                    </div>
                    <div style="margin-bottom: 0.75rem;">
                        <span style="color: var(--color-text-muted);">Host:</span>
                        <div>192.168.1.100 (auth.target.lab)</div>
                    </div>
                    <div style="margin-bottom: 0.75rem;">
                        <span style="color: var(--color-text-muted);">Risk Rating:</span>
                        <div><span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #ef4444;">CRITICAL (CVSS 9.8)</span></div>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <span style="color: var(--color-text-muted);">Advisory:</span>
                        <div style="font-size: 0.85rem; line-height: 1.4; margin-top: 0.3rem;">
                            Redis server accepts unauthenticated remote command execution. Immediate firewall isolation required.
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="width: 100%; font-size: 0.85rem;" onclick="alert('Viewing correlated CVEs and remediation...')">View Remediation Playbook</button>
                </div>
            </div>
        </div>
    `;
}
