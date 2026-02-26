// Controlador Dashboard - Datos Reales
async function initDashboard() {
    await loadDashboardStats();
    await loadRecentArticles();
}

async function loadDashboardStats() {
    try {
        const stats = await apiFetch('/stats/dashboard');
        
        // Mapear IDs de los elementos (asumiendo IDs estándar en dashboard.html)
        const mappings = {
            'stat-total-articles': stats.articles,
            'stat-pending-revision': stats.pending,
            'stat-total-drafts': stats.drafts,
            'stat-total-facebook': stats.facebook,
            'stat-total-sites': stats.sites
        };

        for (const [id, value] of Object.entries(mappings)) {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        }
    } catch (e) { console.error('Error stats:', e); }
}

async function loadRecentArticles() {
    const tbody = document.getElementById('recent-articles-table');
    if (!tbody) return;

    try {
        const data = await apiFetch('/articles?limit=5');
        const articles = data.articles || [];

        if (articles.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3">No hay actividad reciente.</td></tr>';
            return;
        }

        tbody.innerHTML = articles.map(a => `
            <tr>
                <td>${a.title}</td>
                <td><span class="status-badge status-featured">${a.site}</span></td>
                <td style="white-space:nowrap; font-size:0.85rem;">${a.publishedAt ? new Date(a.publishedAt).toLocaleString('es-MX', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : '-'}</td>
            </tr>
        `).join('');
    } catch (e) { console.error(e); }
}
