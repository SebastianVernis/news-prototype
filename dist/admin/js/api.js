const API_CONFIG = { 
    // Si estamos en localhost, llamamos directo al puerto del Worker (8781)
    // saltándonos el proxy de Pages para evitar recibir HTML por error.
    base: window.location.hostname === 'localhost' ? 'https://news-api.sebastianvernis.workers.dev/api' : '/api',
    storageKey: 'CMS_ADMIN_TOKEN' 
};

function getToken() { return (localStorage.getItem(API_CONFIG.storageKey) || '').trim(); }
function setToken(t) { if (t) localStorage.setItem(API_CONFIG.storageKey, t.trim()); }

async function apiFetch(path, options = {}) {
    const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    // Normalizar path
    let cleanPath = path.startsWith('/') ? path.slice(1) : path;
    if (cleanPath.startsWith('api/')) cleanPath = cleanPath.slice(4);
    
    const url = `${API_CONFIG.base}/${cleanPath}`;

    try {
        const response = await fetch(url, { ...options, headers });

        if (response.status === 401 || response.status === 403) {
            const nt = prompt('Acceso Denegado. Ingresa el ADMIN_TOKEN:');
            if (nt) { setToken(nt); return apiFetch(path, options); }
        }

        if (!response.ok) {
            const errorBody = await response.json().catch(() => ({}));
            throw new Error(errorBody.error || `HTTP ${response.status}`);
        }

        return await response.json();
    } catch (e) {
        console.error(`Error en apiFetch [${url}]:`, e.message);
        throw e;
    }
}
