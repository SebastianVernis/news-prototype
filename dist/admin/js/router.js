const Router = {
    contentElement: null,
    currentView: null,

    async init() {
        this.contentElement = document.getElementById('main-content');
        window.addEventListener('popstate', () => this.loadFromUrl());
        this.loadFromUrl();
    },

    async navigate(view, pushState = true) {
        // Permitir recargar la misma vista para refrescar tablas
        try {
            // Intentar cargar el fragmento HTML
            const response = await fetch(`/admin/views/${view}.html`);
            if (!response.ok) throw new Error(`Vista ${view} no encontrada (HTTP ${response.status})`);
            
            const html = await response.text();
            this.contentElement.innerHTML = html;
            this.currentView = view;

            // Actualizar Sidebar
            document.querySelectorAll('.nav-link').forEach(l => {
                l.classList.toggle('active', l.dataset.view === view);
            });

            if (pushState) {
                const url = `#${view}`;
                if (window.location.hash !== url) history.pushState({ view }, '', url);
            }

            // Inicializar controlador específico
            console.log(`Iniciando controlador para: ${view}`);
            this.initController(view);
        } catch (e) {
            console.error('Error en Router:', e);
            this.contentElement.innerHTML = `
                <div class="card" style="border-left: 5px solid #dc3545;">
                    <h2>Error 404</h2>
                    <p>No se pudo cargar la vista: <strong>${view}</strong></p>
                    <p><small>${e.message}</small></p>
                    <button class="btn btn-outline" onclick="location.reload()">Reintentar</button>
                </div>
            `;
        }
    },

    loadFromUrl() {
        const view = window.location.hash.replace('#', '') || 'dashboard';
        this.navigate(view, false);
    },

    initController(view) {
        // Timeout pequeño para asegurar que el DOM se haya inyectado
        setTimeout(() => {
            switch(view) {
                case 'dashboard': if (window.initDashboard) initDashboard(); break;
                case 'cms': if (window.initCMS) initCMS(); break;
                case 'revision': if (window.initRevision) initRevision(); break;
                case 'sites': if (window.initSites) initSites(); break;
                case 'categories': if (window.initCategories) initCategories(); break;
                case 'articles': if (window.initArticles) initArticles(); break;
            }
        }, 50);
    }
};
