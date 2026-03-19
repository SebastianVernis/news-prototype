// Controlador Artículos Destacados
async function initFeatured() {
    await loadFeaturedArticles();
}

async function loadFeaturedArticles() {
    const tbody = document.getElementById('featured-articles-table');
    if (!tbody) return;

    try {
        // Obtenemos artículos públicos (limitados a 100 para buscar destacados)
        const data = await apiFetch('/articles?limit=100');
        const featured = (data.articles || []).filter(a => a.featured);

        if (featured.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:2rem;">No hay artículos marcados como destacados.</td></tr>';
            return;
        }

        tbody.innerHTML = featured.map(a => `
            <tr>
                <td>${a.title}</td>
                <td style="font-size:0.8rem; max-width:200px; overflow:hidden; text-overflow:ellipsis;">${a.site}</td>
                <td>${a.category}</td>
                <td style="white-space:nowrap; font-size:0.85rem;">${a.publishedAt ? new Date(a.publishedAt).toLocaleString('es-MX', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : '-'}</td>
                <td class="actions">
                    <button class="btn btn-outline" title="Editar" onclick="editArticleUnified('${a.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger" title="Quitar Destacado" onclick="removeFeatured('${a.id}')">
                        <i class="fas fa-star-half-alt"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5">Error: ${e.message}</td></tr>`;
    }
}

async function removeFeatured(id) {
    if (!confirm('¿Quitar este artículo de la sección de destacados?')) return;
    try {
        const data = await apiFetch('/articles/id/' + id);
        const art = data.article;
        if (!art) return;

        // Actualizar el estado de destacado a 0
        const payload = { ...art, featured: false };
        await apiFetch(`/articles/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
        
        await loadFeaturedArticles();
    } catch (e) { alert(e.message); }
}
