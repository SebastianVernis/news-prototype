// Controlador CMS Simplificado (Usa Editor Universal)
async function initCMS() {
    await loadCMSArticles();
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
                <td>${a.FECHA_CREACION ? new Date(a.FECHA_CREACION).toLocaleString('es-MX', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : '-'}</td>
                <td class="actions">
                    <button class="btn btn-outline" onclick="editCMSArticleUnified('${a.ID}')"><i class="fas fa-edit"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (e) { console.error('Error cargando artículos CMS:', e); }
}

async function editCMSArticleUnified(id) {
    try {
        const articles = await apiFetch('/cms/articles');
        const a = articles.find(x => x.ID === id);
        if (!a) return;

        openUniversalEditor('cms', {
            id: a.ID,
            title: a.TITULO,
            content: a.CONTENIDO,
            excerpt: a.DESCRIPCION,
            category: a.CATEGORIA,
            imageUrl: a.URL_IMAGEN,
            featured: a.DESTACADO === 1
        });
    } catch (e) { alert(e.message); }
}

function showNewCMSArticle() {
    openUniversalEditor('cms');
}
