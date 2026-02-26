// LÓGICA DEL EDITOR UNIVERSAL (CENTRALIZADA)

// Toggle Seleccionar todos los sitios
function toggleAllSites() {
    const checkboxes = document.querySelectorAll('.uni-site-checkbox');
    if (checkboxes.length === 0) return;
    
    // Verificar si todos están seleccionados
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    
    // Marcar/desmarcar todos
    checkboxes.forEach(cb => {
        cb.checked = !allChecked;
    });
    
    // Actualizar el texto del botón
    const btn = document.querySelector('[onclick="toggleAllSites()"]');
    if (btn) {
        btn.innerHTML = allChecked 
            ? '<i class="fas fa-check-square"></i> Seleccionar todos' 
            : '<i class="fas fa-square"></i> Deseleccionar todos';
    }
}

async function openUniversalEditor(mode, data = {}) {
    const editor = document.getElementById('universal-editor-view');
    const titleEl = document.getElementById('universal-editor-title');
    const actionsContainer = document.getElementById('uni-actions-container');
    const fbSection = document.getElementById('uni-fb-section');
    const sitesContainer = document.getElementById('uni-sites-container');
    
    // Limpiar formulario
    document.getElementById('universal-article-form').reset();
    document.getElementById('uni-image-preview').style.display = 'none';
    document.getElementById('uni-preview-img').src = '';
    
    // Setear Modo
    document.getElementById('uni-mode').value = mode;
    document.getElementById('uni-id').value = data.id || '';
    
    // Llenar campos con data disponible
    document.getElementById('uni-title').value = data.title || '';
    document.getElementById('uni-slug').value = data.slug || '';
    document.getElementById('uni-author').value = data.author || '';
    document.getElementById('uni-excerpt').value = data.excerpt || '';
    document.getElementById('uni-image').value = data.imageUrl || '';
    document.getElementById('uni-category').value = (data.category || 'POLITICA').toUpperCase();
    document.getElementById('uni-featured').value = data.featured ? '1' : '0';
    document.getElementById('uni-content').value = data.content || '';

    if (data.imageUrl) {
        let fullImageUrl = data.imageUrl;
        // Normalizar URLs antiguas /api/images/
        if (data.imageUrl.startsWith('/api/images/')) {
            const key = data.imageUrl.replace('/api/images/', '');
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                fullImageUrl = `${API_CONFIG.r2DevUrl}/${key}`;
            } else {
                fullImageUrl = `${API_CONFIG.r2PublicUrl}/${key}`;
            }
        }
        document.getElementById('uni-preview-img').src = fullImageUrl;
        document.getElementById('uni-image-preview').style.display = 'block';
    }

    // Cargar Sitios dinámicamente
    try {
        const sites = await apiFetch('/sites');
        const currentSites = data.site ? (Array.isArray(data.site) ? data.site : data.site.split(',').map(s => s.trim())) : [];

        sitesContainer.innerHTML = sites.map(s => `
            <div style="margin-bottom:2px;">
                <label style="display:flex; align-items:center; gap:6px; cursor:pointer; font-size:0.85rem;">
                    <input type="checkbox" class="uni-site-checkbox" value="${s.SLUG}" ${currentSites.includes(s.SLUG) ? 'checked' : ''}>
                    ${s.NOMBRE}
                </label>
            </div>
        `).join('');
        
        // Actualizar estado del botón "Seleccionar todos"
        const allChecked = sites.length > 0 && currentSites.length === sites.length;
        const btn = document.querySelector('[onclick="toggleAllSites()"]');
        if (btn) {
            btn.innerHTML = allChecked 
                ? '<i class="fas fa-square"></i> Deseleccionar todos' 
                : '<i class="fas fa-check-square"></i> Seleccionar todos';
        }
    } catch (e) { sitesContainer.innerHTML = 'Error cargando sitios'; }

    // Configurar UI según modo
    const fbPlaceholder = document.getElementById('uni-fb-placeholder');
    
    if (fbSection && fbPlaceholder) {
        fbSection.style.display = 'none';
        fbPlaceholder.style.display = 'none';
    }

    actionsContainer.innerHTML = '';

    if (mode === 'cms') {
        titleEl.textContent = data.id ? 'Editando Borrador (CMS)' : 'Nuevo Borrador (CMS)';
        if (fbSection) fbSection.style.display = 'block';
        actionsContainer.innerHTML = `
            <button type="button" class="btn btn-outline" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="saveUniversal('draft')">
                <i class="fas fa-save"></i> Guardar Borrador
            </button>
            <button type="button" class="btn btn-primary" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="saveUniversal('publish')">
                <i class="fas fa-paper-plane"></i> Publicar Ahora
            </button>
        `;
    }
    else if (mode === 'revision') {
        titleEl.textContent = 'Mesa de Revisión';
        actionsContainer.innerHTML = `
            <button type="button" class="btn btn-outline" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="saveUniversal('revision_save')">
                <i class="fas fa-save"></i> Guardar Cambios
            </button>
            <button type="button" class="btn btn-primary" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="saveUniversal('revision_approve')">
                <i class="fas fa-check-circle"></i> Aprobar y Publicar
            </button>
        `;
    }
    else {
        // Modo 'live' (Artículos ya publicados)
        titleEl.textContent = 'Editar Artículo Publicado';
        if (fbPlaceholder) fbPlaceholder.style.display = 'block';
        actionsContainer.innerHTML = `
            <button type="button" class="btn btn-primary" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="saveUniversal('live_update')">
                <i class="fas fa-save"></i> Actualizar Artículo
            </button>
            <button type="button" class="btn btn-danger" style="flex:1; padding:1rem 1.5rem; font-size:1rem; border-radius:8px;" onclick="deleteArticleFromEditor()">
                <i class="fas fa-trash"></i> Eliminar
            </button>
        `;
    }

    editor.style.display = 'flex';

    // Agregar evento para cerrar con ESC
    document.addEventListener('keydown', handleEscKey);
}

