// Controlador de Gestión de Sitios
let designCatalogs = { colors: [], styles: [], elements: [] };

async function initSites() {
    await loadDesignCatalogs();
    await loadSitesTable();
    const form = document.getElementById('site-form-element');
    if (form) form.onsubmit = handleSiteSubmit;
}

async function loadDesignCatalogs() {
    try {
        const data = await apiFetch('/catalogs/design');
        designCatalogs = {
            colors: Array.isArray(data.colors) ? data.colors : [],
            styles: Array.isArray(data.styles) ? data.styles : [],
            elements: Array.isArray(data.elements) ? data.elements : []
        };
        
        const fillSelect = (id, items, filterType = null) => {
            const el = document.getElementById(id);
            if (!el) return;
            let options = '<option value="">Seleccionar...</option>';
            const filtered = items.filter(i => !filterType || i.TIPO === filterType);
            options += filtered.map(i => `<option value="${i.ID}">${i.NOMBRE}</option>`).join('');
            el.innerHTML = options;
        };

        fillSelect('site-paleta', designCatalogs.colors);
        fillSelect('site-estilo', designCatalogs.styles);
        fillSelect('site-header', designCatalogs.elements, 'HEADER');
        fillSelect('site-footer', designCatalogs.elements, 'FOOTER');
        fillSelect('site-layout', designCatalogs.elements, 'LAYOUT');
        fillSelect('site-preloader', designCatalogs.elements, 'PRELOADER');
        fillSelect('site-carrusel', designCatalogs.elements, 'CAROUSEL');
        fillSelect('site-grid', designCatalogs.elements, 'GRID');
    } catch (e) {
        console.error('Error catálogos:', e);
    }
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
                <td class="actions">
                    <button class="btn btn-outline" onclick="editSiteById('${s.ID}')">
                        <i class="fas fa-edit"></i>
                    </button>
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
    switchSiteTab('basic');
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

        // Cargar datos extendidos
        const [dist, legals, channels, menus] = await Promise.all([
            apiFetch(`/sites/distribution/${id}`).catch(() => ({})),
            apiFetch(`/sites/legals/${id}`).catch(() => ({})),
            apiFetch(`/sites/channels/${id}`).catch(() => ([])),
            apiFetch(`/sites/menus/${id}`).catch(() => ([]))
        ]);

        if (dist.ID_SITIO) {
            document.getElementById('site-paleta').value = dist.ID_PALETA_COLORES || '';
            document.getElementById('site-estilo').value = dist.ID_ESTILO_GENERAL || '';
            document.getElementById('site-header').value = dist.ID_HEADER || '';
            document.getElementById('site-footer').value = dist.ID_FOOTER || '';
            document.getElementById('site-layout').value = dist.ID_LAYOUT_MAESTRO || '';
            document.getElementById('site-preloader').value = dist.ID_PRELOADER || '';
            document.getElementById('site-carrusel').value = dist.ID_CARRUSEL || '';
            document.getElementById('site-grid').value = dist.ID_GRID_NOTICIAS || '';
        }

        const chanContainer = document.getElementById('channels-container');
        if (chanContainer) {
            chanContainer.innerHTML = '';
            if (Array.isArray(channels)) channels.forEach(ch => addChannelRow(ch));
        }

        const menuContainer = document.getElementById('menus-container');
        if (menuContainer) {
            menuContainer.innerHTML = '';
            if (Array.isArray(menus)) menus.forEach(m => addMenuRow(m));
        }

    } catch (e) {
        alert('Error: ' + e.message);
    }
}

function switchSiteTab(tab) {
    ['basic', 'legals', 'channels', 'menus'].forEach(t => {
        const content = document.getElementById(`site-tab-${t}-content`);
        const btn = document.getElementById(`tab-site-${t}`);
        if (content) content.style.display = t === tab ? 'block' : 'none';
        if (btn) btn.classList.toggle('active', t === tab);
    });
}

function exitSiteEditor() {
    document.getElementById('sites-list-view').style.display = 'block';
    document.getElementById('site-editor-view').style.display = 'none';
    loadSitesTable();
}

function addChannelRow(d = {}) {
    const container = document.getElementById('channels-container');
    if (!container) return;
    const row = document.createElement('div');
    row.className = 'channel-row';
    row.style = 'display:grid; grid-template-columns: 1fr 2fr 1.5fr 40px; gap:10px; margin-bottom:10px; align-items:end;';
    const types = ['X', 'FACEBOOK', 'INSTAGRAM', 'WHATSAPP', 'YOUTUBE'];
    row.innerHTML = `
        <select class="form-control channel-tipo">${types.map(t => `<option value="${t}" ${d.TIPO===t?'selected':''}>${t}</option>`).join('')}</select>
        <input type="text" class="form-control channel-url" value="${d.URL||''}" placeholder="URL">
        <input type="text" class="form-control channel-icono" value="${d.ICONO_CLASE||''}" placeholder="Icono fa-...">
        <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(row);
}

function addMenuRow(d = {}) {
    const container = document.getElementById('menus-container');
    if (!container) return;
    const row = document.createElement('div');
    row.className = 'menu-row';
    row.style = 'display:grid; grid-template-columns: 1.5fr 2fr 1fr 40px; gap:10px; margin-bottom:10px; align-items:end;';
    const pos = ['HEADER', 'FOOTER', 'SIDEBAR'];
    row.innerHTML = `
        <input type="text" class="form-control menu-etiqueta" value="${d.ETIQUETA||''}" placeholder="Etiqueta">
        <input type="text" class="form-control menu-url" value="${d.URL||''}" placeholder="/slug">
        <select class="form-control menu-posicion">${pos.map(p => `<option value="${p}" ${d.POSICION===p?'selected':''}>${p}</option>`).join('')}</select>
        <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(row);
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
        alert('¡Guardado!');
        exitSiteEditor();
    } catch (e) { alert(e.message); }
    finally { btn.disabled = false; }
}

function openSitePreview() {
    const modal = document.getElementById('site-preview-modal');
    const iframe = document.getElementById('site-preview-iframe');
    if (!modal || !iframe) return;
    modal.style.display = 'flex';
    const doc = iframe.contentWindow.document;
    doc.open(); doc.write(`<h1>Previsualizando ${document.getElementById('site-nombre').value}</h1>`); doc.close();
}

function closeSitePreview() { document.getElementById('site-preview-modal').style.display = 'none'; }
function setPreviewSize(s) { document.getElementById('site-preview-iframe').style.width = s === 'mobile' ? '375px' : '100%'; }
