/**
 * Controlador para el Explorador de Contenido Live
 */
async function initContentExplorer() {
    console.log('[Explorer] Iniciando...');
    await loadExplorerArticles();
}

async function loadExplorerArticles() {
    const grid = document.getElementById('explorer-grid');
    if (!grid) return;

    const site = document.getElementById('explorer-site-filter').value;
    const category = document.getElementById('explorer-category-filter').value;

    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem;"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Escaneando red de noticias...</p></div>';

    try {
        let url = `/articles?limit=24`;
        if (site) url += `&site=${site}`;
        if (category) url += `&category=${category}`;

        const data = await apiFetch(url);
        const articles = data.articles || data;

        if (!articles || articles.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 3rem;"><i class="fas fa-search fa-2x" style="color:#cbd5e1; margin-bottom:1rem;"></i><p>No se encontraron artículos con estos filtros.</p></div>';
            return;
        }

        grid.innerHTML = articles.map(a => {
            const date = new Date(a.publishedAt).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
            
            // Procesar sitios
            let sites = [];
            if (a.site) {
                sites = a.site.split(',').map(s => s.trim());
            } else if (a.sitio_destino) {
                sites = a.sitio_destino.split(',').map(s => s.trim());
            }

            return `
                <div class="explorer-card">
                    <img src="${a.imageUrl || 'assets/fallback-1.svg'}" class="explorer-img" alt="${a.title}" onerror="this.src='assets/fallback-1.svg'">
                    <div class="explorer-content">
                        <div class="explorer-tag">${a.category || 'Nacional'}</div>
                        <div class="explorer-title" title="${a.title}">${a.title}</div>
                        
                        <div class="explorer-sites">
                            ${sites.map(s => `<span class="site-pill">${s}</span>`).join('')}
                        </div>

                        <div class="explorer-footer">
                            <span><i class="far fa-calendar-alt"></i> ${date}</span>
                            <span style="text-transform: uppercase; font-weight: 800; font-size: 0.6rem; color: #94a3b8;">${a.sourceTable || 'API'}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

    } catch (e) {
        grid.innerHTML = `<div style="grid-column: 1/-1; color: #ef4444; text-align: center; padding: 2rem;">Error: ${e.message}</div>`;
    }
}
