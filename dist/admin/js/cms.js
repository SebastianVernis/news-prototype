// Controlador CMS - Flujo de Publicación Dinámico
async function initCMS() {
    await loadCMSArticles();
    await loadCMSCategories();
}

async function loadCMSCategories() {
    try {
        const categories = await apiFetch('/categories');
        const select = document.getElementById('cms-categoria');
        if (select) {
            select.innerHTML = categories.map(c => `<option value="${c.NOMBRE}">${c.NOMBRE}</option>`).join('');
        }
    } catch (e) { console.error('Error cargando categorías:', e); }
}

async function loadCMSArticles() {
    const tbody = document.getElementById('cms-articles-table');
    if (!tbody) return;
    try {
        const articles = await apiFetch('/cms/articles');
        tbody.innerHTML = articles.map(a => `
            <tr>
                <td>${a.TITULO}</td>
                <td>${a.CATEGORIA}</td>
                <td><span class="status-badge status-normal">${a.ESTADO}</span></td>
                <td>${new Date(a.FECHA_CREACION).toLocaleDateString()}</td>
                <td class="actions">
                    <button class="btn btn-outline" onclick="editCMSArticle('${a.ID}')"><i class="fas fa-edit"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (e) { console.error('Error cargando artículos CMS:', e); }
}

async function editCMSArticle(id) {
    try {
        const articles = await apiFetch('/cms/articles');
        const art = articles.find(a => a.ID === id);
        if (!art) return;

        document.getElementById('cms-list-view').style.display = 'none';
        document.getElementById('cms-editor-view').style.display = 'block';
        
        document.getElementById('cms-article-id').value = art.ID;
        document.getElementById('cms-titulo').value = art.TITULO;
        document.getElementById('cms-categoria').value = art.CATEGORIA;
        document.getElementById('cms-contenido').value = art.CONTENIDO;
        document.getElementById('cms-descripcion').value = art.DESCRIPCION || '';
        document.getElementById('cms-imagen').value = art.URL_IMAGEN || '';
        document.getElementById('cms-destacado').checked = art.DESTACADO === 1;
        
        document.getElementById('cms-editor-title').textContent = 'Editando Borrador';
    } catch (e) { alert('Error: ' + e.message); }
}

function showNewCMSArticle() {
    document.getElementById('cms-list-view').style.display = 'none';
    document.getElementById('cms-editor-view').style.display = 'block';
    document.getElementById('cms-form-element').reset();
    document.getElementById('cms-article-id').value = '';
    document.getElementById('cms-editor-title').textContent = 'Nuevo Artículo';
}

async function saveCMSArticle() {
    const btn = document.querySelector('button[onclick="saveCMSArticle()"]');
    if (btn) btn.disabled = true;

    try {
        const payload = {
            id: document.getElementById('cms-article-id').value || null,
            titulo: document.getElementById('cms-titulo').value,
            contenido: document.getElementById('cms-contenido').value,
            descripcion: document.getElementById('cms-descripcion').value,
            categoria: document.getElementById('cms-categoria').value,
            url_imagen: document.getElementById('cms-imagen').value,
            destacado: document.getElementById('cms-destacado').checked ? 1 : 0,
            estado: 'BORRADOR'
        };
        const res = await apiFetch('/cms/articles', { method: 'POST', body: JSON.stringify(payload) });
        if (res.success) {
            document.getElementById('cms-article-id').value = res.id;
            alert('Borrador guardado.');
            return res.id;
        }
    } catch (e) { alert('Error al guardar: ' + e.message); }
    finally { if (btn) btn.disabled = false; }
}

// Lógica del Modal de Publicación
async function openPublishModal() {
    const titulo = document.getElementById('cms-titulo').value;
    if (!titulo) return alert('Ingresa un título antes de publicar.');

    // Cargar sitios para los checkboxes
    try {
        const sites = await apiFetch('/sites');
        const container = document.getElementById('publish-sites-checkboxes');
        container.innerHTML = sites.map(s => `
            <div style="margin-bottom:5px;">
                <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
                    <input type="checkbox" class="publish-site-check" value="${s.SLUG}">
                    <span>${s.NOMBRE} (${s.DOMINIO})</span>
                </label>
            </div>
        `).join('');
        
        document.getElementById('cms-publish-modal').style.display = 'flex';
    } catch (e) { alert('Error cargando sitios: ' + e.message); }
}

function closePublishModal() {
    document.getElementById('cms-publish-modal').style.display = 'none';
}

// ACCIÓN A: Parafrasear y enviar a revisión
async function actionParaphraseAndReview() {
    const selectedSites = Array.from(document.querySelectorAll('.publish-site-check:checked')).map(cb => cb.value);
    if (selectedSites.length === 0) return alert('Selecciona al menos un sitio para generar las variaciones.');

    if (!confirm(`¿Deseas generar variaciones parafraseadas para los ${selectedSites.length} sitios seleccionados y enviarlas a la Mesa de Revisión?`)) return;
    
    try {
        const btn = document.querySelector('button[onclick="actionParaphraseAndReview()"]');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando...';

        // 1. Guardar primero
        const articleId = await saveCMSArticle();
        if (!articleId) return;

        // 2. Llamar al generador de variaciones
        await apiFetch('/cms/generate-variations', {
            method: 'POST',
            body: JSON.stringify({
                id: articleId,
                sitios: selectedSites
            })
        });

        alert('¡Variaciones generadas! Ya puedes revisarlas en la Mesa de Revisión.');
        closePublishModal();
        exitCMSEditor();
    } catch (e) { 
        alert('Error: ' + e.message); 
    } finally {
        const btn = document.querySelector('button[onclick="actionParaphraseAndReview()"]');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-magic"></i> Parafrasear y Revisar';
        }
    }
}

// ACCIÓN B: Publicar directamente sin parafrasear (En tabla ARTICULOS_CMS)
async function actionPublishDirectly() {
    const selectedSites = Array.from(document.querySelectorAll('.publish-site-check:checked')).map(cb => cb.value);
    if (selectedSites.length === 0) return alert('Selecciona al menos un sitio.');

    if (!confirm(`¿Estás seguro de publicar este contenido en ${selectedSites.length} sitios? Se marcará como PUBLICADO en la base de datos central.`)) return;

    try {
        const btn = document.querySelector('button[onclick="actionPublishDirectly()"]');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publicando...';

        // 1. Guardar primero el borrador por si hubo cambios de último segundo
        const articleId = await saveCMSArticle();
        if (!articleId) return;

        // 2. Ejecutar publicación en tabla ARTICULOS_CMS
        await apiFetch('/cms/publish', {
            method: 'POST',
            body: JSON.stringify({
                id: articleId,
                sitios: selectedSites
            })
        });

        alert('¡Artículo publicado con éxito en los sitios seleccionados!');
        closePublishModal();
        exitCMSEditor();
    } catch (e) { 
        alert('Error en publicación: ' + e.message); 
    } finally {
        const btn = document.querySelector('button[onclick="actionPublishDirectly()"]');
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Publicar en Sitios Seleccionados';
        }
    }
}

function exitCMSEditor() {
    document.getElementById('cms-list-view').style.display = 'block';
    document.getElementById('cms-editor-view').style.display = 'none';
    loadCMSArticles();
}
