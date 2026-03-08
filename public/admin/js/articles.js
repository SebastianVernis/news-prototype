// Controlador Artículos Públicos con Paginación y Filtros
let articlesData = [];
let currentSite = "";
let currentPage = 1;
const limit = 20;

async function initArticles() {
    currentPage = 1;
    await loadPublicArticles();
}

async function loadPublicArticles() {
    const tbody = document.getElementById('articles-public-table');
    if (!tbody) return;

    // Loading state
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px;"><i class="fas fa-spinner fa-spin fa-2x"></i></td></tr>';

    try {
        const offset = (currentPage - 1) * limit;
        let url = `/articles?limit=${limit}&offset=${offset}`;
        if (currentSite) url += `&site=${currentSite}`;

        const data = await apiFetch(url);
        articlesData = data.articles || [];
        
        if (articlesData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px; color: var(--text-secondary);">No se encontraron artículos.</td></tr>';
        } else {
            tbody.innerHTML = articlesData.map(a => `
                <tr>
                    <td style="font-weight:600;">${a.title || ''}</td>
                    <td><span class="badge-info" style="font-size:0.7rem; background:rgba(6,182,212,0.1); color:var(--primary-color); padding:2px 6px; border-radius:4px;">${a.category || ''}</span></td>
                    <td class="site-cell"><small>${a.site || ''}</small></td>
                    <td style="white-space:nowrap; font-size:0.85rem;">${a.publishedAt ? new Date(a.publishedAt).toLocaleString('es-MX', { 
                        year: 'numeric', 
                        month: '2-digit', 
                        day: '2-digit', 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    }) : '-'}</td>
                    <td class="col-actions">
                        <div class="actions">
                            ${!a.fb_published ? `
                                <button class="btn btn-outline" style="color:#1877F2; border-color:#1877F2;" title="Publicar en Facebook" onclick="publishToFBManual('${a.id}')">
                                    <i class="fab fa-facebook"></i>
                                </button>
                            ` : '<button class="btn btn-outline" disabled style="opacity:0.5; color:#cbd5e1; border-color:#e2e8f0;"><i class="fab fa-facebook"></i></button>'}
                            <button class="btn btn-outline" onclick="editArticleUnified('${a.id}')" title="Editar"><i class="fas fa-edit"></i></button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        // Actualizar UI paginación
        document.getElementById('page-info').textContent = `Página ${currentPage}`;
        document.getElementById('prev-page').disabled = currentPage === 1;
        document.getElementById('next-page').disabled = articlesData.length < limit;

    } catch (e) { 
        console.error(e); 
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: #dc3545; padding: 40px;">Error al cargar datos: ${e.message}</td></tr>`;
    }
}

async function changeSiteFilter() {
    currentSite = document.getElementById('filter-site').value;
    currentPage = 1;
    await loadPublicArticles();
}

async function changePage(step) {
    currentPage += step;
    if (currentPage < 1) currentPage = 1;
    await loadPublicArticles();
}

async function editArticleUnified(id) {
    try {
        const data = await apiFetch('/articles/id/' + id);
        const a = data.article;
        if (!a) return;

        openUniversalEditor('live', {
            id: a.id,
            title: a.title,
            slug: a.slug,
            content: a.content,
            excerpt: a.excerpt,
            category: a.category,
            author: a.author,
            imageUrl: a.imageUrl,
            site: a.site,
            featured: a.featured
        });
    } catch (e) { alert(e.message); }
}

function showLoading(msg = "Procesando...") {
    const loader = document.getElementById('global-loader');
    const message = document.getElementById('loader-message');
    if (loader) {
        if (message) message.textContent = msg;
        loader.style.display = 'flex';
    }
}

function hideLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) loader.style.display = 'none';
}

async function publishToFBManual(id) {
    if (!confirm('¿Deseas poner este artículo en cola para publicarlo en Facebook?')) return;

    showLoading("Publicando en Facebook...");
    try {
        const res = await apiFetch(`/articles/publish-fb/${id}`, { method: 'POST' });
        if (res.success) {
            showSuccessToast('¡Publicado!', 'El artículo se publicó en Facebook correctamente.', 3000);
        } else {
            showErrorToast('Fallo en Meta API', res.error || 'No se pudo publicar en Facebook.', 5000);
        }
        await loadPublicArticles();
    } catch (e) {
        showErrorToast('Error de Conexión', e.message, 5000);
    } finally {
        hideLoading();
    }
}

function showNewArticle() {
    openUniversalEditor('cms');
}
