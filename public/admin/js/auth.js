// ============================================
// Sistema de Autenticación con Usuario/Contraseña
// ============================================

const Auth = {
    // Claves para localStorage
    STORAGE_KEY: 'CMS_USER_SESSION',
    TOKEN_KEY: 'CMS_AUTH_TOKEN',
    
    // Obtener sesión actual
    getSession() {
        const session = localStorage.getItem(this.STORAGE_KEY);
        return session ? JSON.parse(session) : null;
    },
    
    // Obtener token
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY) || '';
    },
    
    // Verificar si está autenticado
    isAuthenticated() {
        const session = this.getSession();
        const token = this.getToken();
        return !!(session && session.user && token);
    },
    
    // Login con usuario y contraseña
    async login(username, password) {
        try {
            // Llamar al endpoint de login
            const response = await fetch(`${window.ADMIN_API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.error || 'Error en el login');
            }
            
            const data = await response.json();
            
            if (data.token && data.user) {
                // Limpiar cualquier dato de sesión anterior
                localStorage.removeItem('CMS_ADMIN_TOKEN');
                
                // Guardar sesión y token
                localStorage.setItem(this.STORAGE_KEY, JSON.stringify({
                    user: data.user,
                    loginTime: new Date().toISOString()
                }));
                localStorage.setItem(this.TOKEN_KEY, data.token);
                
                // Actualizar UI
                updateUserUI();
                
                return { success: true, user: data.user };
            }
            
            throw new Error('Respuesta inválida del servidor');
        } catch (e) {
            console.error('Error en login:', e);
            throw e;
        }
    },
    
    // Logout - limpia TODO
    logout() {
        // Limpiar TODOS los datos de sesión
        localStorage.removeItem(this.STORAGE_KEY);
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem('CMS_ADMIN_TOKEN');
        
        // Actualizar UI
        updateUserUI();
        
        // Redireccionar a login
        window.location.hash = 'login';
    },
    
    // Obtener información del usuario actual
    getCurrentUser() {
        const session = this.getSession();
        return session ? session.user : null;
    }
};

// Funciones globales para usar en el HTML
window.Auth = Auth;

// Función para actualizar la UI del usuario
function updateUserUI() {
    const userSection = document.getElementById('user-info-section');
    const userAvatar = document.getElementById('user-avatar');
    const userName = document.getElementById('user-name');
    const userRole = document.getElementById('user-role');
    
    if (Auth.isAuthenticated()) {
        const user = Auth.getCurrentUser();
        if (user && userSection) {
            userSection.style.display = 'block';
            if (userAvatar) userAvatar.textContent = user.name ? user.name.charAt(0).toUpperCase() : 'U';
            if (userName) userName.textContent = user.name || 'Usuario';
            if (userRole) userRole.textContent = user.role || 'Editor';
        }
    } else {
        if (userSection) userSection.style.display = 'none';
    }
}

// Modificar el Router para verificar autenticación
function setupAuthRouter() {
    if (typeof Router === 'undefined') {
        setTimeout(setupAuthRouter, 100);
        return;
    }
    
    const originalNavigate = Router.navigate.bind(Router);
    
    Router.navigate = async function(view, pushState = true) {
        // Rutas públicas que no requieren auth
        const publicViews = ['login'];
        
        // Verificar autenticación - SIEMPRE requiere login ahora
        if (!publicViews.includes(view)) {
            if (!Auth.isAuthenticated()) {
                console.log('No autenticado, redireccionando a login...');
                window.location.hash = 'login';
                return;
            }
        }
        
        // Si va a login y ya está autenticado, ir al dashboard
        if (view === 'login' && Auth.isAuthenticated()) {
            window.location.hash = 'dashboard';
            return;
        }
        
        // Continuar con la navegación normal
        return originalNavigate(view, pushState);
    };
    
    console.log('Auth router configurado');
}

// Forzar logout al cargar si no hay sesión válida
function forceLoginCheck() {
    // Si NO hay sesión de usuario válida,-ir a login
    if (!Auth.isAuthenticated()) {
        console.log('No hay sesión válida, forzando login...');
        window.location.hash = 'login';
        return true;
    }
    return false;
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Limpiar token viejo del CMS
    localStorage.removeItem('CMS_ADMIN_TOKEN');
    
    // Configurar el router modificado
    setupAuthRouter();
    
    // Pequeño delay para verificar autenticación
    setTimeout(() => {
        updateUserUI();
        
        // FORZAR login si no hay sesión
        const currentHash = window.location.hash.replace('#', '');
        if (!Auth.isAuthenticated() && currentHash !== 'login') {
            console.log('Forzando redirección a login...');
            window.location.hash = 'login';
        }
    }, 300);
});

// Hacer funciones globales
window.updateUserUI = updateUserUI;
