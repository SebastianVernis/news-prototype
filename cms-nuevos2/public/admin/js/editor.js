// LÓGICA DEL EDITOR UNIVERSAL (CENTRALIZADA)
// Ahora funciona como una vista independiente del SPA Router

let editorPendingData = null;

async function initEditor() {
    console.log("[Editor] Inicializando vista independiente...");
    
    // Si no hay datos pendientes, intentar recuperar del último modo guardado o por defecto a CMS
    const mode = editorPendingData ? editorPendingData.mode : 'cms';
    const data = editorPendingData ? editorPendingData.data : {};
    
    await setupEditorUI(mode, data);
    
    // Limpiar después de usar solo si se cargó algo
    if (editorPendingData) editorPendingData = null;
}

/**
 * Función compatible con las llamadas existentes.
 * En lugar de abrir un modal, navega a la ruta 'editor'.
 */
function openUniversalEditor(mode, data = {}) {
    editorPendingData = { mode, data };
    Router.navigate('editor');
}

/**
 * Configura los elementos del DOM de la vista editor.html
 */
async function setupEditorUI(mode, data = {}) {
    const titleEl = document.getElementById('universal-editor-title');
    const actionsContainer = document.getElementById('uni-actions-container');
    const fbSection = document.getElementById('uni-fb-section');
    const fbPlaceholder = document.getElementById('uni-fb-placeholder');
    const sitesContainer = document.getElementById('uni-sites-container');
    
    // Limpiar formulario previo si existe
    const form = document.getElementById('universal-article-form');
    if (form) form.reset();
    
    const previewBox = document.getElementById('uni-image-preview');
    const previewImg = document.getElementById('uni-preview-img');
    if (previewBox) previewBox.style.display = 'none';
    if (previewImg) previewImg.src = '';

    if (fbSection && fbPlaceholder) {
        fbSection.style.display = 'none';
        fbPlaceholder.style.display = 'none';
    }

    if (actionsContainer) actionsContainer.innerHTML = '';

    // Configurar modo y acciones
    if (mode === 'cms') {
        if (titleEl) titleEl.textContent = data.id ? 'Editar Artículo CMS' : 'Nuevo Artículo CMS';
        if (actionsContainer) {
            actionsContainer.innerHTML = `
                <button type="button" class="btn btn-outline" onclick="saveUniversal('draft')">
                    <i class="fas fa-save"></i> Guardar Borrador
                </button>
                <button type="button" class="btn btn-primary" onclick="saveUniversal('publish')">
                    <i class="fas fa-paper-plane"></i> Publicar en Sitios
                </button>
            `;
        }
        if (fbSection) fbSection.style.display = 'block';
        if (fbPlaceholder) fbPlaceholder.style.display = 'none';
    } else {
        if (fbSection) fbSection.style.display = 'none';
        if (fbPlaceholder) fbPlaceholder.style.display = 'block';

        if (mode === 'live') {
            if (titleEl) titleEl.textContent = 'Editar Artículo Publicado';
            if (actionsContainer) {
                actionsContainer.innerHTML = `
                    <button type="button" class="btn btn-primary" onclick="saveUniversal('live_update')">
                        <i class="fas fa-sync"></i> Actualizar Cambios
                    </button>
                    <button type="button" class="btn btn-outline" style="color:#ef4444; border-color:#ef4444;" onclick="deleteLiveArticle('${data.id}')">
                        <i class="fas fa-trash"></i> Eliminar
                    </button>
                `;
            }
        }
    }

    // Setear valores en los inputs
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
    
    setVal('uni-id', data.id);
    setVal('uni-mode', mode);
    setVal('uni-title', data.title);
    setVal('uni-slug', data.slug);
    setVal('uni-author', data.author);
    setVal('uni-excerpt', data.excerpt);
    setVal('uni-image', data.imageUrl);
    
    const catEl = document.getElementById('uni-category');
    if (catEl) {
        const catVal = (data.category || 'POLITICA').toUpperCase();
        catEl.value = catVal;
    }
    
    const featEl = document.getElementById('uni-featured');
    if (featEl) featEl.value = data.featured ? '1' : '0';
    
    const contentEl = document.getElementById('uni-content');
    if (contentEl) contentEl.value = data.content || '';

    const fbCheckbox = document.getElementById('uni-publish-fb');
    if (fbCheckbox) fbCheckbox.checked = data.fbRequired || false;

    // Preview de imagen
    if (data.imageUrl) {
        let fullImageUrl = data.imageUrl;
        if (data.imageUrl.startsWith('/api/images/')) {
            const key = data.imageUrl.replace('/api/images/', '');
            fullImageUrl = `https://uploads.sebastianvernis.space/${key}`;
        }
        if (previewImg) previewImg.src = fullImageUrl;
        if (previewBox) previewBox.style.display = 'block';
    } else {
        if (previewBox) previewBox.style.display = 'none';
    }

    // Cargar Sitios dinámicamente
    if (sitesContainer) {
        sitesContainer.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando sitios...';
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
    }
}

