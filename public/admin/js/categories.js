async function initCategories() {
    await loadCategoriesTable();
}

async function loadCategoriesTable() {
    const tbody = document.getElementById('categories-master-table');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:1rem;">Cargando...</td></tr>';
    try {
        const categories = await apiFetch('/categories');
        if (!categories || categories.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:1.5rem; color:#888;">No hay categorías. Crea la primera con el botón "Nueva Categoría".</td></tr>';
            return;
        }
        tbody.innerHTML = categories.map(c => `
            <tr>
                <td><strong>${c.NOMBRE}</strong></td>
                <td><code style="background:#f0f0f0; padding:2px 6px; border-radius:3px;">${c.SLUG}</code></td>
                <td class="actions">
                    <button class="btn btn-outline" title="Editar" onclick="editCategory('${c.ID}', '${c.NOMBRE}')">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="3" style="color:red;">Error: ${e.message}</td></tr>`;
    }
}

function showNewCategoryModal() {
    const modal = document.getElementById('category-modal');
    if (modal) {
        modal.style.display = 'flex';
        const input = document.getElementById('new-category-name');
        if (input) { input.value = ''; input.focus(); }
    }
}

function closeCategoryModal() {
    const modal = document.getElementById('category-modal');
    if (modal) modal.style.display = 'none';
}

async function createCategory() {
    const input = document.getElementById('new-category-name');
    const nombre = (input?.value || '').trim();
    if (!nombre) return alert('Ingresa un nombre para la categoría.');

    const btn = document.querySelector('#category-modal .btn-primary');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando...'; }

    try {
        await apiFetch('/categories', {
            method: 'POST',
            body: JSON.stringify({ nombre })
        });
        closeCategoryModal();
        await loadCategoriesTable();
    } catch (e) {
        alert('Error al crear categoría: ' + e.message);
    } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-save"></i> Crear Categoría'; }
    }
}

function editCategory(id, nombre) {
    const nuevo = prompt('Editar nombre de categoría:', nombre);
    if (!nuevo || nuevo.trim() === nombre) return;
    alert('Edición de categorías próximamente disponible.');
}
