async function initDashboard() {
    const tbody = document.getElementById('recent-articles-tbody');
    if (!tbody) return;
    
    try {
        const data = await apiFetch('/articles?limit=5');
        const articles = data.articles || [];
        
        document.getElementById('dash-total-articles').textContent = data.totalResults || 0;
        
        tbody.innerHTML = articles.map(a => `
            <tr>
                <td>${a.title}</td>
                <td>${a.category}</td>
                <td><span class="status-badge status-featured">Publicado</span></td>
                <td>${new Date(a.publishedAt).toLocaleDateString()}</td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4">Error: ${e.message}</td></tr>`;
    }
}
