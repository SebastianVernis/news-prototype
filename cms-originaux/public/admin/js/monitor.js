// Monitor de Sistema - Dashboard Ingesta + Cron
async function initMonitor() {
  console.log("[Monitor] Iniciando controlador...");
  await loadCronStatus();
  await checkFBTokens();
}

/**
 * Carga el estado del último cron automático desde KV vía API.
 */
async function loadCronStatus() {
  const list = document.getElementById("cron-tasks-list");
  const lastRunEl = document.getElementById("cron-last-run");
  const lastIngestEl = document.getElementById("last-ingest-time");
  if (!list) return;

  try {
    const data = await apiFetch("/cron/status");
    if (!data || !data.tasks) {
      list.innerHTML =
        '<p class="monitor-empty">No hay registros de ejecución previa.</p>';
      return;
    }

    if (lastRunEl) {
      lastRunEl.textContent = new Date(data.lastRun).toLocaleString("es");
    }
    
    if (lastIngestEl) {
      lastIngestEl.textContent = new Date(data.lastRun).toLocaleTimeString("es");
    }

    list.innerHTML = Object.entries(data.tasks)
      .map(([task, status]) => {
        const isOk = status.includes("OK");
        let taskIcon = '⚙️';
        let taskLabel = task.replace(/_/g, " ");
        
        if (task === 'ingest') {
          taskIcon = '📥';
          taskLabel = 'RSS Ingesta';
        } else if (task === 'fb') {
          taskIcon = '📘';
          taskLabel = 'Facebook Timer';
        } else if (task === 'ticker') {
          taskIcon = '📰';
          taskLabel = 'Ticker';
        }
        
        return `
                <div class="status-item ${isOk ? "status-item--ok" : "status-item--err"}">
                    <span class="status-item-name">${taskIcon} ${taskLabel}:</span>
                    <span class="${isOk ? "badge-ok" : "badge-err"}">${status}</span>
                </div>
            `;
      })
      .join("");
      
    // Auto-refresh cada 30 segundos
    setTimeout(loadCronStatus, 30000);
  } catch (e) {
    list.innerHTML = `<p class="monitor-error"><i class="fas fa-exclamation-circle"></i> Error: ${e.message}</p>`;
  }
}

/**
 * Verifica si los tokens de los sitios están presentes en los secretos.
 * Con paginación para manejar 27 sitios.
 */
let tokenPage = 1;
const tokensPerPage = 10;
let allTokens = [];

async function checkFBTokens() {
  const list = document.getElementById("token-status-list");
  if (!list) return;

  try {
    list.innerHTML =
      '<p class="monitor-empty" style="grid-column: 1 / -1">Diagnosticando...</p>';
    const tokens = await apiFetch("/facebook/debug-tokens");

    if (!tokens || tokens.length === 0) {
      list.innerHTML =
        '<p class="monitor-empty" style="grid-column: 1 / -1">No se encontraron sitios.</p>';
      return;
    }

    allTokens = tokens;
    renderTokenPage(1);
  } catch (e) {
    list.innerHTML = `<p class="monitor-error" style="grid-column: 1 / -1"><i class="fas fa-exclamation-circle"></i> Error de diagnóstico: ${e.message}</p>`;
  }
}

