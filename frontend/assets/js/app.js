/**
 * scanet — Main Application Entry Point (ES6 Module)
 * Bootstraps the SPA router, sidebar navigation, and initial page load.
 */

import { router }    from './router.js';
import { renderNav } from './components/nav.js';

async function boot() {
    const app = document.getElementById('app');

    // Build the shell layout
    app.innerHTML = `
        <div id="app-shell">
            <nav class="sidebar" id="sidebar"></nav>
            <header class="topbar" id="topbar">
                <span class="topbar-title" id="page-title">Dashboard</span>
                <div class="topbar-badges" id="topbar-badges"></div>
            </header>
            <main class="content" id="content"></main>
        </div>
    `;

    // Render navigation links
    renderNav(document.getElementById('sidebar'));

    // Start the router (handles URL hash-based navigation)
    router.init(document.getElementById('content'));
}

// Boot the application
boot().catch(err => {
    console.error('[scanet] Boot failed:', err);
    document.getElementById('app').innerHTML =
        `<div style="padding:2rem;color:#ef4444">
            <h2>Application failed to start</h2>
            <p>${err.message}</p>
        </div>`;
});
