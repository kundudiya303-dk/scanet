/**
 * scanet — Target & Scope Manager Page
 */
export async function renderTargets(container) {
    container.innerHTML = `
        <div class="page-header" style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Target & Scope Authorization Manager</h2>
                <p style="color: var(--color-text-muted);">Manage approved IP addresses, CIDR blocks, and domains for ethical lab reconnaissance.</p>
            </div>
            <button class="btn btn-primary" onclick="alert('Target added to approved whitelist successfully!')">+ Add Authorized Target</button>
        </div>

        <!-- Add Target Card -->
        <div class="card" style="margin-bottom: 2rem; border-left: 4px solid var(--color-primary);">
            <div class="card-title">Register New Target Scope</div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 1rem; align-items: end;">
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Target Value (Hostname / IP / CIDR)</label>
                    <input type="text" class="input" placeholder="e.g. 192.168.1.100 or target.lab" value="192.168.1.50" />
                </div>
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Target Type</label>
                    <select class="input" style="cursor: pointer;">
                        <option>IPv4 Single Host</option>
                        <option>CIDR Subnet Block</option>
                        <option>Domain / FQDN</option>
                    </select>
                </div>
                <div>
                    <label style="font-size: 0.8rem; color: var(--color-text-muted); display: block; margin-bottom: 0.35rem;">Lab Group</label>
                    <input type="text" class="input" placeholder="e.g. CyberLab-A" value="Defense-Course" />
                </div>
                <div>
                    <button class="btn btn-emerald" onclick="alert('Scope validation passed: Target 192.168.1.50 added!')">Verify & Add</button>
                </div>
            </div>
        </div>

        <!-- Whitelisted Targets Table -->
        <div class="card">
            <div class="card-title">
                <span>Currently Whitelisted Targets (4 Active)</span>
                <span class="badge badge-emerald"><span class="badge-pulse"></span> SCOPE ENFORCED</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Target Name</th>
                            <th>Value</th>
                            <th>Type</th>
                            <th>Approval Status</th>
                            <th>Created By</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Metasploitable 2</strong></td>
                            <td><code>192.168.1.100</code></td>
                            <td><span class="badge badge-indigo">IPv4 Host</span></td>
                            <td><span class="badge badge-emerald">Approved</span></td>
                            <td>Instructor (Prof. Alan)</td>
                            <td>
                                <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.3rem 0.6rem;" onclick="window.location.hash='#/jobs'">Scan Target</button>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>OWASP Juice Shop</strong></td>
                            <td><code>juiceshop.lab</code></td>
                            <td><span class="badge badge-cyan">Domain</span></td>
                            <td><span class="badge badge-emerald">Approved</span></td>
                            <td>Admin</td>
                            <td>
                                <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.3rem 0.6rem;" onclick="window.location.hash='#/jobs'">Scan Target</button>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>DVWA Training Node</strong></td>
                            <td><code>192.168.1.150</code></td>
                            <td><span class="badge badge-indigo">IPv4 Host</span></td>
                            <td><span class="badge badge-emerald">Approved</span></td>
                            <td>Instructor (Prof. Alan)</td>
                            <td>
                                <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.3rem 0.6rem;" onclick="window.location.hash='#/jobs'">Scan Target</button>
                            </td>
                        </tr>
                        <tr>
                            <td><strong>Cyber Range Subnet</strong></td>
                            <td><code>10.0.0.0/24</code></td>
                            <td><span class="badge badge-amber">CIDR Block</span></td>
                            <td><span class="badge badge-emerald">Approved</span></td>
                            <td>Admin</td>
                            <td>
                                <button class="btn btn-secondary" style="font-size: 0.78rem; padding: 0.3rem 0.6rem;" onclick="window.location.hash='#/jobs'">Scan Target</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
}
