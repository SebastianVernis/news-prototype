// Controlador Monitor Facebook Unificado
async function initFacebook() {
    await loadFBMonitor();
}

async function loadFBMonitor() {
    const tbody = document.getElementById('fb-monitor-table');
    if (!tbody) return;

    try {
        // Consultar la cola unificada (CMS + Auto)
        const fbArticles = await apiFetch('/facebook/monitor');

        if (fbArticles.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:2rem;">No hay registros de envío a Facebook.</td></tr>';
            return;
        }

        tbody.innerHTML = fbArticles.map(a => `
            <tr>
                <td>
                    <small style="color:#666; display:block;">[${a.TIPO}]</small>
                    <strong>${a.TITULO}</strong>
                </td>
                <td style="font-size:0.8rem; max-width:200px; overflow:hidden; text-overflow:ellipsis;">${a.SITIOS_DESTINO || '-'}</td>
                <td>
                    ${a.FB_PUBLICADO === 1 
                        ? '<span class="status-badge" style="background:#d4edda; color:#155724;">Publicado</span>' 
                        : '<span class="status-badge" style="background:#fff3cd; color:#856404;">Pendiente / Error</span>'}
                </td>
                <td>${a.FB_FECHA ? new Date(a.FB_FECHA).toLocaleString() : 'En proceso...'}</td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4">Error: ${e.message}</td></tr>`;
    }
}
