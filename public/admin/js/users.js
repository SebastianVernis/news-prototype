// users.js - Gestión de Usuarios y Generación de Links de Contraseña

const UsersModule = (function () {
    const API_BASE = window.ADMIN_API_BASE_URL || 'https://news-api.sebastianvernis.workers.dev/api';

    // Obtener token de autenticación
    function getAuthToken() {
        return localStorage.getItem('adminToken') || sessionStorage.getItem('adminToken');
    }

    // Renderizar la vista de usuarios
    function render() {
        loadUsers();
    }

    // Cargar lista de usuarios
    async function loadUsers() {
        const loading = document.getElementById('users-loading');
        const error = document.getElementById('users-error');
        const tableWrap = document.getElementById('users-table-wrap');
        const tbody = document.getElementById('users-tbody');

        try {
            const users = await apiFetch('/auth/users');

            loading.style.display = 'none';
            tableWrap.style.display = 'block';

            if (users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;">No hay usuarios registrados</td></tr>';
                return;
            }

            tbody.innerHTML = users.map(user => `
                <tr>
                    <td><strong>${escapeHtml(user.NOMBRE || user.username || '')}</strong></td>
                    <td>${escapeHtml(user.EMAIL || user.email || '—')}</td>
                    <td><span class="badge badge-${(user.ROL || user.role || 'editor').toLowerCase()}">${escapeHtml(user.ROL || user.role || 'Editor')}</span></td>
                    <td>${user.ACTIVO ? '✓ Activo' : '✗ Inactivo'}</td>
                    <td>
                        <button class="btn-sm btn-link" onclick="UsersModule.openGenerateLink('${escapeHtml(user.NOMBRE || user.username || '')}')">
                            <i class="fas fa-key"></i> Generar Link
                        </button>
                    </td>
                </tr>
            `).join('');

        } catch (err) {
            loading.style.display = 'none';
            error.style.display = 'block';
            error.textContent = err.message || 'Error al cargar usuarios';
        }
    }

    // Abrir modal para generar link
    function openGenerateLink(username = '') {
        const modal = document.getElementById('generate-link-modal');
        const input = document.getElementById('gl-username');
        
        input.value = username;
        modal.style.display = 'flex';
        
        // Resetear estados
        document.getElementById('gl-loading').style.display = 'none';
        document.getElementById('gl-error').style.display = 'none';
        document.getElementById('gl-success').style.display = 'none';
        document.getElementById('gl-link-wrap').style.display = 'none';
        document.getElementById('gl-footer').style.display = 'flex';
    }

    // Cerrar modal
    function closeGenerateLink() {
        const modal = document.getElementById('generate-link-modal');
        modal.style.display = 'none';
    }

    // Generar link
    async function doGenerateLink() {
        const username = document.getElementById('gl-username').value.trim();
        
        if (!username) {
            alert('Por favor selecciona un usuario');
            return;
        }

        const loading = document.getElementById('gl-loading');
        const error = document.getElementById('gl-error');
        const success = document.getElementById('gl-success');
        const linkWrap = document.getElementById('gl-link-wrap');
        const linkDisplay = document.getElementById('gl-link-display');
        const footer = document.getElementById('gl-footer');

        loading.style.display = 'block';
        error.style.display = 'none';
        success.style.display = 'none';
        linkWrap.style.display = 'none';
        footer.style.display = 'none';

        try {
            const data = await apiFetch('/auth/generate-password-token', {
                method: 'POST',
                body: JSON.stringify({ username })
            });

            loading.style.display = 'none';
            success.style.display = 'block';
            linkWrap.style.display = 'block';
            linkDisplay.textContent = data.setupUrl;

        } catch (err) {
            loading.style.display = 'none';
            footer.style.display = 'flex';
            error.style.display = 'block';
            error.textContent = err.message || 'Error al generar el link';
        }
    }

    // Copiar link
    async function copyLink() {
        const link = document.getElementById('gl-link-display').textContent;
        
        try {
            await navigator.clipboard.writeText(link);
            alert('Link copiado al portapapeles');
        } catch (err) {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = link;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Link copiado al portapapeles');
        }
    }

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Exportar funciones públicas
    return {
        render,
        loadUsers,
        openGenerateLink,
        closeGenerateLink,
        doGenerateLink,
        copyLink
    };
})();

// Hacer disponible globalmente
window.UsersModule = UsersModule;
