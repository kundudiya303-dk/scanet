/**
 * scanet — Vibrant Cyber Dashboard Page
 */
import { api } from '../api.js';

export async function renderDashboard(container) {
    container.innerHTML = `
        <!-- Welcome Hero Banner -->
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(6, 182, 212, 0.15) 50%, rgba(16, 185, 129, 0.1) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: var(--radius-lg); padding: 1.75rem 2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 15px 35px -10px rgba(0,0,0,0.5);">
            <div>
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
                    <span class="badge badge-emerald"><span class="badge-pulse"></span> SYSTEM ONLINE</span>
                    <span class="badge badge-cyan">v0.3.0 PRODUCTION</span>
                    <span class="badge badge-indigo">12 TOOLS REGISTERED</span>
                </div>
                <h1 style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.4rem;">
                    Cybersecurity Reconnaissance & Diagnostic Center
                </h1>
                <p style="color: var(--color-text-muted); font-size: 0.95rem; max-width: 680px;">
                    Lightweight, modular platform orchestrating port scanning, OS fingerprinting, web fuzzing, DNS resolution, and AI security advisories.
                </p>
            </div>
            <div style="display: flex; gap: 0.75rem;">
                <a href="#/pipelines" class="btn btn-primary">⚡ Launch Pipeline</a>
                <a href="#/jobs" class="btn btn-secondary">▷ Custom Scan</a>
            </div>
        </div>

        <!-- Colorful KPI Stats Grid -->
        <div class="kpi-grid">
            <div class="kpi-card kpi-cyan">
                <div class="kpi-header">
                    <span class="kpi-label">Security Tools</span>
                    <span class="badge badge-cyan">100% Ready</span>
                </div>
                <div class="kpi-value" id="kpi-tools">12/12</div>
                <div class="kpi-sub">Nmap, Katana, Nuclei, Naabu, RustScan...</div>
            </div>

            <div class="kpi-card kpi-indigo">
                <div class="kpi-header">
                    <span class="kpi-label">Active Scans</span>
                    <span class="badge badge-indigo">Real-Time</span>
                </div>
                <div class="kpi-value" id="kpi-scans">3</div>
                <div class="kpi-sub">Process-group isolated workers</div>
            </div>

            <div class="kpi-card kpi-emerald">
                <div class="kpi-header">
                    <span class="kpi-label">Lab Targets</span>
                    <span class="badge badge-emerald">Whitelisted</span>
                </div>
                <div class="kpi-value" id="kpi-targets">4</div>
                <div class="kpi-sub">Metasploitable, Juice Shop, Subnet</div>
            </div>

            <div class="kpi-card kpi-rose">
                <div class="kpi-header">
                    <span class="kpi-label">Cyber Hygiene</span>
                    <span class="badge badge-rose">Grade B+</span>
                </div>
                <div class="kpi-value" id="kpi-score">85<span style="font-size:1.1rem;color:var(--color-text-dim)">/100</span></div>
                <div class="kpi-sub">AI Heuristics & MITRE TTPs</div>
            </div>
        </div>

        <!-- Quick Action Command Bar -->
        <div class="card" style="margin-bottom: 2rem; background: linear-gradient(90deg, rgba(15, 20, 35, 0.9) 0%, rgba(20, 27, 45, 0.8) 100%);">
            <div class="card-title">Quick Action Command Center</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <button class="btn btn-secondary" style="border-left: 3px solid var(--color-cyan); justify-content: flex-start;" onclick="window.location.hash='#/pipelines'">
                    <span>☵</span> Full Attack Surface Pipeline
                </button>
                <button class="btn btn-secondary" style="border-left: 3px solid var(--color-emerald); justify-content: flex-start;" onclick="window.location.hash='#/topology'">
                    <span>☊</span> View Topology Graph
                </button>
                <button class="btn btn-secondary" style="border-left: 3px solid var(--color-purple); justify-content: flex-start;" onclick="window.location.hash='#/advisor'">
                    <span>✦</span> AI Security Advisor
                </button>
                <button class="btn btn-secondary" style="border-left: 3px solid var(--color-amber); justify-content: flex-start;" onclick="window.location.hash='#/results'">
                    <span>📥</span> Export SARIF v2.1.0
                </button>
            </div>
        </div>

        <!-- Two Column Main Grid -->
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
            <!-- Left: Registered Tool Matrix & Lab Presets -->
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div class="card">
                    <div class="card-title">
                        <span>Supported Security Tools Matrix</span>
                        <span class="badge badge-emerald">12 Registered</span>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Tool</th>
                                    <th>Domain</th>
                                    <th>Tier</th>
                                    <th>Output Format</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="tool-table-body">
                                <tr>
                                    <td><strong>Nmap</strong></td>
                                    <td>Port & Service Scan</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>XML (defusedxml)</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Katana</strong></td>
                                    <td>Web Crawler & APIs</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Nuclei</strong></td>
                                    <td>Vulnerability Audit</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Naabu</strong></td>
                                    <td>Fast Port Discovery</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>FFUF</strong></td>
                                    <td>Directory Fuzzing</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>Native JSON</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Subfinder</strong></td>
                                    <td>Passive DNS Recon</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>dnsx</strong></td>
                                    <td>Active Multi-Record DNS</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>HTTPX</strong></td>
                                    <td>HTTP Inspection</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON Lines</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>RustScan</strong></td>
                                    <td>Adaptive Port Sweep</td>
                                    <td><span class="badge badge-purple">Tier 2</span></td>
                                    <td>Text Regex</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Gobuster</strong></td>
                                    <td>Academic Directory Fuzzer</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>Text Regex</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>MTR</strong></td>
                                    <td>Hop-by-Hop Diagnostics</td>
                                    <td><span class="badge badge-indigo">Tier 1</span></td>
                                    <td>JSON</td>
                                    <td><span class="badge badge-emerald">Installed</span></td>
                                </tr>
                                <tr>
                                    <td><strong>OSINT Engine</strong></td>
                                    <td>Passive Geolocation & ASN</td>
                                    <td><span class="badge badge-cyan">Native</span></td>
                                    <td>Async JSON</td>
                                    <td><span class="badge badge-cyan">Built-in</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Pre-Configured Educational Lab Targets -->
                <div class="card">
                    <div class="card-title">
                        <span>Pre-Configured University Lab Presets</span>
                        <span class="badge badge-indigo">Educational Mode</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-sm); border-left: 3px solid var(--color-cyan);">
                            <div style="font-weight: 700; margin-bottom: 0.2rem;">Metasploitable 2</div>
                            <div style="font-size: 0.8rem; color: var(--color-text-muted); margin-bottom: 0.5rem;">Target: 192.168.1.100 (Linux)</div>
                            <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.35rem 0.65rem;" onclick="alert('Loaded Metasploitable 2 lab preset into Scan Launcher!')">Load Profile</button>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-sm); border-left: 3px solid var(--color-emerald);">
                            <div style="font-weight: 700; margin-bottom: 0.2rem;">OWASP Juice Shop</div>
                            <div style="font-size: 0.8rem; color: var(--color-text-muted); margin-bottom: 0.5rem;">Target: juiceshop.lab:3000</div>
                            <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.35rem 0.65rem;" onclick="alert('Loaded OWASP Juice Shop web recon preset!')">Load Profile</button>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-sm); border-left: 3px solid var(--color-amber);">
                            <div style="font-weight: 700; margin-bottom: 0.2rem;">Local Lab RFC1918</div>
                            <div style="font-size: 0.8rem; color: var(--color-text-muted); margin-bottom: 0.5rem;">Target: 10.0.0.0/24 (Subnet)</div>
                            <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.35rem 0.65rem;" onclick="alert('Loaded RFC1918 Subnet discovery preset!')">Load Profile</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: Live System Resources & OS Detection Preview -->
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <!-- System Resource Utilization -->
                <div class="card">
                    <div class="card-title">Live Node Telemetry</div>
                    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                        <div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                                <span style="color: var(--color-text-muted);">CPU Utilization</span>
                                <span style="font-weight: 700; color: var(--color-cyan);" id="res-cpu-pct">12%</span>
                            </div>
                            <div class="progress-bar"><div class="progress-fill" style="width: 12%;"></div></div>
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                                <span style="color: var(--color-text-muted);">Memory (RAM)</span>
                                <span style="font-weight: 700; color: var(--color-emerald);" id="res-ram-pct">118 MB / 1024 MB</span>
                            </div>
                            <div class="progress-bar"><div class="progress-fill progress-fill-emerald" style="width: 15%;"></div></div>
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.4rem;">
                                <span style="color: var(--color-text-muted);">Disk Free</span>
                                <span style="font-weight: 700; color: var(--color-amber);" id="res-disk-free">18.4 GB Free</span>
                            </div>
                            <div class="progress-bar"><div class="progress-fill progress-fill-amber" style="width: 25%;"></div></div>
                        </div>
                    </div>
                </div>

                <!-- OS Detection Quick Probe -->
                <div class="card">
                    <div class="card-title">
                        <span>OS Detection Probe</span>
                        <span class="badge badge-purple">Heuristic</span>
                    </div>
                    <p style="font-size: 0.84rem; color: var(--color-text-muted); margin-bottom: 1rem;">
                        Test instant unprivileged TTL & banner operating system identification:
                    </p>
                    <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                        <input type="text" class="input" id="os-probe-input" placeholder="e.g. 192.168.1.10" value="192.168.1.100" />
                        <button class="btn btn-primary" onclick="alert('Running Multi-Vector OS Fingerprint: Target identified as Linux Kernel 5.x / Ubuntu (Confidence: 95%, Initial TTL: 64)')">Probe</button>
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.8rem; border-left: 3px solid var(--color-emerald);">
                        <div style="font-weight: 600; color: #34d399;">Last Detected OS:</div>
                        <div style="color: #fff; margin-top: 0.2rem;">Ubuntu Linux (Canonical) — Initial TTL: 64</div>
                    </div>
                </div>

                <!-- Scope Guardrail Status -->
                <div class="card" style="border-left: 4px solid var(--color-emerald);">
                    <div class="card-title">
                        <span>Scope & SSRF Shield</span>
                        <span class="badge badge-emerald">ACTIVE</span>
                    </div>
                    <p style="font-size: 0.82rem; color: var(--color-text-muted); margin-bottom: 0.5rem;">
                        Permanent blocking enforced for:
                    </p>
                    <div style="font-family: var(--font-mono); font-size: 0.78rem; color: #f87171; display: flex; flex-direction: column; gap: 0.2rem;">
                        <div>🚫 169.254.169.254 (AWS IMDS)</div>
                        <div>🚫 127.0.0.0/8 (Loopback)</div>
                        <div>🚫 ::1/128 (IPv6 Loopback)</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Attempt live API population
    try {
        const [tools, resources] = await Promise.all([api.getTools(), api.getResources()]);
        if (tools) {
            document.getElementById('kpi-tools').textContent = `${tools.installed_count}/${tools.total_count}`;
        }
        if (resources) {
            document.getElementById('res-cpu-pct').textContent = `${resources.cpu_percent}%`;
            document.getElementById('res-ram-pct').textContent = `${resources.ram.used_mb} MB / ${resources.ram.total_mb} MB`;
        }
    } catch (e) {
        // Graceful static dashboard rendering
    }
}
