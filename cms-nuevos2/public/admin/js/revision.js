// Controlador Mesa de Revisión Simplificado (Usa Editor Universal)
let currentRevisionList = [];

async function initRevision() {
    const tbody = document.getElementById('revision-pending-table');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5">La revisión está deshabilitada.</td></tr>';
}

async function loadRevisionTable() {
    const tbody = document.getElementById('revision-pending-table');
    if (!tbody) return;
    try {
        currentRevisionList = await apiFetch('/revision/pending');
        if (currentRevisionList.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No hay artículos pendientes.</td></tr>';
            return;
        }
        tbody.innerHTML = currentRevisionList.map(rev => `
            <tr>
                <td>${rev.TITULO_PROPUESTO || 'Sin título'}</td>
                <td>${rev.SITIO_DESTINO || 'General'}</td>
                <td>${rev.CATEGORIA || 'Nacional'}</td>
                <td style="font-size:0.85rem; white-space:nowrap;">${rev.FECHA_CREACION ? new Date(rev.FECHA_CREACION).toLocaleString('es-MX', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                }) : '-'}</td>
                <td class="col-actions">
                    <div class="actions">
                        <button class="btn btn-primary" onclick="openRevisionEditorUnified('${rev.ID}')" title="Revisar">
                            <i class="fas fa-eye"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (e) { 
        console.error('Error cargando revisión:', e);
        tbody.innerHTML = '<tr><td colspan="5">Error cargando artículos. Recarga la página.</td></tr>';
    }
}

// Función global para abrir editor de revisión
window.openRevisionEditorUnified = function(id) {
    if (typeof showErrorToast === 'function') {
        showErrorToast('Deshabilitado', 'La revisión está deshabilitada. Usa Redacción Interna.', 3000);
    }
    return;

    console.log('Abriendo revisión para ID:', id);
    const rev = currentRevisionList.find(r => String(r.ID) === String(id));
    if (!rev) {
        console.error('No se encontró el artículo con ID:', id);
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error', 'No se encontró el artículo', 3000);
        }
        return;
    }

    console.log('Artículo encontrado:', rev.TITULO_PROPUESTO);

    // Verificar que openUniversalEditor esté disponible
    if (typeof openUniversalEditor !== 'function') {
        console.error('openUniversalEditor no está disponible');
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error', 'El editor no está cargado. Recarga la página.', 3000);
        }
        return;
    }

    openUniversalEditor('revision', {
        id: rev.ID,
        title: rev.TITULO_PROPUESTO,
        content: rev.CONTENIDO_PROPUESTO || '',
        excerpt: rev.DESCRIPCION_PROPUESTA || '',
        category: rev.CATEGORIA || 'NACIONAL',
        site: rev.SITIO_DESTINO || '',
        imageUrl: rev.URL_IMAGEN || ''
    });
};
