/**
 * Sistema de Notificaciones Toast para NexoPress CMS
 * Notificaciones no invasivas que desaparecen automáticamente
 */

// Contenedor de toasts
let toastContainer = null;

/**
 * Inicializa el contenedor de toasts
 */
function initToastSystem() {
    if (toastContainer) return;
    
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 400px;
        pointer-events: none;
    `;
    document.body.appendChild(toastContainer);
}

/**
 * Muestra una notificación toast
 * @param {string} title - Título de la notificación
 * @param {string} message - Mensaje detallado
 * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Duración en ms (default: 3000)
 */
function showToast(title, message, type = 'info', duration = 3000) {
    initToastSystem();
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    
    const colors = {
        success: { bg: '#10b981', border: '#059669', icon: '#ffffff' },
        error: { bg: '#ef4444', border: '#dc2626', icon: '#ffffff' },
        warning: { bg: '#f59e0b', border: '#d97706', icon: '#ffffff' },
        info: { bg: '#3b82f6', border: '#2563eb', icon: '#ffffff' }
    };
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        background: ${colors[type].bg};
        border-left: 4px solid ${colors[type].border};
        border-radius: 8px;
        padding: 1rem 1.25rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        color: white;
        min-width: 300px;
        max-width: 400px;
        pointer-events: auto;
        animation: slideInRight 0.3s ease-out;
        cursor: pointer;
        transition: all 0.3s;
    `;
    
    toast.innerHTML = `
        <style>
            @keyframes slideInRight {
                from { transform: translateX(400px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(400px); opacity: 0; }
            }
            .toast-close:hover { opacity: 0.8; }
        </style>
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <i class="fas ${icons[type]}" style="font-size: 1.25rem; margin-top: 2px; flex-shrink: 0;"></i>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 600;">${title}</h4>
                <p style="margin: 0; font-size: 0.85rem; opacity: 0.9; line-height: 1.4;">${message}</p>
            </div>
            <button class="toast-close" style="
                background: transparent;
                border: none;
                color: white;
                cursor: pointer;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0.7;
                transition: opacity 0.2s;
            ">
                <i class="fas fa-times" style="font-size: 0.9rem;"></i>
            </button>
        </div>
    `;
    
    // Click para cerrar
    toast.onclick = (e) => {
        if (!e.target.closest('.toast-close')) {
            dismissToast(toast);
        }
    };
    
    toast.querySelector('.toast-close').onclick = () => dismissToast(toast);
    
    toastContainer.appendChild(toast);
    
    // Auto-dismiss
    if (duration > 0) {
        setTimeout(() => dismissToast(toast), duration);
    }
    
    return toast;
}

/**
 * Descarta un toast con animación
 */
function dismissToast(toast) {
    toast.style.animation = 'slideOutRight 0.3s ease-out';
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
        // Limpiar contenedor si está vacío
        if (toastContainer && toastContainer.children.length === 0) {
            document.body.removeChild(toastContainer);
            toastContainer = null;
        }
    }, 300);
}

/**
 * Verifica el estado del sistema y muestra notificaciones discretas
 */
async function checkSystemCriticalAlerts() {
    console.log("[Alerts] Verificando estado del sistema...");
    const errors = [];
    const warnings = [];

    try {
        // 1. Verificar Crons
        const cronData = await apiFetch("/cron/status");
        if (cronData && cronData.tasks) {
            for (const [task, status] of Object.entries(cronData.tasks)) {
                if (task.startsWith('fb_') && status.includes('Error')) {
                    errors.push({ task, status });
                } else if (task.startsWith('fb_') && status.includes('pending')) {
                    // Solo warning si está pendiente por mucho tiempo
                    warnings.push({ task, status });
                }
            }
        }

        // 2. Verificar Tokens de Facebook
        try {
            const tokens = await apiFetch("/facebook/debug-tokens");
            if (tokens && Array.isArray(tokens)) {
                const invalidTokens = tokens.filter(t => !t.is_valid);
                if (invalidTokens.length > 0) {
                    errors.push({ 
                        type: 'tokens', 
                        message: `Tokens inválidos: ${invalidTokens.map(t => t.slug).join(", ")}` 
                    });
                }
            }
        } catch (e) {
            // Ignorar error de debug-tokens si no está disponible
        }

        // Mostrar notificaciones solo si hay errores reales
        if (errors.length > 0) {
            // Mostrar toast de error en el monitor
            const errorMessages = errors.map(e => {
                if (e.task) {
                    return `${e.task.replace(/_/g, ' ')}: ${e.status}`;
                }
                return e.message;
            }).join('; ');
            
            showToast(
                'Errores en Autopublicación',
                `Se detectaron ${errors.length} error(es). Revisa el Monitor para más detalles.`,
                'error',
                5000
            );
        }
    } catch (e) {
        console.error("[Alerts] Error al verificar estado:", e);
        // No mostrar alerta si falla la verificación (podría ser temporal)
    }
}

/**
 * Muestra notificación de éxito
 */
function showSuccessToast(title, message, duration = 3000) {
    return showToast(title, message, 'success', duration);
}

/**
 * Muestra notificación de error
 */
function showErrorToast(title, message, duration = 5000) {
    return showToast(title, message, 'error', duration);
}

/**
 * Muestra notificación de advertencia
 */
function showWarningToast(title, message, duration = 4000) {
    return showToast(title, message, 'warning', duration);
}

/**
 * Muestra notificación de información
 */
function showInfoToast(title, message, duration = 3000) {
    return showToast(title, message, 'info', duration);
}

// Inicializar al cargar
document.addEventListener('DOMContentLoaded', initToastSystem);
