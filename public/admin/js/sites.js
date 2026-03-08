// Controlador de Gestión de Sitios (Simplificado)

async function initSites() {
    await loadSitesTable();
    const form = document.getElementById('site-form-element');
    if (form) form.onsubmit = handleSiteSubmit;
}

async function loadSitesTable() {
    const tbody = document.getElementById('sites-table');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="4">Cargando sitios...</td></tr>';
    try {
        const sites = await apiFetch('/sites');
        if (!Array.isArray(sites)) throw new Error('La API no devolvió una lista de sitios.');

        tbody.innerHTML = sites.map(s => `
            <tr>
                <td>${s.NOMBRE}</td>
                <td>${s.DOMINIO}</td>
                <td><span class="status-badge ${s.ACTIVO ? 'status-featured' : 'status-normal'}">${s.ACTIVO ? 'Activo' : 'Inactivo'}</span></td>
                <td class="col-actions">
                    <div class="actions">
                        <button class="btn btn-outline" onclick="editSiteById('${s.ID}')" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4">Error: ${e.message}</td></tr>`;
    }
}

function showNewSite() {
    const listView = document.getElementById('sites-list-view');
    const editorView = document.getElementById('site-editor-view');
    if (listView && editorView) {
        listView.style.display = 'none';
        editorView.style.display = 'block';
    }
    const form = document.getElementById('site-form-element');
    if (form) form.reset();
    document.getElementById('site-id').value = '';
    document.getElementById('site-form-title').textContent = 'Nuevo Sitio';
}

async function editSiteById(id) {
    try {
        const sites = await apiFetch('/sites');
        const site = sites.find(s => s.ID === id);
        if (!site) return;

        showNewSite();
        document.getElementById('site-form-title').textContent = 'Editar: ' + site.NOMBRE;
        document.getElementById('site-id').value = site.ID;
        document.getElementById('site-nombre').value = site.NOMBRE;
        document.getElementById('site-dominio').value = site.DOMINIO;
        document.getElementById('site-tagline').value = site.TAGLINE || '';
        document.getElementById('site-activo').checked = site.ACTIVO == 1;
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error', e.message, 5000);
        }
    }
}

function exitSiteEditor() {
    document.getElementById('sites-list-view').style.display = 'block';
    document.getElementById('site-editor-view').style.display = 'none';
    loadSitesTable();
}

async function handleSiteSubmit(e) {
    e.preventDefault();
    const siteId = document.getElementById('site-id').value || crypto.randomUUID();
    const btn = e.target.querySelector('button[type="submit"]');
    btn.disabled = true;

    try {
        const sitePayload = {
            id: siteId,
            nombre: document.getElementById('site-nombre').value,
            dominio: document.getElementById('site-dominio').value,
            tagline: document.getElementById('site-tagline').value,
            activo: document.getElementById('site-activo').checked
        };

        await apiFetch('/sites', { method: 'POST', body: JSON.stringify(sitePayload) });
        if (typeof showSuccessToast === 'function') {
            showSuccessToast('Guardado', 'El sitio se guardó correctamente', 3000);
        }
        exitSiteEditor();
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error', e.message, 5000);
        }
    } finally {
        btn.disabled = false;
    }
}
