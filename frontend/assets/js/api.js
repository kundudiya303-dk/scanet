/** scanet API client — centralized fetch wrapper */
const BASE = '/api/v1';

async function request(path, options = {}) {
    const res = await fetch(`${BASE}${path}`, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    });
    if (!res.ok) {
        // Try to parse a structured error detail from FastAPI
        let msg = `API Error ${res.status}: ${res.statusText}`;
        try {
            const body = await res.json();
            if (body.detail) msg = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
        } catch {}
        throw new Error(msg);
    }
    return res.json();
}

export const api = {
    // System
    getTools:     ()         => request('/system/tools'),
    getResources: ()         => request('/system/resources'),
    getHealth:    ()         => request('/system/health'),

    // Targets
    getTargets:   ()         => request('/targets'),
    getTarget:    (id)       => request(`/targets/${id}`),
    createTarget: (data)     => request('/targets', { method: 'POST', body: JSON.stringify(data) }),
    deleteTarget: (id)       => request(`/targets/${id}`, { method: 'DELETE' }),

    // Jobs
    getJobs:      ()         => request('/jobs'),
    getJob:       (id)       => request(`/jobs/${id}`),
    createJob:    (data)     => request('/jobs', { method: 'POST', body: JSON.stringify(data) }),
    cancelJob:    (id)       => request(`/jobs/${id}/cancel`, { method: 'POST' }),

    // Results
    getHosts:     (jobId)    => request(`/results/hosts${jobId ? '?job_id=' + jobId : ''}`),
    getEndpoints: (jobId)    => request(`/results/endpoints${jobId ? '?job_id=' + jobId : ''}`),
    getFindings:  (jobId)    => request(`/results/findings${jobId ? '?job_id=' + jobId : ''}`),
    diffJobs:     (a, b)     => request(`/results/diff?job_a=${a}&job_b=${b}`),
    exportResults:(fmt, jobId) => `/api/v1/results/export/${fmt}${jobId ? '?job_id=' + jobId : ''}`,

    // SSE streaming — real live output from subprocess
    streamJob: (jobId, onLine) => {
        const es = new EventSource(`/api/v1/jobs/${jobId}/stream`);
        es.onmessage = (e) => onLine(e.data);
        es.onerror   = () => es.close();
        return es;
    },

    // Advisor
    analyzeAdvisory: (data)  => request('/advisor/analyze', { method: 'POST', body: JSON.stringify(data) }),
    getMitreKnowledge: ()    => request('/advisor/mitre-knowledge'),

    // Pipelines
    getPipelines:    ()               => request('/pipelines/presets'),
    executePipeline: (presetId, data) => request(`/pipelines/execute/${presetId}`, { method: 'POST', body: JSON.stringify(data) }),

    // Topology
    getTopology:     (targetId)       => request(`/topology/graph${targetId ? '/' + targetId : ''}`),

    // Web Security Auditor
    scanWebSecurity:   (url)           => request('/web-audit/scan', { method: 'POST', body: JSON.stringify({ target_url: url }) }),
    checkTakeover:     (domain, cname) => request('/web-audit/takeover', { method: 'POST', body: JSON.stringify({ domain, cname }) }),
    checkZoneTransfer: (domain, ns)    => request('/web-audit/zone-transfer', { method: 'POST', body: JSON.stringify({ domain, nameserver: ns }) }),
    getAuditRules:     ()              => request('/web-audit/rules'),
};
