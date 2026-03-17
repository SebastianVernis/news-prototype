// Controlador Mesa de Revisión - Versión Interactiva Corregida
let currentRevisionList = [];

async function initRevision() {
    await loadRevisionTable();
}

async function loadRevisionTable() {
    const tbody = document.getElementById('revision-pending-table');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="5">Consultando mesa de redacción...</td></tr>';
    try {
        currentRevisionList = await apiFetch('/revision/pending');
        if (!Array.isArray(currentRevisionList) || currentRevisionList.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:2rem;">No hay artículos pendientes de revisión.</td></tr>';
            return;
        }

        tbody.innerHTML = currentRevisionList.map(rev => `
            <tr>
                <td>${rev.TITULO_PROPUESTO || 'Sin título'}</td>
                <td><span class="status-badge status-normal">${rev.SITIO_DESTINO || 'General'}</span></td>
                <td>${rev.CATEGORIA || 'Nacional'}</td>
                <td>${rev.FECHA_CREACION ? new Date(rev.FECHA_CREACION).toLocaleDateString() : 'Hoy'}</td>
                <td class="actions">
                    <button class="btn btn-outline" title="Ver y Editar" onclick="openRevisionEditor('${rev.ID}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-primary" title="Aprobar Rápido" onclick="approveRevision('${rev.ID}')">
                        <i class="fas fa-check"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5">Error: ${e.message}</td></tr>`;
    }
}

function openRevisionEditor(id) {
    // Buscar por ID (string o int)
    const rev = currentRevisionList.find(r => String(r.ID) === String(id));
    if (!rev) return alert('No se encontró el artículo en la lista local.');

    document.getElementById('rev-id').value = rev.ID;
    document.getElementById('rev-titulo').value = rev.TITULO_PROPUESTO || '';
    document.getElementById('rev-descripcion').value = rev.DESCRIPCION_PROPUESTA || '';
    document.getElementById('rev-contenido').value = rev.CONTENIDO_PROPUESTO || '';
    
    document.getElementById('rev-modal-title').textContent = 'Revisando para: ' + (rev.SITIO_DESTINO || 'Sitio');
    document.getElementById('revision-edit-modal').style.display = 'flex';
}

function closeRevisionModal() {
    document.getElementById('revision-edit-modal').style.display = 'none';
}

async function saveRevisionChanges() {
    const id = document.getElementById('rev-id').value;
    const payload = {
        titulo: document.getElementById('rev-titulo').value,
        descripcion: document.getElementById('rev-descripcion').value,
        contenido: document.getElementById('rev-contenido').value
    };

    try {
        await apiFetch(`/revision/${id}`, {
            method: 'PUT',
            body: JSON.stringify(payload)
        });
        alert('Cambios guardados exitosamente.');
        await loadRevisionTable();
        closeRevisionModal();
    } catch (e) { alert('Error al guardar cambios: ' + e.message); }
}

async function approveFromModal() {
    const id = document.getElementById('rev-id').value;
    // Guardar cambios antes de aprobar para no perder ediciones
    const payload = {
        titulo: document.getElementById('rev-titulo').value,
        descripcion: document.getElementById('rev-descripcion').value,
        contenido: document.getElementById('rev-contenido').value
    };
    
    try {
        await apiFetch(`/revision/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
        await approveRevision(id);
    } catch (e) { alert('Error: ' + e.message); }
}

async function approveRevision(id) {
    if(!confirm('¿Publicar definitivamente este artículo en el sitio destino?')) return;
    try {
        await apiFetch(`/revision/approve/${id}`, { method: 'POST' });
        alert('¡Artículo publicado con éxito!');
        closeRevisionModal();
        await loadRevisionTable();
    } catch (e) { alert('Error al aprobar: ' + e.message); }
}
