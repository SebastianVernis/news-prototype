/* ========================================
   Reporte Central MX - Admin Login Script
   ======================================== */

const TOKEN_KEY = 'cms_token_reportecentralmx';
const SESSION_KEY = 'cms_session_reportecentralmx';

document.addEventListener('DOMContentLoaded', () => {
    // Check if already logged in
    const session = sessionStorage.getItem(SESSION_KEY);
    if (session) {
        window.location.href = 'index.html';
        return;
    }

    setupLoginForm();
});

function setupLoginForm() {
    const form = document.getElementById('login-form');
    const tokenInput = document.getElementById('token');
    const toggleBtn = document.getElementById('toggle-token');

    // Toggle password visibility
    toggleBtn?.addEventListener('click', () => {
        const type = tokenInput.type === 'password' ? 'text' : 'password';
        tokenInput.type = type;
        toggleBtn.innerHTML = type === 'password' 
            ? '<i class="fas fa-eye"></i>' 
            : '<i class="fas fa-eye-slash"></i>';
    });

    // Form submission
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const token = tokenInput.value.trim();
        
        // Validate token format (64 hex characters)
        if (!/^[a-fA-F0-9]{64}$/.test(token)) {
            showToast('El token debe ser de 64 caracteres hexadecimales', 'error');
            return;
        }

        try {
            // Store token and session
            sessionStorage.setItem(TOKEN_KEY, token);
            sessionStorage.setItem(SESSION_KEY, JSON.stringify({
                loggedIn: true,
                timestamp: Date.now(),
                token: token
            }));

            showToast('Autenticación exitosa', 'success');
            
            // Redirect to admin panel
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
        } catch (error) {
            console.error('Login error:', error);
            showToast('Error de autenticación', 'error');
        }
    });
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show ' + type;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Generate a sample token for testing (remove in production)
function generateSampleToken() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, b => b.toString(16).padStart(2, '0')).join('');
}

// Console helper for generating tokens
console.log('Para generar un token de prueba, ejecute: generateSampleToken()');
