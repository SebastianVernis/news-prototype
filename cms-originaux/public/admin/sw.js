/**
 * NexoPress CMS Service Worker
 */
const CACHE_NAME = 'nexopress-cms-v2';
const ASSETS = [
    './',
    './index.html',
    './css/admin.css',
    './js/api.js',
    './js/auth.js',
    './js/router.js',
    './js/dashboard.js',
    './js/articles.js',
    './js/cms.js',
    './js/facebook.js',
    './js/monitor.js',
    './assets/logo.png',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
        ))
    );
});

self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;

    // Estrategia para API: Network First
    if (e.request.url.includes('/api/')) {
        e.respondWith(
            fetch(e.request)
                .catch(() => caches.match(e.request))
        );
        return;
    }

    // Estrategia para Activos: Cache First
    e.respondWith(
        caches.match(e.request).then(res => res || fetch(e.request))
    );
});
