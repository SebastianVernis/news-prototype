/**
 * NexoPress PWA Manager - Client Side
 * Gestiona registro de SW y respaldo local de datos
 */
const PWAManager = {
    DB_NAME: 'NexoPress_LocalData',
    STORE_NAME: 'articles',
    UPDATE_INTERVAL: 30 * 60 * 1000, // 30 minutos

    async init() {
        console.log('[PWA] Iniciando Manager...');
        this.registerSW();
        await this.setupDataBackup();
    },

    registerSW() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js')
                    .then(reg => console.log('[PWA] Service Worker registrado', reg.scope))
                    .catch(err => console.error('[PWA] Error al registrar SW', err));
            });
        }
    },

    async setupDataBackup() {
        // Ejecutar primera actualización
        await this.refreshLocalData();
        
        // Programar actualizaciones cada 30 min
        setInterval(() => this.refreshLocalData(), this.UPDATE_INTERVAL);
    },

    async refreshLocalData() {
        const container = document.querySelector('#featured-container');
        const apiUrl = container?.dataset.api || '/api/articles?limit=12';
        
        try {
            console.log('[PWA] Actualizando respaldo local desde API...');
            const res = await fetch(apiUrl);
            if (!res.ok) throw new Error('API Offline');
            const data = await res.json();
            
            if (data.articles) {
                await this.saveToLocal(data.articles);
                console.log('[PWA] Respaldo local actualizado:', data.articles.length, 'artículos');
                
                // Disparar evento para que la UI se actualice si es necesario
                window.dispatchEvent(new CustomEvent('articlesUpdated', { detail: data.articles }));
            }
        } catch (e) {
            console.warn('[PWA] No se pudo actualizar de la API, usando datos locales:', e.message);
        }
    },

    async saveToLocal(articles) {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, 1);
            
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains(this.STORE_NAME)) {
                    db.createObjectStore(this.STORE_NAME, { keyPath: 'id' });
                }
            };

            request.onsuccess = (e) => {
                const db = e.target.result;
                const tx = db.transaction(this.STORE_NAME, 'readwrite');
                const store = tx.objectStore(this.STORE_NAME);
                
                articles.forEach(art => store.put(art));
                tx.oncomplete = () => resolve();
            };

            request.onerror = () => reject(request.error);
        });
    },

    async getLocalArticles() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, 1);
            request.onsuccess = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains(this.STORE_NAME)) return resolve([]);
                
                const tx = db.transaction(this.STORE_NAME, 'readonly');
                const store = tx.objectStore(this.STORE_NAME);
                const getReq = store.getAll();
                getReq.onsuccess = () => resolve(getReq.result);
            };
            request.onerror = () => resolve([]);
        });
    }
};

// Iniciar manager
PWAManager.init();