function renderTokenPage(page) {
  const list = document.getElementById("token-status-list");
  if (!list || !allTokens.length) return;

  tokenPage = page;
  const totalPages = Math.ceil(allTokens.length / tokensPerPage);
  const start = (page - 1) * tokensPerPage;
  const end = start + tokensPerPage;
  const pageTokens = allTokens.slice(start, end);

  list.innerHTML = pageTokens
    .map(
      (t) => `
            <div class="token-item">
                <span class="token-item-slug">${t.slug}</span>
                ${
                  t.is_valid
                    ? '<i class="fas fa-check-circle token-ok" title="Token Válido"></i>'
                    : t.has_token
                    ? `<i class="fas fa-exclamation-circle token-warn" title="Error: ${t.fb_error || 'Token expirado'}"></i>`
                    : '<i class="fas fa-times-circle token-err" title="Falta Token"></i>'
                }
            </div>
        `,
    )
    .join("");

  // Agregar controles de paginación
  const pagination = document.getElementById("token-pagination");
  if (pagination) {
    pagination.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
        <small style="color: var(--text-secondary); font-size: 0.85rem;">
          Mostrando ${start + 1}-${Math.min(end, allTokens.length)} de ${allTokens.length} sitios
        </small>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <button class="btn btn-outline btn-sm" onclick="prevTokenPage()" ${page === 1 ? 'disabled' : ''}>
            <i class="fas fa-chevron-left"></i> Anterior
          </button>
          <span style="font-size: 0.85rem; color: var(--text-secondary);">
            Página ${page} de ${totalPages}
          </span>
          <button class="btn btn-outline btn-sm" onclick="nextTokenPage()" ${page === totalPages ? 'disabled' : ''}>
            Siguiente <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    `;
  }
}

function prevTokenPage() {
  if (tokenPage > 1) renderTokenPage(tokenPage - 1);
}

function nextTokenPage() {
  const totalPages = Math.ceil(allTokens.length / tokensPerPage);
  if (tokenPage < totalPages) renderTokenPage(tokenPage + 1);
}

/**
 * Carga el historial de envíos unificado (Facebook Monitor) - Nuevo sistema por sitio
 */
async function loadFBMonitorHistory() {
  const tbody = document.getElementById("monitor-fb-table-body");
  if (!tbody) return;

  // Skeleton mientras carga
  if (window.showTableSkeleton) {
    showTableSkeleton(tbody, 4, 5);
  } else {
    tbody.innerHTML =
      '<tr><td colspan="5" class="monitor-empty">Cargando historial...</td></tr>';
  }

  try {
    const fbArticles = await apiFetch("/facebook/monitor");

    if (!fbArticles || fbArticles.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="5" class="monitor-empty">No hay registros.</td></tr>';
      return;
    }

    tbody.innerHTML = fbArticles
      .map(
        (a) => `
            <tr>
                <td>
                    <small class="monitor-article-type">[${a.TIPO || "ART"}]</small>
                    <div class="monitor-article-title">${a.TITULO}</div>
                </td>
                <td>
                    <span class="badge-info" style="font-size:0.7rem; background:rgba(6,182,212,0.1); color:var(--primary-color); padding:2px 6px; border-radius:4px;">
                        ${a.SITIO || '-'}
                    </span>
                </td>
                <td style="white-space: nowrap; width: 120px;">
                    <span class="monitor-badge monitor-badge--published"><i class="fas fa-check"></i> Web</span>
                </td>
                <td style="white-space: nowrap; width: 120px;">
                    ${
                      a.FB_PUBLICADO === 1
                        ? '<span class="monitor-badge monitor-badge--published"><i class="fas fa-facebook"></i> FB</span>'
                        : '<span class="monitor-badge monitor-badge--pending"><i class="fas fa-clock"></i> FB</span>'
                    }
                </td>
                <td class="monitor-article-date">
                    ${a.FECHA_PUBLICACION ? new Date(a.FECHA_PUBLICACION).toLocaleString("es") : '-'}
                </td>
            </tr>
        `,
      )
      .join("");
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="5" class="monitor-error"><i class="fas fa-exclamation-circle"></i> Error: ${e.message}</td></tr>`;
  }
}

/**
 * Dispara manualmente la ingesta de noticias.
 */
async function triggerManualIngest() {
  const btn = document.getElementById("btn-manual-ingest");
  if (!btn) return;

  if (
    !confirm(
      "Esto ejecutará el proceso de búsqueda de noticias (RSS/Atom) ahora mismo. ¿Continuar?",
    )
  )
    return;

  const originalHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML =
    '<i class="fas fa-spinner fa-spin"></i> Ejecutando ingesta...';

  try {
    const res = await apiFetch("/cron/ingest", { method: "POST" });
    if (res.success) {
      if (typeof showSuccessToast === 'function') {
        showSuccessToast('Ingesta Completada', `Se importaron ${res.count} artículos nuevos`, 4000);
      }
      await loadCronStatus();
      await loadFBMonitorHistory();
    } else {
      const msg = res.error || "Ocurrió un problema durante la ingesta.";
      if (typeof showErrorToast === 'function') {
        showErrorToast('Error en Ingesta', msg, 5000);
      }
    }
  } catch (e) {
    if (typeof showErrorToast === 'function') {
      showErrorToast('Error Técnico', e.message, 5000);
    }
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}
