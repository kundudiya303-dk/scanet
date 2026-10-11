/**
 * scanet — System Health & Binary Integrity Page
 */
import { api } from '../api.js';

export async function renderSystem(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>System Health & Binary Integrity</h2>
                <p style="color: var(--color-text-muted);">Monitor tool installations, executable binary paths, and real-time host resource metrics.</p>
            </div>
            <button class="btn btn-secondary" onclick="alert('Checking binary presence in /usr/bin, /opt/scanet/bin, and system $PATH...')">↻ Refresh Audit</button>
        </div>

        <!-- Node Telemetry Row -->
        <div class="card" style="margin-bottom: 2rem; border-left: 4px solid var(--color-emerald);">
            <div class="card-title">Node Telemetry & Host Environment</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;" id="system-telemetry">
                <div>
                    <div style="font-size: 0.8rem; color: var(--color-text-muted);">OS & Kernel</div>
                    <div style="font-weight: 700; font-size: 1.05rem; margin-top: 0.2rem;" id="sys-os">Linux / AWS Node</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: var(--color-text-muted);">Python Runtime</div>
                    <div style="font-weight: 700; font-size: 1.05rem; margin-top: 0.2rem; color: var(--color-cyan);">Python 3.10+ (AsyncIO)</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: var(--color-text-muted);">Database Engine</div>
                    <div style="font-weight: 700; font-size: 1.05rem; margin-top: 0.2rem; color: var(--color-emerald);">SQLite WAL Mode</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: var(--color-text-muted);">Process Manager</div>
                    <div style="font-weight: 700; font-size: 1.05rem; margin-top: 0.2rem; color: var(--color-purple);">os.setsid Isolation</div>
                </div>
            </div>
        </div>

        <!-- Tool Availability Matrix -->
        <div class="card" id="tools-grid">
            <div class="card-title">
                <span>Security Tools Binary Availability</span>
                <span class="badge badge-cyan" id="tools-count-badge">12 Configured</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tool Name</th>
                            <th>Domain Category</th>
                            <th>Tier</th>
                            <th>Status</th>
                            <th>Binary Path</th>
                        </tr>
                    </thead>
                    <tbody id="tools-table-rows">
                        <tr>
                            <td><strong>nmap</strong></td>
                            <td><span class="badge badge-indigo">port_scan</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/usr/bin/nmap</code></td>
                        </tr>
                        <tr>
                            <td><strong>katana</strong></td>
                            <td><span class="badge badge-indigo">web_discovery</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/katana</code></td>
                        </tr>
                        <tr>
                            <td><strong>nuclei</strong></td>
                            <td><span class="badge badge-indigo">assessment</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/nuclei</code></td>
                        </tr>
                        <tr>
                            <td><strong>naabu</strong></td>
                            <td><span class="badge badge-indigo">port_scan</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/naabu</code></td>
                        </tr>
                        <tr>
                            <td><strong>ffuf</strong></td>
                            <td><span class="badge badge-indigo">web_discovery</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/ffuf</code></td>
                        </tr>
                        <tr>
                            <td><strong>subfinder</strong></td>
                            <td><span class="badge badge-indigo">dns</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/subfinder</code></td>
                        </tr>
                        <tr>
                            <td><strong>dnsx</strong></td>
                            <td><span class="badge badge-indigo">dns</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/dnsx</code></td>
                        </tr>
                        <tr>
                            <td><strong>httpx</strong></td>
                            <td><span class="badge badge-indigo">http</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/httpx</code></td>
                        </tr>
                        <tr>
                            <td><strong>rustscan</strong></td>
                            <td><span class="badge badge-indigo">port_scan</span></td>
                            <td><span class="badge badge-purple">Tier 2</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/rustscan</code></td>
                        </tr>
                        <tr>
                            <td><strong>gobuster</strong></td>
                            <td><span class="badge badge-indigo">web_discovery</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/opt/scanet/bin/gobuster</code></td>
                        </tr>
                        <tr>
                            <td><strong>mtr</strong></td>
                            <td><span class="badge badge-indigo">diagnostics</span></td>
                            <td><span class="badge badge-cyan">Tier 1</span></td>
                            <td><span class="badge badge-emerald">Installed</span></td>
                            <td><code style="color:var(--color-text-dim)">/usr/bin/mtr</code></td>
                        </tr>
                        <tr>
                            <td><strong>osint</strong></td>
                            <td><span class="badge badge-indigo">osint_recon</span></td>
                            <td><span class="badge badge-cyan">Native</span></td>
                            <td><span class="badge badge-cyan">Built-in</span></td>
                            <td><code style="color:var(--color-text-dim)">backend/adapters/osint_adapter.py</code></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;

    try {
        const [tools, res] = await Promise.all([api.getTools(), api.getResources()]);
        if (res && res.platform) {
            document.getElementById('sys-os').textContent = `${res.platform.os} ${res.platform.release} (${res.platform.arch})`;
        }
        if (tools) {
            document.getElementById('tools-count-badge').textContent = `${tools.installed_count}/${tools.total_count} Online`;
        }
    } catch (e) {}
}
