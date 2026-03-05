/**
 * Sistema de Alertas Críticas para NexoPress CMS
 * Detecta fallos en la autopublicación y notifica al usuario inmediatamente.
 */

async function checkSystemCriticalAlerts() {
    console.log("[Alerts] Verificando estado del sistema...");
    const errors = [];

    try {
        // 1. Verificar Crons
        const cronData = await apiFetch("/cron/status");
        if (cronData && cronData.tasks) {
            for (const [task, status] of Object.entries(cronData.tasks)) {
                if (!status.includes("OK")) {
                    errors.push(`Cron Fallido: ${task.replace(/_/g, " ")} (${status})`);
                }
            }
        }

        // 2. Verificar Tokens de Facebook
        const tokens = await apiFetch("/facebook/debug-tokens");
        if (tokens && Array.isArray(tokens)) {
            const invalidTokens = tokens.filter(t => !t.is_valid);
            if (invalidTokens.length > 0) {
                errors.push(`Tokens de Meta Inválidos: ${invalidTokens.map(t => t.slug).join(", ")}`);
            }
        }

        if (errors.length > 0) {
            showCriticalErrorModal(errors);
        }
    } catch (e) {
        console.error("[Alerts] Error al verificar estado:", e);
        // Si falla la API de monitoreo, también es una alerta
        // Pero evitamos ser intrusivos si es solo un error de red temporal
    }
}

/**
 * Muestra un modal altamente visible con los errores detectados.
 */
function showCriticalErrorModal(errors) {
    // Evitar duplicados
    if (document.getElementById('critical-error-modal')) return;

    const modal = document.createElement('div');
    modal.id = 'critical-error-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.85);
        z-index: 10001;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
    `;

    const errorItems = errors.map(err => `
        <li style="margin-bottom: 0.8rem; color: #ffeb3b; display: flex; align-items: flex-start; gap: 10px;">
            <i class="fas fa-exclamation-triangle" style="margin-top: 3px;"></i>
            <span>${err}</span>
        </li>
    `).join("");

    modal.innerHTML = `
        <div style="
            background: #1e1e2e;
            color: white;
            padding: 2.5rem;
            border-radius: 16px;
            width: 90%;
            max-width: 550px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 2px solid #ff5252;
            animation: modalShake 0.5s ease-in-out;
        ">
            <style>
                @keyframes modalShake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-10px); }
                    75% { transform: translateX(10px); }
                }
            </style>
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <i class="fas fa-exclamation-circle" style="font-size: 4rem; color: #ff5252; margin-bottom: 1rem;"></i>
                <h2 style="margin: 0; color: #ff5252; font-size: 1.8rem; letter-spacing: 1px;">SISTEMA CAÍDO</h2>
                <p style="color: #a9b1d6; margin-top: 0.5rem;">Se han detectado fallos críticos en la autopublicación.</p>
            </div>
            
            <div style="
                background: rgba(255, 82, 82, 0.1);
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                border-left: 4px solid #ff5252;
            ">
                <h4 style="margin: 0 0 1rem 0; font-size: 1rem; text-transform: uppercase; color: #ff8a80;">Detalles del error:</h4>
                <ul style="margin: 0; padding: 0; list-style: none; font-size: 0.95rem;">
                    ${errorItems}
                </ul>
            </div>

            <div style="display: flex; gap: 1rem;">
                <button id="btn-fix-now" style="
                    flex: 1;
                    padding: 1rem;
                    background: #ff5252;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.2s;
                    text-transform: uppercase;
                " onmouseover="this.style.background='#ff1744'" onmouseout="this.style.background='#ff5252'">
                    <i class="fas fa-tools"></i> Ir al Monitor
                </button>
                <button id="btn-ignore-error" style="
                    padding: 1rem;
                    background: transparent;
                    color: #a9b1d6;
                    border: 1px solid #444;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.2s;
                " onmouseover="this.style.borderColor='#666'" onmouseout="this.style.borderColor='#444'">
                    Cerrar
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('btn-fix-now').onclick = () => {
        modal.remove();
        goToView('monitor');
    };

    document.getElementById('btn-ignore-error').onclick = () => {
        modal.remove();
    };
}

/**
 * Muestra un popup de error genérico con estilo NexoPress.
 */
function showErrorPopup(title, message) {
    if (document.getElementById('generic-error-modal')) {
        document.getElementById('generic-error-modal').remove();
    }

    const modal = document.createElement('div');
    modal.id = 'generic-error-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75);
        z-index: 10002;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(3px);
    `;

    modal.innerHTML = `
        <div style="
            background: #ffffff;
            color: #1a202c;
            padding: 2rem;
            border-radius: 12px;
            width: 90%;
            max-width: 450px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            text-align: center;
            border-top: 5px solid #ff5252;
        ">
            <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #ff5252; margin-bottom: 1rem;"></i>
            <h3 style="margin: 0 0 10px 0; font-size: 1.5rem; color: #2d3748;">${title}</h3>
            <p style="color: #4a5568; margin-bottom: 1.5rem; font-size: 1rem; line-height: 1.5;">${message}</p>
            <button id="btn-close-error" style="
                width: 100%;
                padding: 0.85rem;
                background: #2d3748;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            " onmouseover="this.style.background='#1a202c'" onmouseout="this.style.background='#2d3748'">
                Entendido
            </button>
        </div>
    `;

    document.body.appendChild(modal);
    document.getElementById('btn-close-error').onclick = () => modal.remove();
}