// Manejar tecla ESC para cerrar editor
function handleEscKey(e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
        const editor = document.getElementById('universal-editor-view');
        if (editor && editor.style.display === 'flex') {
            closeUniversalEditor();
        }
    }
}

function closeUniversalEditor() {
    document.getElementById('universal-editor-view').style.display = 'none';
    // Remover event listener de ESC
    document.removeEventListener('keydown', handleEscKey);
}

// Ayudantes de Edición HTML
function insertTag(tag) {
    const textarea = document.getElementById('uni-content');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selected = text.substring(start, end);
    const replacement = `<${tag}>${selected}</${tag}>`;
    
    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    textarea.focus();
    // Reposicionar cursor
    textarea.selectionStart = start + tag.length + 2;
    textarea.selectionEnd = textarea.selectionStart + selected.length;
}

function autoParagraph() {
    const textarea = document.getElementById('uni-content');
    let text = textarea.value.trim();
    
    if (!text) return;

    if (text.includes('<p>') && !confirm('El texto ya contiene etiquetas <p>. ¿Deseas forzar la conversión de todos modos?')) {
        return;
    }

    text = text.replace(/<p>/gi, '').replace(/<\/p>/gi, '\n');
    const lines = text.split(/\n+/);
    const wrapped = lines
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .map(line => `<p>${line}</p>`)
        .join('\n');

    textarea.value = wrapped;
}

