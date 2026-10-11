/**
 * scanet — Client-Side Router
 * Hash-based SPA navigation (#/dashboard, #/targets, etc.)
 */

import { renderDashboard } from './pages/dashboard.js';
import { renderTargets }   from './pages/targets.js';
import { renderJobs }      from './pages/jobs.js';
import { renderResults }   from './pages/results.js';
import { renderSystem }    from './pages/system.js';
import { renderPipelines } from './pages/pipelines.js';
import { renderTopology }  from './pages/topology.js';
import { renderAdvisor }   from './pages/advisor.js';

const ROUTES = {
    ''           : { title: 'Dashboard',             render: renderDashboard },
    'dashboard'  : { title: 'Dashboard',             render: renderDashboard },
    'targets'    : { title: 'Target Manager',        render: renderTargets   },
    'pipelines'  : { title: 'Recon Pipelines',       render: renderPipelines },
    'jobs'       : { title: 'Live Job Center',       render: renderJobs      },
    'topology'   : { title: 'Attack Surface Graph',  render: renderTopology  },
    'results'    : { title: 'Results Explorer',      render: renderResults   },
    'advisor'    : { title: 'AI Security Advisor',   render: renderAdvisor   },
    'system'     : { title: 'System Health',         render: renderSystem    },
};


export const router = {
    _container: null,

    init(container) {
        this._container = container;
        window.addEventListener('hashchange', () => this._navigate());
        this._navigate();
    },

    _navigate() {
        const hash  = window.location.hash.replace('#/', '').split('?')[0];
        const route = ROUTES[hash] || ROUTES['dashboard'];

        // Update page title
        const titleEl = document.getElementById('page-title');
        if (titleEl) titleEl.textContent = route.title;

        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(el => {
            el.classList.toggle('active', el.dataset.route === hash);
        });

        // Render page
        route.render(this._container);
    },

    navigate(path) {
        window.location.hash = `#/${path}`;
    }
};
