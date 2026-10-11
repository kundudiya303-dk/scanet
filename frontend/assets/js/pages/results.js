/**
 * scanet — Results Explorer & Multi-Format Report Center
 */
export async function renderResults(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Normalized Results & Audit Findings</h2>
                <p style="color: var(--color-text-muted);">Inspect discovered hosts, open ports, identified services, and vulnerability findings.</p>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-primary" onclick="alert('Exporting OASIS SARIF v2.1.0 JSON report for GitHub Security / CI/CD...')">📥 Export SARIF</button>
                <button class="btn btn-secondary" onclick="alert('Generating Executive PDF Report with charts and remediation...')">📥 PDF Report</button>
                <button class="btn btn-secondary" onclick="alert('Exporting normalized JSON dataset...')">📥 JSON</button>
            </div>
        </div>

        <!-- Severity Summary Bar -->
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 2rem;">
            <div class="card" style="border-left: 4px solid var(--color-rose); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">CRITICAL</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #f87171;">1</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-amber); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">HIGH</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #fbbf24;">2</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-primary); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">MEDIUM</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8;">3</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-emerald); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">LOW</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #34d399;">5</div>
            </div>
            <div class="card" style="border-left: 4px solid var(--color-cyan); padding: 1rem;">
                <div style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: 700;">INFO</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #22d3ee;">14</div>
            </div>
        </div>

        <!-- Discovered Hosts & Ports Table -->
        <div class="card" style="margin-bottom: 2rem;">
            <div class="card-title">
                <span>Discovered Hosts & Service Fingerprints</span>
                <span class="badge badge-emerald">Normalized Schema</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Host IP</th>
                            <th>Port / Protocol</th>
                            <th>Service</th>
                            <th>Product & Version</th>
                            <th>Detected OS</th>
                            <th>Severity</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge badge-rose">6379/tcp</span></td>
                            <td>redis</td>
                            <td>Redis 6.2.6 (Unauthenticated)</td>
                            <td>Linux 5.x (Ubuntu)</td>
                            <td><span class="badge badge-rose">CRITICAL</span></td>
                        </tr>
                        <tr>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge badge-indigo">22/tcp</span></td>
                            <td>ssh</td>
                            <td>OpenSSH 8.9p1 (Ubuntu)</td>
                            <td>Linux 5.x (Ubuntu)</td>
                            <td><span class="badge badge-emerald">LOW</span></td>
                        </tr>
                        <tr>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge badge-cyan">80/tcp</span></td>
                            <td>http</td>
                            <td>nginx 1.24.0 (Missing HSTS/CSP)</td>
                            <td>Linux 5.x (Ubuntu)</td>
                            <td><span class="badge badge-amber">MEDIUM</span></td>
                        </tr>
                        <tr>
                            <td><code>juiceshop.lab</code></td>
                            <td><span class="badge badge-cyan">3000/tcp</span></td>
                            <td>http-alt</td>
                            <td>Node.js Express / Angular SPA</td>
                            <td>Linux / Container</td>
                            <td><span class="badge badge-amber">MEDIUM</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Security Findings Table -->
        <div class="card">
            <div class="card-title">
                <span>Security Findings & Vulnerabilities</span>
                <span class="badge badge-indigo">CVE & Misconfigs</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Finding</th>
                            <th>Matched Location</th>
                            <th>CVE / Standard</th>
                            <th>CVSS</th>
                            <th>Severity</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Unauthenticated Redis Remote Listener</strong></td>
                            <td><code>redis://192.168.1.100:6379</code></td>
                            <td>MISCONFIG-REDIS-UNAUTH</td>
                            <td>9.8</td>
                            <td><span class="badge badge-rose">CRITICAL</span></td>
                            <td>
                                <button class="btn btn-secondary" style="font-size:0.75rem;padding:0.25rem 0.5rem;" onclick="alert('Remediation: Set requirepass in redis.conf, bind to 127.0.0.1')">View Fix</button>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>Missing HTTP Defense Headers (Grade D)</strong></td>
                            <td><code>http://192.168.1.100/</code></td>
                            <td>OWASP A05:2021</td>
                            <td>5.3</td>
                            <td><span class="badge badge-amber">MEDIUM</span></td>
                            <td>
                                <button class="btn btn-secondary" style="font-size:0.75rem;padding:0.25rem 0.5rem;" onclick="alert('Remediation: Deploy Content-Security-Policy and X-Frame-Options headers')">View Fix</button>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>regreSSHion Signal Detection</strong></td>
                            <td><code>ssh://192.168.1.100:22</code></td>
                            <td>CVE-2024-6387</td>
                            <td>8.1</td>
                            <td><span class="badge badge-amber">HIGH</span></td>
                            <td>
                                <button class="btn btn-secondary" style="font-size:0.75rem;padding:0.25rem 0.5rem;" onclick="alert('Remediation: Upgrade OpenSSH to 9.8p1 or newer')">View Fix</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
}
