/** scanet API client — centralized fetch wrapper */
const BASE = '/api/v1';

async function request(path, options = {}) {
    const res = await fetch(`${BASE}${path}`, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    });
    if (!res.ok) throw new Error(`API Error ${res.status}: ${res.statusText}`);
    return res.json();
}

export const api = {
    // System
    getTools:     ()         => request('/system/tools'),
    getResources: ()         => request('/system/resources'),
    getHealth:    ()         => request('/system/health'),

    // Targets
    getTargets:   ()         => request('/targets'),
    createTarget: (data)     => request('/targets', { method: 'POST', body: JSON.stringify(data) }),
    deleteTarget: (id)       => request(`/targets/${id}`, { method: 'DELETE' }),

    // Jobs
    getJobs:      ()         => request('/jobs'),
    getJob:       (id)       => request(`/jobs/${id}`),
    createJob:    (data)     => request('/jobs', { method: 'POST', body: JSON.stringify(data) }),
    cancelJob:    (id)       => request(`/jobs/${id}/cancel`, { method: 'POST' }),

    // Results
    getHosts:     ()         => request('/results/hosts'),
    getEndpoints: ()         => request('/results/endpoints'),
    getFindings:  ()         => request('/results/findings'),
    diffJobs:     (a, b)     => request(`/results/diff?job_a=${a}&job_b=${b}`),
    exportResults:(fmt)      => `/api/v1/results/export/${fmt}`,

    // SSE streaming
    streamJob: (jobId, onLine) => {
        const es = new EventSource(`/api/v1/jobs/${jobId}/stream`);
        es.onmessage = (e) => onLine(e.data);
        es.onerror   = () => es.close();
        return es;
    },
};
