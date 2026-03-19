/**
 * NexoPress Service Worker
 * Proporciona capacidades offline y cache de activos
 */
const CACHE_NAME = 'nexopress-v1';
const ASSETS = [
    './',
    './index.html',
    './style.css',
    './style-custom.css',
    './script.js',
    './components.js',
    './pwa-manager.js',
    './manifest.json',
    './logo-header.png',
    './logo.png'
];

// Instalación: Cachear activos estáticos
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
});

// Activación: Limpiar caches antiguos
self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
        ))
    );
});

// Estrategia: Network First, Fallback to Cache
self.addEventListener('fetch', (e) => {
    // Solo manejar peticiones GET
    if (e.request.method !== 'GET') return;

    // Para la API de artículos, intentamos red primero para tener lo último
    if (e.request.url.includes('/api/articles')) {
        e.respondWith(
            fetch(e.request)
                .catch(() => caches.match(e.request))
        );
        return;
    }

    // Para activos estáticos, Cache First
    e.respondWith(
        caches.match(e.request).then(response => {
            return response || fetch(e.request);
        })
    );
});
