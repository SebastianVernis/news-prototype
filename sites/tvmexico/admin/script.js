/* ========================================
   TV México - Admin CMS Script
   ======================================== */

const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8781/api' : '/api';
const STORAGE_KEY = 'cms_articles_tvmexico';
const TOKEN_KEY = 'cms_token_tvmexico';
const SESSION_KEY = 'cms_session_tvmexico';

let articles = [];
let currentToken = '';

// ===== INIT =====
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    loadArticles();
    setupEventListeners();
});

// ===== AUTH =====
async function checkAuth() {
    const session = sessionStorage.getItem(SESSION_KEY);
    if (!session) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const token = sessionStorage.getItem(TOKEN_KEY);
        if (!token || token.length !== 64) {
            throw new Error('Token inválido');
        }
        currentToken = token;
        document.getElementById('auth-check').style.display = 'none';
        document.getElementById('admin-app').style.display = 'flex';
        displayToken();
    } catch (error) {
        console.error('Auth error:', error);
        window.location.href = 'login.html';
    }
}

function displayToken() {
    const tokenDisplay = document.getElementById('current-token');
    if (tokenDisplay) {
        tokenDisplay.textContent = currentToken.substring(0, 32) + '...';
    }
}

async function logout() {
    sessionStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(TOKEN_KEY);
    window.location.href = 'login.html';
}

// ===== NAVIGATION =====
function showView(viewName) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.view === viewName) {
            item.classList.add('active');
        }
    });

    // Update views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById('view-' + viewName).classList.add('active');

    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'articles': 'Artículos',
        'new-article': 'Crear Artículo',
        'categories': 'Categorías',
        'settings': 'Configuración'
    };
    document.getElementById('page-title').textContent = titles[viewName] || 'Dashboard';

    // Refresh data based on view
    if (viewName === 'articles') {
        renderArticlesTable();
    } else if (viewName === 'dashboard') {
        updateDashboard();
    } else if (viewName === 'categories') {
        updateCategories();
    } else if (viewName === 'new-article') {
        resetArticleForm();
    }
}

// ===== ARTICLES CRUD =====
function loadArticles() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
        articles = JSON.parse(stored);
    } else {
        // Sample articles
        articles = [
            {
                id: '1',
                title: 'Informe especial: El futuro de la tecnología en México',
                slug: 'informe-especial-tecnologia',
                excerpt: 'Un análisis profundo sobre cómo la innovación está transformando diversos sectores del país',
                content: 'El panorama tecnológico en México ha experimentado una transformación sin precedentes...',
                category: 'nacional',
                author: 'Redacción',
                imageUrl: 'https://placehold.co/800x500/004a99/ffffff?text=Tecnologia',
                status: 'published',
                featured: true,
                tags: ['tecnología', 'innovación', 'méxico'],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            }
        ];
        saveArticles();
    }
    updateDashboard();
}

function saveArticles() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(articles));
    updateDashboard();
}

function renderArticlesTable() {
    const tbody = document.getElementById('articles-body');
    if (!tbody) return;

    const searchTerm = document.getElementById('search-articles')?.value.toLowerCase() || '';
    const filtered = articles.filter(a => 
        a.title.toLowerCase().includes(searchTerm) ||
        a.category.toLowerCase().includes(searchTerm)
    );

    tbody.innerHTML = filtered.map(article => `
        <tr>
            <td>
                <strong>${article.title}</strong>
                <br><small style="color: #999;">${article.slug}</small>
            </td>
            <td><span class="badge badge-${getCategoryColor(article.category)}">${article.category}</span></td>
            <td>${article.author}</td>
            <td>
                <span class="badge badge-${article.status === 'published' ? 'success' : 'warning'}">
                    ${article.status === 'published' ? 'Publicado' : 'Borrador'}
                </span>
            </td>
            <td>${formatDate(article.createdAt)}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" onclick="editArticle('${article.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" onclick="deleteArticle('${article.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderRecentArticles() {
    const tbody = document.getElementById('recent-articles-body');
    if (!tbody) return;

    const recent = articles.slice(-5).reverse();
    tbody.innerHTML = recent.map(article => `
        <tr>
            <td><strong>${article.title}</strong></td>
            <td><span class="badge badge-${getCategoryColor(article.category)}">${article.category}</span></td>
            <td>
                <span class="badge badge-${article.status === 'published' ? 'success' : 'warning'}">
                    ${article.status === 'published' ? 'Publicado' : 'Borrador'}
                </span>
            </td>
            <td>${formatDate(article.createdAt)}</td>
            <td>
                <div class="table-actions">
                    <button class="btn-edit" onclick="editArticle('${article.id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" onclick="deleteArticle('${article.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function editArticle(id) {
    const article = articles.find(a => a.id === id);
    if (!article) return;

    document.getElementById('article-id').value = article.id;
    document.getElementById('article-title').value = article.title;
    document.getElementById('article-slug').value = article.slug;
    document.getElementById('article-excerpt').value = article.excerpt || '';
    document.getElementById('article-content').value = article.content;
    document.getElementById('article-category').value = article.category;
    document.getElementById('article-author').value = article.author || '';
    document.getElementById('article-image').value = article.imageUrl || '';
    document.getElementById('article-tags').value = article.tags?.join(', ') || '';
    document.getElementById('article-status').value = article.status;
    document.getElementById('article-featured').checked = article.featured || false;

    document.getElementById('article-form-title').textContent = 'Editar Artículo';
    document.getElementById('btn-delete').style.display = 'block';

    showView('new-article');
}

function deleteArticle(id) {
    if (!confirm('¿Está seguro de eliminar este artículo?')) return;
    
    articles = articles.filter(a => a.id !== id);
    saveArticles();
    renderArticlesTable();
    updateDashboard();
    showToast('Artículo eliminado correctamente', 'success');
}

function resetArticleForm() {
    document.getElementById('article-form').reset();
    document.getElementById('article-id').value = '';
    document.getElementById('article-form-title').textContent = 'Crear Nuevo Artículo';
    document.getElementById('btn-delete').style.display = 'none';
    generateSlug();
}

function generateSlug() {
    const title = document.getElementById('article-title').value;
    const slugInput = document.getElementById('article-slug');
    
    if (!slugInput.value || slugInput.value === 'se-genera-automaticamente') {
        const slug = title
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '');
        slugInput.value = slug;
    }
}

