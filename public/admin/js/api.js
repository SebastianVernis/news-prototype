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

// Modal de autenticación (reemplaza prompt() bloqueante)
function showAuthModal(onSubmit) {
    let modal = document.getElementById('auth-token-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'auth-token-modal';
        modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);z-index:9999;display:flex;align-items:center;justify-content:center;';
        modal.innerHTML = `
            <div style="background:#fff;padding:2rem;border-radius:8px;width:420px;box-shadow:0 10px 40px rgba(0,0,0,0.3);">
                <h3 style="margin-bottom:1rem;color:#2c3e50;"><i class="fas fa-lock"></i> Acceso Restringido</h3>
                <p style="color:#666;margin-bottom:1rem;font-size:0.9rem;">Ingresa el ADMIN_TOKEN para continuar:</p>
                <input id="auth-token-input" type="password" placeholder="Token de administrador"
                    style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:4px;margin-bottom:1rem;font-size:1rem;">
                <div style="display:flex;gap:0.5rem;">
                    <button id="auth-token-submit" style="flex:1;padding:0.75rem;background:#667eea;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:1rem;">
                        <i class="fas fa-check"></i> Confirmar
                    </button>
                    <button id="auth-token-cancel" style="padding:0.75rem 1rem;background:#dc3545;color:#fff;border:none;border-radius:4px;cursor:pointer;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>`;
        document.body.appendChild(modal);
    }
    modal.style.display = 'flex';
    const input = document.getElementById('auth-token-input');
    input.value = '';
    input.focus();

    const submit = () => {
        const val = input.value.trim();
        if (val) { setToken(val); modal.style.display = 'none'; onSubmit(val); }
    };
    document.getElementById('auth-token-submit').onclick = submit;
    document.getElementById('auth-token-cancel').onclick = () => { modal.style.display = 'none'; };
    input.onkeydown = (e) => { if (e.key === 'Enter') submit(); };
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
            return new Promise((resolve, reject) => {
                showAuthModal((newToken) => {
                    apiFetch(path, options).then(resolve).catch(reject);
                });
            });
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