function closeUniversalEditor() {
    const mode = document.getElementById('uni-mode').value;
    Router.navigate(mode === 'live' ? 'articles' : 'cms');
}

// Toggle Seleccionar todos los sitios
function toggleAllSites() {
    const checkboxes = document.querySelectorAll('.uni-site-checkbox');
    if (checkboxes.length === 0) return;
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => { cb.checked = !allChecked; });
    const btn = document.querySelector('[onclick="toggleAllSites()"]');
    if (btn) {
        btn.innerHTML = allChecked 
            ? '<i class="fas fa-check-square"></i> Seleccionar todos' 
            : '<i class="fas fa-square"></i> Deseleccionar todos';
    }
}

// Auxiliares del Editor (Tags, Imágenes, etc)
function insertTag(tag) {
    const textarea = document.getElementById('uni-content');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selected = text.substring(start, end);
    
    let replacement = "";
    if (tag === 'ul' || tag === 'ol') {
        // Si es una lista, rodear el contenido seleccionado con <li> si no está vacío
        const items = selected ? selected.split('\n').map(li => `  <li>${li}</li>`).join('\n') : "  <li></li>";
        replacement = `<${tag}>\n${items}\n</${tag}>`;
    } else {
        replacement = `<${tag}>${selected}</${tag}>`;
    }
    
    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    textarea.focus();
}

function insertLink() {
    const url = prompt("URL del enlace:");
    if (url) {
        const textarea = document.getElementById('uni-content');
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selected = textarea.value.substring(start, end);
        const replacement = `<a href="${url}" target="_blank">${selected || url}</a>`;
        textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    }
}

function autoParagraph() {
    const textarea = document.getElementById('uni-content');
    let text = textarea.value.trim();
    if (!text) return;
    if (!text.startsWith('<p>')) {
        text = text.split('\n').filter(line => line.trim() !== '').map(line => `<p>${line.trim()}</p>`).join('\n');
        textarea.value = text;
    }
}

function insertYouTube() {
    const url = prompt("URL de YouTube (Video o Reel):");
    if (!url) return;
    let videoId = "";
    if (url.includes('v=')) videoId = url.split('v=')[1].split('&')[0];
    else if (url.includes('youtu.be/')) videoId = url.split('youtu.be/')[1].split('?')[0];
    else if (url.includes('shorts/')) videoId = url.split('shorts/')[1].split('?')[0];
    
    if (videoId) {
        const embed = `\n<div class="video-container"><iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen></iframe></div>\n`;
        const textarea = document.getElementById('uni-content');
        textarea.value += embed;
    }
}

function insertTwitter() {
    const url = prompt("URL del Tweet:");
    if (url) {
        const embed = `\n<blockquote class="twitter-tweet"><a href="${url}"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"><\/script>\n`;
        document.getElementById('uni-content').value += embed;
    }
}

function insertInstagram() {
    const url = prompt("URL de Instagram (Post/Reel):");
    if (url) {
        const cleanUrl = url.split('?')[0];
        const embed = `\n<div class="instagram-embed" style="display:flex; justify-content:center; margin:25px 0;"><blockquote class="instagram-media" data-instgrm-permalink="${cleanUrl}" data-instgrm-version="14" style="background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%;"></blockquote></div><script async src="//www.instagram.com/embed.js"><\/script>\n`;
        document.getElementById('uni-content').value += embed;
    }
}

function insertImage() {
    // En lugar de pedir URL, abrimos el selector de archivos
    document.getElementById('uni-content-image-input').click();
}

async function uploadContentImage(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    if (window.showLoading) showLoading("Subiendo imagen al servidor...");

    try {
        const res = await fetch(`${window.ADMIN_API_BASE_URL}/upload`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('CMS_AUTH_TOKEN')}` },
            body: formData
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.error || data.message || `Error al subir imagen (HTTP ${res.status})`);
        }

        if (!data.url) {
            throw new Error('La API no devolvió la URL de la imagen');
        }

        const textarea = document.getElementById('uni-content');
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;

        // Insertar el HTML de la imagen en la posición del cursor
        const embed = `\n<figure class="content-image">\n  <img src="${data.url}" alt="imagen">\n  <figcaption>Descripción de la imagen</figcaption>\n</figure>\n`;
        textarea.value = text.substring(0, start) + embed + text.substring(end);

        if (typeof showSuccessToast === 'function') {
            showSuccessToast('Imagen Insertada', 'La imagen se subió correctamente', 3000);
        }
        textarea.focus();
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error al Subir Imagen', e.message, 5000);
        }
    } finally {
        if (window.hideLoading) hideLoading();
        input.value = ''; // Resetear input para permitir subir la misma imagen si se desea
    }
}

async function uploadUniversalImage(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const btn = document.querySelector('.btn-upload-image');
    const originalHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subiendo...';

    try {
        const res = await fetch(`${window.ADMIN_API_BASE_URL}/upload`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('CMS_AUTH_TOKEN')}` },
            body: formData
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.error || data.message || `Error al subir portada (HTTP ${res.status})`);
        }

        if (!data.url) {
            throw new Error('La API no devolvió la URL de la portada');
        }

        document.getElementById('uni-image').value = data.url;
        document.getElementById('uni-preview-img').src = data.url;
        document.getElementById('uni-image-preview').style.display = 'block';
        if (typeof showSuccessToast === 'function') {
            showSuccessToast('Imagen Subida', 'La portada se subió correctamente', 3000);
        }
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error al Subir', e.message, 5000);
        }
    }
    finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
    }
}

