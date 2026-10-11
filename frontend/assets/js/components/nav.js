/**
 * scanet — Sidebar Navigation Component
 */
export function renderNav(container) {
    container.innerHTML = `
        <div class="sidebar-logo-container">
            <a href="#/dashboard" class="sidebar-logo-link" title="scanet Cybersecurity Reconnaissance">
                <div class="sidebar-logo-badge">
                    <img src="/assets/images/scanet_emblem.svg" alt="scanet emblem" class="sidebar-logo-img" />
                </div>
                <div class="sidebar-logo-text">
                    <span class="logo-title">scan<span class="logo-net">et</span></span>
                    <span class="logo-subtitle">CYBER RECON</span>
                </div>
            </a>
        </div>

        <span class="nav-section-label">Overview</span>
        <a class="nav-item" data-route="dashboard" href="#/dashboard">
            <span class="nav-icon">◈</span> Dashboard
        </a>

        <span class="nav-section-label">Reconnaissance</span>
        <a class="nav-item" data-route="targets"   href="#/targets">
            <span class="nav-icon">⊹</span> Target Manager
        </a>
        <a class="nav-item" data-route="pipelines" href="#/pipelines">
            <span class="nav-icon">☵</span> Recon Pipelines
        </a>
        <a class="nav-item" data-route="jobs"      href="#/jobs">
            <span class="nav-icon">▷</span> Scan Launcher
        </a>
        <a class="nav-item" data-route="topology"  href="#/topology">
            <span class="nav-icon">☊</span> Topology Graph
        </a>
        <a class="nav-item" data-route="results"   href="#/results">
            <span class="nav-icon">≡</span> Results Explorer
        </a>

        <span class="nav-section-label">Intelligence & AI</span>
        <a class="nav-item" data-route="advisor"   href="#/advisor">
            <span class="nav-icon">✦</span> AI Security Advisor
        </a>

        <span class="nav-section-label">Platform</span>
        <a class="nav-item" data-route="system"    href="#/system">
            <span class="nav-icon">⊕</span> System Health
        </a>

    `;
}
