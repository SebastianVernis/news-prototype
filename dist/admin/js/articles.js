async function initArticles() {
    await loadPublicArticles();
}

async function loadPublicArticles() {
    const tbody = document.getElementById('articles-public-table');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5">Cargando...</td></tr>';
    try {
        const data = await apiFetch('/articles?limit=50');
        const articles = data.articles || [];
        tbody.innerHTML = articles.map(a => `
            <tr>
                <td>${a.title}</td>
                <td>${a.category}</td>
                <td>${(a.sites || []).join(', ')}</td>
                <td>${new Date(a.publishedAt).toLocaleDateString()}</td>
                <td class="actions">
                    <button class="btn btn-outline" onclick="editPublicArticle('${a.id}')"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-danger" onclick="deletePublicArticle('${a.id}')"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5">Error: ${e.message}</td></tr>`;
    }
}

async function editPublicArticle(id) {
    alert('Función de edición rápida de artículos públicos en desarrollo. Por ahora, puedes editarlos en la Mesa de Revisión si aún no han sido aprobados, o borrarlos y volver a publicarlos.');
}

async function deletePublicArticle(id) {
    if(confirm('¿Eliminar artículo de los sitios públicos?')) {
        try {
            await apiFetch(`/articles/${id}`, { method: 'DELETE' });
            loadPublicArticles();
        } catch (e) {
            console.error('Error al borrar:', e);
            // Si el error fue un 404 pero el artículo ya no está, simplemente refrescamos
            loadPublicArticles();
        }
    }
}
