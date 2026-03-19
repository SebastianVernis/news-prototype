const API_CONFIG = {
    // Detectar si estamos en localhost para cambiar la URL de la API
    base: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8787/api'
        : 'https://cms-api.sebastianvernis.space/api',
    r2DevUrl: 'https://pub-42bf42f47f554f9791e810e7d0f209d4.r2.dev',
    r2PublicUrl: 'https://uploads.sebastianvernis.space',
    storageKey: 'CMS_AUTH_TOKEN',
    legacyKey: 'CMS_ADMIN_TOKEN'
};

function getToken() {
    // 1. Prioridad: Token de sesión del login moderno
    let token = localStorage.getItem(API_CONFIG.storageKey);
    
    // 2. Fallback: Token administrativo manual (el que pide el modal)
    if (!token) {
        token = localStorage.getItem(API_CONFIG.legacyKey);
    }

    // 3. Contingencia: Parámetro URL (desarrollo)
    const urlToken = new URLSearchParams(window.location.search).get('token');
    if (urlToken) { 
        token = urlToken.trim();
        localStorage.setItem(API_CONFIG.legacyKey, token); 
    }

    return (token || '').trim();
}
function setToken(t) {
    if (t) {
        // Guardamos en ambas para máxima compatibilidad entre módulos
        localStorage.setItem(API_CONFIG.storageKey, t.trim());
        localStorage.setItem(API_CONFIG.legacyKey, t.trim());
    }
}

async function apiFetch(path, options = {}) {
    const headers = Object.assign({}, options.headers || {});

    // Solo setear JSON si no es multipart
    if (!options.isMultipart) {
        headers['Content-Type'] = 'application/json';
    }

    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    // Normalizar path
    let cleanPath = path.startsWith('/') ? path.slice(1) : path;
    if (cleanPath.startsWith('api/')) cleanPath = cleanPath.slice(4);

    const url = `${API_CONFIG.base}/${cleanPath}`;

    try {
        const response = await fetch(url, { ...options, headers });

        if (response.status === 401 || response.status === 403) {
            console.warn('[API] Sesión expirada o no autorizada (401/403)');

            // Si el error viene de un intento de LOGIN, no redirigir (evitar loop)
            if (path.includes('/auth/login')) {
                throw new Error('Credenciales incorrectas');
            }

            // Comportamiento estándar: Redirigir a login y mostrar toast
            if (!window.location.hash.includes('login')) {
                if (typeof showWarningToast === 'function') {
                    showWarningToast('Sesión Expirada', 'Por favor inicia sesión nuevamente', 3000);
                }
                window.location.hash = 'login';
            }
            throw new Error('Sesión expirada');
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