// ===== DASHBOARD =====
function updateDashboard() {
    const total = articles.length;
    const published = articles.filter(a => a.status === 'published').length;
    const drafts = articles.filter(a => a.status === 'draft').length;

    document.getElementById('total-articles').textContent = total;
    document.getElementById('published-articles').textContent = published;
    document.getElementById('draft-articles').textContent = drafts;

    renderRecentArticles();
}

function updateCategories() {
    const categories = {};
    articles.forEach(a => {
        categories[a.category] = (categories[a.category] || 0) + 1;
    });

    ['nacional', 'politica', 'economia', 'deportes'].forEach(cat => {
        const el = document.getElementById('cat-' + cat + '-count');
        if (el) {
            el.textContent = (categories[cat] || 0) + ' artículos';
        }
    });
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            showView(item.dataset.view);
        });
    });

    // Logout
    document.getElementById('logout-btn')?.addEventListener('click', logout);

    // Article form
    document.getElementById('article-form')?.addEventListener('submit', handleArticleSubmit);

    // Slug generation
    document.getElementById('article-title')?.addEventListener('input', generateSlug);

    // Search
    document.getElementById('search-articles')?.addEventListener('input', renderArticlesTable);
}

function handleArticleSubmit(e) {
    e.preventDefault();

    const id = document.getElementById('article-id').value;
    const article = {
        id: id || Date.now().toString(),
        title: document.getElementById('article-title').value,
        slug: document.getElementById('article-slug').value,
        excerpt: document.getElementById('article-excerpt').value,
        content: document.getElementById('article-content').value,
        category: document.getElementById('article-category').value,
        author: document.getElementById('article-author').value,
        imageUrl: document.getElementById('article-image').value,
        tags: document.getElementById('article-tags').value.split(',').map(t => t.trim()).filter(t => t),
        status: document.getElementById('article-status').value,
        featured: document.getElementById('article-featured').checked,
        createdAt: id ? articles.find(a => a.id === id)?.createdAt : new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };

    if (id) {
        const index = articles.findIndex(a => a.id === id);
        articles[index] = article;
        showToast('Artículo actualizado correctamente', 'success');
    } else {
        articles.push(article);
        showToast('Artículo creado correctamente', 'success');
    }

    saveArticles();
    showView('articles');
}

// ===== UTILS =====
function getCategoryColor(category) {
    const colors = {
        'nacional': 'danger',
        'politica': 'info',
        'economia': 'success',
        'deportes': 'warning',
        'cultura': 'info',
        'tecnologia': 'success'
    };
    return colors[category] || 'info';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-MX', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show ' + type;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function regenerateToken() {
    if (!confirm('¿Está seguro de regenerar el token? El token anterior dejará de funcionar.')) return;
    
    const newToken = generateToken();
    sessionStorage.setItem(TOKEN_KEY, newToken);
    currentToken = newToken;
    displayToken();
    showToast('Token regenerado correctamente', 'success');
}

function generateToken() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, b => b.toString(16).padStart(2, '0')).join('');
}

function exportArticles() {
    const data = JSON.stringify(articles, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'articles-export.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Artículos exportados correctamente', 'success');
}

// Expose functions globally
window.showView = showView;
window.editArticle = editArticle;
window.deleteArticle = deleteArticle;
window.regenerateToken = regenerateToken;
window.exportArticles = exportArticles;
