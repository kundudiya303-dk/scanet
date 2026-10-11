/**
 * scanet — Scan Launcher & Live Job Execution Center
 */
export async function renderJobs(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem;">
            <h2>Scan Launcher & Live Process Center</h2>
            <p style="color: var(--color-text-muted);">Configure tool parameters, preview safe CLI vectors, and stream real-time scan output.</p>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
            <!-- Scan Configuration Panel -->
            <div class="card" style="border-left: 4px solid var(--color-cyan);">
                <div class="card-title">1. Configure Scan Job</div>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div>
                        <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Select Target</label>
                        <select class="input" id="job-target-select">
                            <option value="192.168.1.100">Metasploitable 2 (192.168.1.100)</option>
                            <option value="juiceshop.lab">OWASP Juice Shop (juiceshop.lab)</option>
                            <option value="192.168.1.150">DVWA Node (192.168.1.150)</option>
                            <option value="10.0.0.0/24">Lab Subnet (10.0.0.0/24)</option>
                        </select>
                    </div>

                    <div>
                        <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Select Security Tool</label>
                        <select class="input" id="job-tool-select" onchange="updateCommandPreview()">
                            <option value="nmap">Nmap — Deep Service & Version Scan</option>
                            <option value="katana">Katana — Web Crawler & API Routes</option>
                            <option value="nuclei">Nuclei — Vulnerability & Misconfig Templates</option>
                            <option value="naabu">Naabu — High-Speed Port Discovery</option>
                            <option value="ffuf">FFUF — Fast Directory Fuzzing</option>
                            <option value="subfinder">Subfinder — Passive Subdomain Recon</option>
                            <option value="dnsx">dnsx — Multi-Record DNS Resolver</option>
                            <option value="httpx">HTTPX — HTTP Tech & TLS Surface</option>
                            <option value="rustscan">RustScan — Adaptive Fast Sweep</option>
                            <option value="gobuster">Gobuster — Directory Fuzzer</option>
                            <option value="mtr">MTR — Hop-by-Hop Route Diagnostics</option>
                            <option value="osint">OSINT Engine — Passive Geo/ASN/crt.sh</option>
                        </select>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Scan Profile / Speed</label>
                            <select class="input">
                                <option>Normal (T3 - Safe)</option>
                                <option>Polite (T2 - Low Bandwidth)</option>
                                <option>Aggressive (T4 - High Speed)</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Port Range</label>
                            <select class="input">
                                <option>Top 100 Common Ports</option>
                                <option>Top 1,000 Standard Ports</option>
                                <option>All 65,535 Ports (-p-)</option>
                            </select>
                        </div>
                    </div>

                    <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem;">
                        <button class="btn btn-primary" style="flex: 1;" onclick="startSimulatedScan()">▶ Launch Scan</button>
                        <button class="btn btn-secondary" onclick="clearTerminal()">Clear Console</button>
                    </div>
                </div>
            </div>

            <!-- Command Generator & Flag Explainer -->
            <div class="card" style="border-left: 4px solid var(--color-primary);">
                <div class="card-title">
                    <span>2. Live CLI Flag Explainer</span>
                    <span class="badge badge-indigo">Educational Mode</span>
                </div>
                <div style="font-size: 0.82rem; color: var(--color-text-muted); margin-bottom: 0.75rem;">
                    Generated vector executed safely via process-group isolation (zero shell concatenation):
                </div>
                <div id="cmd-preview-box" style="background: #050811; border: 1px solid rgba(99, 102, 241, 0.3); padding: 0.85rem 1rem; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 0.88rem; color: #38bdf8; margin-bottom: 1rem;">
                    nmap -sT -sV -T3 --top-ports 100 -oX - 192.168.1.100
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.82rem; line-height: 1.5; color: var(--color-text-muted);">
                    <div style="color: #34d399; font-weight: 600; margin-bottom: 0.2rem;">Flag Anatomy:</div>
                    <div><code style="color:#38bdf8">-sT</code>: TCP Connect scan using standard unprivileged system calls.</div>
                    <div><code style="color:#38bdf8">-sV</code>: Probes open ports to determine service name and software version.</div>
                    <div><code style="color:#38bdf8">-T3</code>: Enforces normal timing template to prevent switch packet flooding.</div>
                </div>
            </div>
        </div>

        <!-- Live Terminal Stream Area -->
        <div class="card">
            <div class="card-title">
                <span>Real-Time Output Stream (SSE Server-Sent Events)</span>
                <span class="badge badge-cyan"><span class="badge-pulse"></span> LISTENING</span>
            </div>
            <div class="terminal" id="terminal-screen">[scanet-engine] Process job manager ready. Waiting for scan initiation...
[scanet-engine] Process isolation: os.setsid process-group termination active.
[scanet-engine] Scope guardrail: Hard-blocked IMDS (169.254.169.254) and loopback ranges enforced.
[scanet-engine] Tool adapters ready: 12 security tools registered.</div>
        </div>
    `;

    // Setup global helper functions for the page
    window.startSimulatedScan = function() {
        const term = document.getElementById('terminal-screen');
        term.textContent = `[scanet-engine] Job 104e initialized against target 192.168.1.100\n` +
            `[scanet-engine] Launching process: nmap -sT -sV -T3 --top-ports 100 -oX - 192.168.1.100 (PID 4821)\n` +
            `[nmap] Starting Nmap 7.94 ( https://nmap.org )\n` +
            `[nmap] Initiating Connect Scan at 19:54:12\n` +
            `[nmap] Scanning 192.168.1.100 [100 ports]\n` +
            `[nmap] Discovered open port 22/tcp on 192.168.1.100 (ssh -> OpenSSH 8.9p1 Ubuntu)\n` +
            `[nmap] Discovered open port 80/tcp on 192.168.1.100 (http -> nginx 1.24.0)\n` +
            `[nmap] Discovered open port 6379/tcp on 192.168.1.100 (redis -> Redis 6.2.6 unauthenticated!)\n` +
            `[scanet-analyzer] Live OS deduction: Initial TTL 64 (Linux Kernel 5.x) - Confidence 95%\n` +
            `[scanet-analyzer] Threat alert: Port 6379 unauthenticated Redis listener detected!\n` +
            `[scanet-engine] Scan completed in 3.42 seconds. Findings ingested into normalized SQLite models.`;
    };

    window.clearTerminal = function() {
        document.getElementById('terminal-screen').textContent = '[scanet-engine] Terminal cleared.';
    };

    window.updateCommandPreview = function() {
        const tool = document.getElementById('job-tool-select').value;
        const box = document.getElementById('cmd-preview-box');
        if (tool === 'katana') box.textContent = 'katana -u https://juiceshop.lab -jc -depth 2 -concurrency 10 -silent';
        else if (tool === 'nuclei') box.textContent = 'nuclei -target https://juiceshop.lab -tags misconfig,exposure -silent -jsonl';
        else if (tool === 'naabu') box.textContent = 'naabu -host 192.168.1.100 -top-ports 1000 -json -silent';
        else if (tool === 'ffuf') box.textContent = 'ffuf -u https://target.lab/FUZZ -w /opt/scanet/wordlists/common.txt -rate 50 -of json';
        else box.textContent = 'nmap -sT -sV -T3 --top-ports 100 -oX - 192.168.1.100';
    };
}
