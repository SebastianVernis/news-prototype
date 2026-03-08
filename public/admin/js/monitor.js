// Monitor de Sistema - Dashboard Ingesta + Facebook + Cron
async function initMonitor() {
  console.log("[Monitor] Iniciando controlador...");
  await loadCronStatus();
  await checkFBTokens();
  await loadFBMonitorHistory();
}

/**
 * Carga el estado del último cron automático desde KV vía API.
 */
async function loadCronStatus() {
  const list = document.getElementById("cron-tasks-list");
  const lastRunEl = document.getElementById("cron-last-run");
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

    list.innerHTML = Object.entries(data.tasks)
      .map(([task, status]) => {
        const isOk = status.includes("OK");
        return `
                <div class="status-item ${isOk ? "status-item--ok" : "status-item--err"}">
                    <span class="status-item-name">${task.replace(/_/g, " ")}:</span>
                    <span class="${isOk ? "badge-ok" : "badge-err"}">${status}</span>
                </div>
            `;
      })
      .join("");
  } catch (e) {
    list.innerHTML = `<p class="monitor-error"><i class="fas fa-exclamation-circle"></i> Error: ${e.message}</p>`;
  }
}

/**
 * Verifica si los tokens de los sitios están presentes en los secretos.
 */
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

    list.innerHTML = tokens
      .map(
        (t) => `
            <div class="token-item">
                <span class="token-item-slug">${t.slug}</span>
                ${
                  t.is_valid
                    ? '<i class="fas fa-check-circle token-ok" title="Token Válido"></i>'
                    : t.has_token
                    ? `<i class="fas fa-exclamation-circle token-warn" title="Error de validación: ${t.fb_error || 'Token expirado'}"></i>`
                    : '<i class="fas fa-times-circle token-err" title="Falta Token"></i>'
                }
            </div>
        `,
      )
      .join("");
  } catch (e) {
    list.innerHTML = `<p class="monitor-error" style="grid-column: 1 / -1"><i class="fas fa-exclamation-circle"></i> Error de diagnóstico: ${e.message}</p>`;
  }
}

/**
 * Carga el historial de envíos unificado (Facebook Monitor).
 */
async function loadFBMonitorHistory() {
  const tbody = document.getElementById("monitor-fb-table-body");
  if (!tbody) return;

  // Skeleton mientras carga
  if (window.showTableSkeleton) {
    showTableSkeleton(tbody, 4, 5);
  } else {
    tbody.innerHTML =
      '<tr><td colspan="4" class="monitor-empty">Cargando historial...</td></tr>';
  }

  try {
    const fbArticles = await apiFetch("/facebook/monitor");

    if (!fbArticles || fbArticles.length === 0) {
      tbody.innerHTML =
        '<tr><td colspan="4" class="monitor-empty">No hay registros.</td></tr>';
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
                <td class="monitor-article-sites">${a.SITIOS_DESTINO || "-"}</td>
                <td style="white-space: nowrap; width: 120px;">
                    ${
                      a.FB_PUBLICADO === 1
                        ? '<span class="monitor-badge monitor-badge--published"><i class="fas fa-check"></i> Publicado</span>'
                        : '<span class="monitor-badge monitor-badge--pending"><i class="fas fa-clock"></i> Pendiente</span>'
                    }
                </td>
                <td class="monitor-article-date">
                    ${a.FB_FECHA ? new Date(a.FB_FECHA).toLocaleString("es") : "En proceso..."}
                </td>
            </tr>
        `,
      )
      .join("");
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="4" class="monitor-error"><i class="fas fa-exclamation-circle"></i> Error: ${e.message}</td></tr>`;
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
