// Controlador Artículos Públicos Simplificado (Usa Editor Universal)
let articlesData = [];

async function initArticles() {
    await loadPublicArticles();
}

async function loadPublicArticles() {
    const tbody = document.getElementById('articles-public-table');
    if (!tbody) return;
    try {
        const data = await apiFetch('/articles?limit=100');
        articlesData = data.articles || [];
        tbody.innerHTML = articlesData.map(a => `
            <tr>
                <td>${a.title || ''}</td>
                <td>${a.category || ''}</td>
                <td class="site-cell">${a.site || ''}</td>
                <td style="white-space:nowrap;">${a.publishedAt ? new Date(a.publishedAt).toLocaleString('es-MX', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : '-'}</td>
                <td class="actions">
                    ${!a.fb_published ? `
                        <button class="btn btn-outline" style="color:#1877F2; border-color:#1877F2;" title="Publicar en Facebook" onclick="publishToFBManual('${a.id}')">
                            <i class="fab fa-facebook"></i>
                        </button>
                    ` : '<i class="fab fa-facebook" style="color:#ddd;" title="Ya en Facebook"></i>'}
                    <button class="btn btn-outline" onclick="editArticleUnified('${a.id}')"><i class="fas fa-edit"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (e) { console.error(e); }
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

async function publishToFBManual(id) {
    if (!confirm('¿Deseas poner este artículo en cola para publicarlo en Facebook?')) return;
    try {
        await apiFetch(`/articles/publish-fb/${id}`, { method: 'POST' });
        alert('¡Artículo en cola! Se publicará en unos minutos automáticamente.');
        await loadPublicArticles();
    } catch (e) { alert('Error: ' + e.message); }
}

function showNewArticle() {
    openUniversalEditor('cms'); // Los nuevos artículos se crean vía flujo CMS
}
