async function initCategories() {
    await loadCategoriesTable();
}

async function loadCategoriesTable() {
    const tbody = document.getElementById('categories-master-table');
    tbody.innerHTML = '<tr><td colspan="3">Cargando...</td></tr>';
    try {
        const categories = await apiFetch('/categories');
        tbody.innerHTML = categories.map(c => `
            <tr>
                <td>${c.NOMBRE}</td>
                <td>${c.SLUG}</td>
                <td class="actions">
                    <button class="btn btn-outline"><i class="fas fa-edit"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="3">Error: ${e.message}</td></tr>`;
    }
}
