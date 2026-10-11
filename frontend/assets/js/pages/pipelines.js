/**
 * scanet — Chained Reconnaissance Pipelines & Playbooks Page
 */
import { api } from '../api.js';

export async function renderPipelines(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem;">
            <h2>Reconnaissance Pipelines & Playbooks</h2>
            <p style="color: var(--color-text-muted);">Execute multi-tool automated attack surface workflows in sequence.</p>
        </div>

        <div class="card-grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); margin-bottom: 2rem;">
            <div class="card" style="border-left: 4px solid var(--color-accent);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h3 style="font-size: 1.1rem; margin: 0;">Full Attack Surface Recon</h3>
                    <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">6 Tools</span>
                </div>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                    Passive Subdomain Discovery ➔ DNS Resolution ➔ Fast Port Screening ➔ Nmap Services ➔ HTTPX Probing ➔ Nuclei Audit.
                </p>
                <div style="font-size: 0.8rem; background: var(--color-bg-base); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-family: monospace;">
                    subfinder ➔ dnsx ➔ naabu ➔ nmap ➔ httpx ➔ nuclei
                </div>
                <button class="btn btn-primary" onclick="alert('Starting Full Attack Surface Pipeline against target...')">Launch Full Pipeline</button>
            </div>

            <div class="card" style="border-left: 4px solid #10b981;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h3 style="font-size: 1.1rem; margin: 0;">Web App Security Audit</h3>
                    <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">4 Tools</span>
                </div>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                    Deep Crawler ➔ Web Directory Fuzzing ➔ TLS & Security Headers ➔ Misconfiguration Auditing.
                </p>
                <div style="font-size: 0.8rem; background: var(--color-bg-base); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-family: monospace;">
                    katana ➔ ffuf ➔ httpx ➔ nuclei
                </div>
                <button class="btn btn-secondary" onclick="alert('Starting Web App Security Audit Pipeline...')">Launch Web Pipeline</button>
            </div>

            <div class="card" style="border-left: 4px solid #f59e0b;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h3 style="font-size: 1.1rem; margin: 0;">Network Route & Diagnostics</h3>
                    <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">3 Tools</span>
                </div>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                    MTR Hop Latency ➔ All-Port Screening ➔ Service Version Probing ➔ Subnet CIDR Calculation.
                </p>
                <div style="font-size: 0.8rem; background: var(--color-bg-base); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-family: monospace;">
                    mtr ➔ naabu ➔ nmap ➔ subnet
                </div>
                <button class="btn btn-secondary" onclick="alert('Starting Network Diagnostics Pipeline...')">Launch Diagnostics</button>
            </div>

            <div class="card" style="border-left: 4px solid #06b6d4;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h3 style="font-size: 1.1rem; margin: 0;">Stealth Passive OSINT</h3>
                    <span class="badge" style="background: rgba(6, 182, 212, 0.2); color: #22d3ee;">100% Passive</span>
                </div>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
                    Zero target packets. Collects Subfinder records, crt.sh Cert Transparency, WHOIS, and IP Geolocation / ASN.
                </p>
                <div style="font-size: 0.8rem; background: var(--color-bg-base); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-family: monospace;">
                    subfinder ➔ crt.sh ➔ ip-api ➔ rdap
                </div>
                <button class="btn btn-secondary" onclick="alert('Starting Passive OSINT Pipeline...')">Launch OSINT</button>
            </div>
        </div>

        <div class="card">
            <h3>Active Pipeline Execution Progress</h3>
            <div style="margin-top: 1rem; color: var(--color-text-muted);">
                Select and launch a pipeline above to monitor multi-stage tool execution in real time.
            </div>
        </div>
    `;
}