async function saveUniversal(action) {
    const id = document.getElementById('uni-id').value;
    const mode = document.getElementById('uni-mode').value;
    const selectedSites = Array.from(document.querySelectorAll('.uni-site-checkbox:checked')).map(cb => cb.value);

    const payload = {
        title: document.getElementById('uni-title').value.trim(),
        slug: document.getElementById('uni-slug').value.trim(),
        author: document.getElementById('uni-author').value.trim(),
        category: document.getElementById('uni-category').value,
        excerpt: document.getElementById('uni-excerpt').value.trim(),
        imageUrl: document.getElementById('uni-image').value.trim(),
        featured: document.getElementById('uni-featured').value === '1',
        content: document.getElementById('uni-content').value.trim(),
        site: selectedSites.join(','),
        fbRequired: document.getElementById('uni-publish-fb')?.checked || false
    };

    if (!payload.title) {
        showErrorToast('Campo Requerido', 'El título es obligatorio', 3000);
        return;
    }

    if (!payload.content) {
        showErrorToast('Campo Requerido', 'El contenido es obligatorio', 3000);
        return;
    }

    if (selectedSites.length === 0) {
        showErrorToast('Selección Requerida', 'Debes seleccionar al menos un sitio de destino', 3000);
        return;
    }

    if (window.showLoading) showLoading("Guardando artículo...");

    try {
        if (mode === 'cms') {
            // Step 1: Save to CMS table (always)
            const cmsPayload = { 
                id, 
                titulo: payload.title,
                contenido: payload.content,
                descripcion: payload.excerpt,
                categoria: payload.category,
                url_imagen: payload.imageUrl,
                destacado: payload.featured ? 1 : 0,
                estado: 'BORRADOR' // Always save as BORRADOR first
            };
            
            // If editing existing article, include id and estado
            if (id) {
                cmsPayload.estado = payload.status || 'BORRADOR';
            }
            
            const saveResult = await apiFetch('/cms/articles', { 
                method: 'POST', 
                body: JSON.stringify(cmsPayload) 
            });
            
            const articleId = id || saveResult.id;
            
            // Step 2: If publishing, also call /cms/publish to move to PARAFRASEADOS
            if (action === 'publish') {
                if (window.showLoading) showLoading("Publicando en sitios...");
                
                await apiFetch('/cms/publish', { 
                    method: 'POST', 
                    body: JSON.stringify({ 
                        id: articleId, 
                        sitios: selectedSites, 
                        fb_requerido: payload.fbRequired 
                    }) 
                });
            }
            
            if (action === 'publish' && payload.fbRequired) {
                console.log("Artículo marcado para Facebook");
            }
        } else if (mode === 'live') {
            await apiFetch('/articles/' + id, { method: 'PUT', body: JSON.stringify(payload) });
        }

        if (typeof showSuccessToast === 'function') {
            showSuccessToast('¡Operación Exitosa!', 'El artículo se guardó correctamente', 3000);
        }

        closeUniversalEditor();
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error al Guardar', e.message, 5000);
        }
    }
    finally { if (window.hideLoading) hideLoading(); }
}

async function deleteLiveArticle(id) {
    if (!confirm('¿Estás seguro de ELIMINAR permanentemente este artículo de todos los sitios?')) return;
    if (window.showLoading) showLoading("Eliminando...");
    try {
        await apiFetch(`/articles/${id}`, { method: 'DELETE' });
        closeUniversalEditor();
        if (typeof showSuccessToast === 'function') {
            showSuccessToast('Artículo Eliminado', 'El artículo fue eliminado correctamente', 3000);
        }
    } catch (e) {
        if (typeof showErrorToast === 'function') {
            showErrorToast('Error al Eliminar', e.message, 5000);
        }
    }
    finally { if (window.hideLoading) hideLoading(); }
}
