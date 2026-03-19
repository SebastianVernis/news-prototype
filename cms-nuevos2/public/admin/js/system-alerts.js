/**
 * Sistema de Alertas para NexoPress CMS
 * Usa notificaciones toast no invasivas
 */

async function checkSystemCriticalAlerts() {
    console.log("[Alerts] Verificando estado del sistema...");
    const errors = [];

    try {
        // 1. Verificar Crons
        const cronData = await apiFetch("/cron/status");
        if (cronData && cronData.tasks) {
            for (const [task, status] of Object.entries(cronData.tasks)) {
                if (task.startsWith('fb_') && status.includes('Error')) {
                    errors.push({ task, status });
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
            // Ignorar si no está disponible
        }

        // Mostrar notificación solo si hay errores reales
        if (errors.length > 0) {
            showCriticalErrorToast(errors);
        }
    } catch (e) {
        console.error("[Alerts] Error al verificar estado:", e);
    }
}

/**
 * Muestra toast de error crítico
 */
function showCriticalErrorToast(errors) {
    const errorMessages = errors.map(e => {
        if (e.task) {
            return `${e.task.replace(/_/g, ' ')}: ${e.status}`;
        }
        return e.message;
    }).join('; ');
    
    showErrorToast(
        'Errores en Autopublicación',
        `Se detectaron ${errors.length} error(es). Revisa el Monitor.`,
        6000
    );
}

/**
 * Muestra notificación de error genérica (reemplaza al modal)
 */
function showErrorPopup(title, message) {
    showErrorToast(title, message, 5000);
}
