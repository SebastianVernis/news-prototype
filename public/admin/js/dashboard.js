// Controlador Dashboard - Datos Reales (Adaptado al nuevo sistema por sitio)
async function initDashboard() {
    await loadDashboardStats();
    await loadRecentArticles();
    await loadSiteStats();
    await loadLiveMetrics();
    await loadCronStatus();
}

// Cargar estado del cron y mostrar próximo timer
async function loadCronStatus() {
    try {
        const status = await apiFetch('/cron/status');
        
        // Actualizar próximo timer de ingesta
        const nextTimer = document.getElementById('next-ingest-timer');
        if (nextTimer && status.nextRunInMinutes !== undefined) {
            const mins = status.nextRunInMinutes;
            const secs = status.nextRunInSeconds || 0;
            nextTimer.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
            
            // Auto-refresh
            setTimeout(loadCronStatus, 10000);
        }
    } catch (e) {
        console.error('Cron status error:', e);
    }
}

async function loadDashboardStats() {
    try {
        const stats = await apiFetch('/stats/dashboard');

        // Actualizar métricas principales
        const mappings = {
            'stat-total-articles': stats.articles,
            'stat-pending-revision': stats.pending,
            'stat-total-drafts': stats.drafts,
            'stat-total-facebook': stats.facebook,
            'stat-facebook-pending': stats.facebookPending || 0,
            'stat-total-sites': stats.sites,
            'stat-web-today': stats.webToday || 0
        };

        for (const [id, value] of Object.entries(mappings)) {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = value.toLocaleString('es-MX');
                // Animación de actualización
                el.style.transform = 'scale(1.2)';
                setTimeout(() => el.style.transform = 'scale(1)', 200);
            }
        }
    } catch (e) { console.error('Error stats:', e); }
}

// Nuevo: Métricas en vivo (auto-actualización cada 30 seg)
async function loadLiveMetrics() {
    const liveContainer = document.getElementById('live-metrics');
    if (!liveContainer) return;
    
    try {
        const stats = await apiFetch('/stats/dashboard');
        
        liveContainer.innerHTML = `
            <div class="metric-card">
                <div class="metric-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <i class="fas fa-globe"></i>
                </div>
                <div class="metric-details">
                    <div class="metric-value">${(stats.webToday || 0).toLocaleString('es-MX')}</div>
                    <div class="metric-label">Web Hoy</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="metric-details">
                    <div class="metric-value">${(stats.facebookPending || 0).toLocaleString('es-MX')}</div>
                    <div class="metric-label">Cola FB</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="metric-details">
                    <div class="metric-value">${(stats.facebook || 0).toLocaleString('es-MX')}</div>
                    <div class="metric-label">FB Publicados</div>
                </div>
            </div>
        `;
    } catch (e) {
        console.error('Live metrics error:', e);
    }
    
    // Auto-actualizar cada 30 segundos
    setTimeout(loadLiveMetrics, 30000);
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

// Nuevo: Cargar estadísticas por sitio del nuevo sistema ARTICULOS_SITIO_{SLUG}
async function loadSiteStats() {
    const tbody = document.getElementById('site-stats-table');
    if (!tbody) return;

    try {
        // Obtener estadísticas desde el nuevo endpoint
        const stats = await apiFetch('/sites/stats');
        
        // Obtener diagnóstico del cron para timers
        let diagnostics = {};
        try {
            const diag = await apiFetch('/cron/diagnostic');
            if (diag && diag.diagnostics) {
                diagnostics = diag.diagnostics.reduce((acc, d) => {
                    acc[d.site] = d;
                    return acc;
                }, {});
            }
        } catch (e) {
            console.log('Diagnostic not available');
        }

        if (!stats || stats.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No hay sitios configurados.</td></tr>';
            return;
        }

        tbody.innerHTML = stats.map(s => {
            const diag = diagnostics[s.slug] || {};
            const timerReady = diag.timer?.ready;
            const timerRemaining = diag.timer?.expires || '-';
            const pending = diag.articles?.pending || 0;
            
            return `
            <tr>
                <td><strong>${s.name}</strong><br><small style="color:var(--text-secondary);">${s.slug}</small></td>
                <td style="text-align:center;">
                    <span style="font-weight:600; color: var(--primary-color);">${s.total}</span>
                    ${pending > 0 ? `<br><small style="color: var(--text-secondary);">${pending} pend.</small>` : ''}
                </td>
                <td style="text-align:center;">
                    <span class="status-badge status-featured" style="font-size:0.75rem; background:rgba(24,119,242,0.1); color:#1877F2;">
                        ${s.fb}
                    </span>
                </td>
                <td style="text-align:center;">
                    ${timerReady === true ? 
                        '<span class="status-badge" style="background:rgba(16,185,129,0.1); color:#10b981;"><i class="fas fa-play"></i> Listo</span>' :
                        timerReady === false ?
                        `<span style="color: var(--text-secondary); font-size:0.8rem;">${timerRemaining} min</span>` :
                        '-'
                    }
                </td>
                <td style="text-align:center;">
                    ${s.fb > 0 ? '<span class="status-badge status-featured" style="font-size:0.7rem;"><i class="fas fa-check"></i> Activo</span>' : '<small style="color:var(--text-secondary);">Sin actividad</small>'}
                </td>
            </tr>
        `}).join('');
    } catch (e) {
        console.error('Error loading site stats:', e);
        tbody.innerHTML = '<tr><td colspan="5">Error al cargar estadísticas por sitio.</td></tr>';
    }
}
