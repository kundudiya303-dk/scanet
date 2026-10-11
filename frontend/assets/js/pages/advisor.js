/**
 * scanet — AI Security Advisory & MITRE ATT&CK Copilot Page
 */
export async function renderAdvisor(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem;">
            <h2>AI Security Advisor & MITRE ATT&CK Copilot</h2>
            <p style="color: var(--color-text-muted);">Heuristic threat analysis, educational student explanations, and automated remediation playbooks.</p>
        </div>

        <!-- Hygiene Score Banner -->
        <div class="card" style="margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; border-left: 4px solid #10b981;">
            <div>
                <h3 style="margin-bottom: 0.25rem;">Overall Security Posture & Cyber Hygiene</h3>
                <p style="color: var(--color-text-muted); font-size: 0.9rem; margin: 0;">Evaluation of port exposure, TLS configurations, and HTTP defense posture.</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.2rem; font-weight: 800; color: #10b981;">85<span style="font-size: 1.1rem; color: var(--color-text-muted);">/100</span></div>
                <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">Posture Grade: B+</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem;">
            <!-- Priority Advisories -->
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="card" style="border-left: 4px solid #ef4444;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <div>
                            <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #ef4444; margin-right: 0.5rem;">CRITICAL</span>
                            <span style="font-weight: 700; font-size: 1.05rem;">Insecure Cleartext Protocol (FTP Port 21)</span>
                        </div>
                        <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">T1040 - Network Sniffing</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 0.75rem;">
                        FTP transmits user credentials and session tokens in cleartext over the wire, allowing attackers on the local network or ISP path to capture credentials via passive packet sniffing.
                    </p>
                    <div style="background: var(--color-bg-base); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.85rem;">
                        <span style="color: #34d399; font-weight: 600;">Remediation Playbook:</span><br/>
                        1. Decommission vsftpd/proftpd listener: <code>sudo systemctl stop vsftpd</code><br/>
                        2. Transition users to SFTP on port 22 or enforce TLS 1.3 encrypted FTPS sessions.
                    </div>
                </div>

                <div class="card" style="border-left: 4px solid #f59e0b;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <div>
                            <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; margin-right: 0.5rem;">MEDIUM</span>
                            <span style="font-weight: 700; font-size: 1.05rem;">Missing HTTP Defensive Headers (Grade D)</span>
                        </div>
                        <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #818cf8;">T1189 - Drive-by Compromise</span>
                    </div>
                    <p style="color: var(--color-text-muted); font-size: 0.9rem; margin-bottom: 0.75rem;">
                        Target web server lacks <code>Content-Security-Policy</code> and <code>X-Frame-Options</code>, leaving web clients exposed to Clickjacking and Cross-Site Scripting (XSS).
                    </p>
                    <div style="background: var(--color-bg-base); padding: 0.75rem; border-radius: var(--radius-sm); font-size: 0.85rem;">
                        <span style="color: #34d399; font-weight: 600;">Remediation Playbook:</span><br/>
                        Add security headers in Nginx configuration:<br/>
                        <code>add_header X-Frame-Options "DENY"; add_header Content-Security-Policy "default-src 'self'";</code>
                    </div>
                </div>
            </div>

            <!-- Compliance & MITRE Framework Card -->
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="card">
                    <h3>Compliance Mapping</h3>
                    <div style="margin-top: 1rem; font-size: 0.88rem; display: flex; flex-direction: column; gap: 0.75rem;">
                        <div>
                            <div style="font-weight: 600;">OWASP Top 10 (2021)</div>
                            <div style="color: #f87171;">A05: Security Misconfiguration (Non-compliant)</div>
                        </div>
                        <div>
                            <div style="font-weight: 600;">CIS Controls v8</div>
                            <div style="color: #34d399;">Control 4: Secure Asset Configuration (Pass)</div>
                        </div>
                        <div>
                            <div style="font-weight: 600;">NIST CSF 2.0</div>
                            <div style="color: #34d399;">PR.IP: Baseline Config Verification (Pass)</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h3>Correlated CVE Matches</h3>
                    <div style="margin-top: 0.75rem; font-size: 0.85rem;">
                        <div style="padding: 0.5rem; background: var(--color-bg-base); border-radius: var(--radius-sm); margin-bottom: 0.5rem;">
                            <div style="font-weight: 600; color: #ef4444;">CVE-2024-6387 (regreSSHion)</div>
                            <div style="color: var(--color-text-muted);">OpenSSH 8.5p1–9.7p1 RCE (CISA KEV)</div>
                        </div>
                        <div style="padding: 0.5rem; background: var(--color-bg-base); border-radius: var(--radius-sm);">
                            <div style="font-weight: 600; color: #f59e0b;">CVE-2021-41773 (Path Traversal)</div>
                            <div style="color: var(--color-text-muted);">Apache 2.4.49 (CVSS 9.8)</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}