async function uploadUniversalImage(input) {
    if (!input.files || !input.files[0]) return;
    const formData = new FormData();
    formData.append('file', input.files[0]);
    const btn = input.previousElementSibling;
    const oldHtml = btn.innerHTML;
    try {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        const res = await apiFetch('/upload', { method: 'POST', body: formData, isMultipart: true });
        if (res.success) {
            document.getElementById('uni-image').value = res.url;
            
            // En localhost, si la URL es de nuestra API, usar la URL pública de R2 para la vista previa
            let previewUrl = res.url;
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                if (res.url.includes('/api/images/')) {
                    const key = res.url.split('/api/images/')[1];
                    previewUrl = `${API_CONFIG.r2DevUrl}/${key}`;
                } else if (res.url.includes('uploads.sebastianvernis.space/')) {
                    const key = res.url.split('uploads.sebastianvernis.space/')[1];
                    previewUrl = `${API_CONFIG.r2DevUrl}/${key}`;
                }
            }
            
            document.getElementById('uni-preview-img').src = previewUrl;
            document.getElementById('uni-image-preview').style.display = 'block';
        }
    } catch (e) { alert('Error: ' + e.message); }
    finally { btn.disabled = false; btn.innerHTML = oldHtml; }
}

async function saveUniversal(action) {
    const mode = document.getElementById('uni-mode').value;
    const id = document.getElementById('uni-id').value;
    
    // Obtener sitios seleccionados
    const selectedSites = Array.from(document.querySelectorAll('.uni-site-checkbox:checked')).map(cb => cb.value);
    
    const payload = {
        id: id || null,
        title: document.getElementById('uni-title').value.trim(),
        slug: document.getElementById('uni-slug').value.trim(),
        author: document.getElementById('uni-author').value.trim(),
        excerpt: document.getElementById('uni-excerpt').value.trim(),
        imageUrl: document.getElementById('uni-image').value.trim(),
        category: document.getElementById('uni-category').value,
        site: selectedSites[0] || 'cbnnoticias', // Fallback
        sites: selectedSites,
        featured: document.getElementById('uni-featured').value === '1',
        content: document.getElementById('uni-content').value.trim()
    };

    if (!payload.title || !payload.content) return alert('Título y contenido son obligatorios.');

    try {
        if (action === 'draft' || action === 'publish') {
            const cmsPayload = {
                id: payload.id,
                titulo: payload.title,
                contenido: payload.content,
                descripcion: payload.excerpt,
                categoria: payload.category,
                url_imagen: payload.imageUrl,
                destacado: payload.featured ? 1 : 0,
                estado: 'BORRADOR'
            };
            const res = await apiFetch('/cms/articles', { method: 'POST', body: JSON.stringify(cmsPayload) });
            
            if (action === 'publish' && res.success) {
                if (selectedSites.length === 0) return alert('Selecciona al menos un sitio.');
                const fbReq = document.getElementById('uni-publish-fb').checked;
                await apiFetch('/cms/publish', {
                    method: 'POST',
                    body: JSON.stringify({
                        id: res.id,
                        sitios: selectedSites,
                        fb_requerido: fbReq
                    })
                });
                alert('¡Publicado con éxito!');
            } else {
                alert('Borrador guardado.');
            }
        }
        else if (action === 'revision_save' || action === 'revision_approve') {
            const revPayload = {
                titulo: payload.title,
                descripcion: payload.excerpt,
                contenido: payload.content,
                url_imagen: payload.imageUrl
            };
            await apiFetch(`/revision/${id}`, { method: 'PUT', body: JSON.stringify(revPayload) });
            if (action === 'revision_approve') {
                await apiFetch(`/revision/approve/${id}`, { method: 'POST' });
                alert('¡Aprobado y publicado!');
            } else {
                alert('Cambios guardados en revisión.');
            }
        }
        else if (action === 'live_update') {
            await apiFetch(`/articles/${id}`, {
                method: 'PUT',
                body: JSON.stringify(payload)
            });
            alert('Artículo actualizado.');
        }

        closeUniversalEditor();
        const currentView = window.location.hash.replace('#', '') || 'dashboard';
        Router.navigate(currentView);
    } catch (e) { alert('Error: ' + e.message); }
}

async function deleteArticleFromEditor() {
    const id = document.getElementById('uni-id').value;
    if (!id || !confirm('¿Eliminar definitivamente este artículo?')) return;
    try {
        await apiFetch(`/articles/${id}`, { method: 'DELETE' });
        closeUniversalEditor();
        Router.navigate('articles');
    } catch (e) { alert('Error al eliminar: ' + e.message); }
}
