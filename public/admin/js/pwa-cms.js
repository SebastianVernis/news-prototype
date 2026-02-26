/**
 * CMS PWA & Local Data Backup Manager
 */
const CMSPWA = {
    DB_NAME: 'NexoPress_CMS_Backup',
    STORES: ['articles', 'sites', 'revision'],
    UPDATE_INTERVAL: 30 * 60 * 1000, // 30 min

    async init() {
        console.log('[CMS-PWA] Iniciando...');
        this.registerSW();
        await this.initDB();
        this.startSyncCycle();
    },

    registerSW() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('[CMS-PWA] SW Registrado'))
                .catch(err => console.error('[CMS-PWA] Error SW:', err));
        }
    },

    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, 1);
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                this.STORES.forEach(s => {
                    if (!db.objectStoreNames.contains(s)) db.createObjectStore(s, { keyPath: 'ID' });
                });
            };
            request.onsuccess = () => resolve();
            request.onerror = () => reject();
        });
    },

    startSyncCycle() {
        // Primera sincronización
        this.syncAll();
        // Ciclo cada 30 min
        setInterval(() => this.syncAll(), this.UPDATE_INTERVAL);
        
        // Verificar si estamos instalados para mostrar el indicador
        this.updateSyncUI();
    },

    async syncAll() {
        console.log('[CMS-PWA] Iniciando ciclo de respaldo local (30 min)...');
        try {
            // Sincronizar Sitios
            const sites = await apiFetch('/sites');
            if (sites) await this.saveToLocal('sites', sites);

            // Sincronizar Últimos Artículos (CMS)
            const articles = await apiFetch('/articles?limit=50');
            if (articles && articles.articles) await this.saveToLocal('articles', articles.articles);

            // Sincronizar Mesa de Revisión
            const revision = await apiFetch('/revision');
            if (revision) await this.saveToLocal('revision', revision);

            const now = new Date();
            localStorage.setItem('CMS_LAST_SYNC', now.toISOString());
            this.updateSyncUI();
            
            console.log('[CMS-PWA] Respaldo local completado con éxito.');
        } catch (e) {
            console.warn('[CMS-PWA] Falló la sincronización (Offline):', e.message);
        }
    },

    updateSyncUI() {
        const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
        if (!isStandalone) return;

        let indicator = document.getElementById('pwa-sync-indicator');
        if (!indicator) {
            // Buscar un lugar en el header para inyectarlo
            const headerActions = document.querySelector('.header-actions') || document.querySelector('.user-profile');
            if (!headerActions) return;

            indicator = document.createElement('div');
            indicator.id = 'pwa-sync-indicator';
            indicator.style.cssText = 'font-size: 0.7rem; color: #10b981; background: #dcfce7; padding: 2px 8px; border-radius: 10px; margin-right: 10px; display: flex; align-items: center; gap: 4px; border: 1px solid #b9f6ca;';
            headerActions.parentNode.insertBefore(indicator, headerActions);
        }

        const lastSync = localStorage.getItem('CMS_LAST_SYNC');
        if (lastSync) {
            const time = new Date(lastSync).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            indicator.innerHTML = `<i class="fas fa-cloud-download-alt"></i> Backup: ${time}`;
            indicator.title = 'Respaldo local actualizado (Modo App)';
        }
    },

    async saveToLocal(storeName, data) {
        return new Promise((resolve) => {
            const request = indexedDB.open(this.DB_NAME, 1);
            request.onsuccess = (e) => {
                const db = e.target.result;
                const tx = db.transaction(storeName, 'readwrite');
                const store = tx.objectStore(storeName);
                
                const items = Array.isArray(data) ? data : [data];
                items.forEach(item => {
                    if (item.ID) store.put(item);
                });
                tx.oncomplete = () => resolve();
            };
        });
    },

    /**
     * Helper para obtener datos si estamos offline
     */
    async getBackup(storeName) {
        return new Promise((resolve) => {
            const request = indexedDB.open(this.DB_NAME, 1);
            request.onsuccess = (e) => {
                const db = e.target.result;
                const tx = db.transaction(storeName, 'readonly');
                const store = tx.objectStore(storeName);
                const req = store.getAll();
                req.onsuccess = () => resolve(req.result);
            };
            request.onerror = () => resolve([]);
        });
    }
};

// Iniciar
if (typeof apiFetch !== 'undefined') {
    CMSPWA.init();
} else {
    window.addEventListener('load', () => CMSPWA.init());
}
