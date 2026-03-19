/**
 * NexoPress CMS — Animations & UI Utilities
 *
 * Incluye:
 *  - Toast notification system (global window.Toast)
 *  - Animated counter for dashboard stats (window.animateCounter)
 *  - Animated editor open/close helpers (window.openEditorAnimated / closeEditorAnimated)
 *  - Ripple helper callable externally (window.applyRipple)
 *  - Scroll-reveal for cards/rows (IntersectionObserver)
 */

/* ═══════════════════════════════════════════════════════
   TOAST SYSTEM
═══════════════════════════════════════════════════════ */
const Toast = (() => {
    const ICONS = {
        success: 'fas fa-check-circle',
        error:   'fas fa-times-circle',
        info:    'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle',
    };
    const DEFAULT_DURATION = 4000;

    /** Obtiene o crea el contenedor de toasts */
    function getContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    /**
     * Muestra un toast.
     * @param {string} message  Texto del mensaje
     * @param {'success'|'error'|'info'|'warning'} type
     * @param {number} duration  Ms antes de auto-cerrar (0 = permanente)
     */
    function show(message, type = 'info', duration = DEFAULT_DURATION) {
        const container = getContainer();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');

        toast.innerHTML = `
            <i class="${ICONS[type] || ICONS.info}" aria-hidden="true"></i>
            <span class="toast-message">${message}</span>
            <button class="toast-close" aria-label="Cerrar notificación">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Botón cerrar
        toast.querySelector('.toast-close').addEventListener('click', () => {
            dismiss(toast);
        });

        container.appendChild(toast);

        // Auto-cerrar
        if (duration > 0) {
            setTimeout(() => dismiss(toast), duration);
        }

        return toast;
    }

    /** Anima la salida y elimina el toast */
    function dismiss(toast) {
        if (!toast || !toast.parentNode) return;
        toast.classList.add('toast-out');
        toast.addEventListener('animationend', () => {
            toast.remove();
        }, { once: true });
    }

    /** Cierra todos los toasts activos */
    function dismissAll() {
        document.querySelectorAll('.toast').forEach(dismiss);
    }

    return {
        show,
        dismiss,
        dismissAll,
        success: (msg, dur) => show(msg, 'success', dur),
        error:   (msg, dur) => show(msg, 'error',   dur),
        info:    (msg, dur) => show(msg, 'info',     dur),
        warning: (msg, dur) => show(msg, 'warning',  dur),
    };
})();

// Exponer globalmente
window.Toast = Toast;


/* ═══════════════════════════════════════════════════════
   ANIMATED COUNTER (dashboard stats)
═══════════════════════════════════════════════════════ */

/**
 * Anima el número en un elemento desde 0 hasta `target`.
 * @param {HTMLElement|string} elOrId  Elemento o su id
 * @param {number}  target   Valor final
 * @param {number}  duration Duración en ms (default 900)
 * @param {string}  [suffix] Sufijo opcional (ej: '%', 'k')
 */
function animateCounter(elOrId, target, duration = 900, suffix = '') {
    const el = typeof elOrId === 'string'
        ? document.getElementById(elOrId)
        : elOrId;

    if (!el) return;

    const start     = performance.now();
    const startVal  = 0;
    const endVal    = Number(target) || 0;

    // Clase de animación pop
    el.classList.add('stat-value-animated');
    el.addEventListener('animationend', () => {
        el.classList.remove('stat-value-animated');
    }, { once: true });

    function step(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease-out cubic
        const eased    = 1 - Math.pow(1 - progress, 3);
        const current  = Math.round(startVal + (endVal - startVal) * eased);

        el.textContent = current.toLocaleString('es') + suffix;

        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            el.textContent = endVal.toLocaleString('es') + suffix;
        }
    }

    requestAnimationFrame(step);
}

window.animateCounter = animateCounter;


/* ═══════════════════════════════════════════════════════
   EDITOR OVERLAY — Abrir / cerrar animado
═══════════════════════════════════════════════════════ */

/**
 * Abre el editor universal con animación.
 * Llama a la función openUniversalEditor original si existe,
 * luego aplica las clases CSS de entrada.
 */
function openEditorAnimated() {
    const overlay = document.getElementById('universal-editor-view');
    if (!overlay) return;

    overlay.style.display = 'block';
    // Forzar reflow antes de añadir la clase
    void overlay.offsetWidth;
    overlay.classList.add('editor-visible');

    // Bloquear scroll del body
    document.body.style.overflow = 'hidden';
}

/**
 * Cierra el editor universal con animación de salida.
 * @param {Function} [onClosed]  Callback tras completar la animación
 */
function closeEditorAnimated(onClosed) {
    const overlay = document.getElementById('universal-editor-view');
    if (!overlay) return;

    // Animación de salida: invertir overlay-in
    overlay.style.transition = 'opacity 0.2s ease';
    overlay.style.opacity    = '0';

    overlay.addEventListener('transitionend', () => {
        overlay.style.display     = 'none';
        overlay.style.opacity     = '';
        overlay.style.transition  = '';
        overlay.classList.remove('editor-visible');
        document.body.style.overflow = '';
        if (typeof onClosed === 'function') onClosed();
    }, { once: true });
}

window.openEditorAnimated  = openEditorAnimated;
window.closeEditorAnimated = closeEditorAnimated;


/* ═══════════════════════════════════════════════════════
   RIPPLE — helper externo
═══════════════════════════════════════════════════════ */

/**
 * Aplica el efecto ripple a un elemento en la posición del evento.
 * Útil para botones generados dinámicamente.
 * @param {HTMLElement} el
 * @param {MouseEvent|PointerEvent} e
 */
function applyRipple(el, e) {
    if (!el || el.disabled) return;

    const rect = el.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 2;
    const x    = (e.clientX - rect.left) - size / 2;
    const y    = (e.clientY - rect.top)  - size / 2;

    const span = document.createElement('span');
    span.classList.add('ripple');
    span.style.cssText = `
        width:  ${size}px;
        height: ${size}px;
        left:   ${x}px;
        top:    ${y}px;
    `;

    el.appendChild(span);
    span.addEventListener('animationend', () => span.remove(), { once: true });
}

window.applyRipple = applyRipple;


/* ═══════════════════════════════════════════════════════
   SCROLL REVEAL — tarjetas y filas de tabla
═══════════════════════════════════════════════════════ */

(function initScrollReveal() {
    // Solo si el browser soporta IntersectionObserver
    if (!window.IntersectionObserver) return;

    const REVEAL_CLASS = 'scroll-reveal';
    const VISIBLE_CLASS = 'scroll-visible';

    // Inyectar estilos mínimos de reveal
    const style = document.createElement('style');
    style.textContent = `
        .${REVEAL_CLASS} {
            opacity: 0;
            transform: translateY(18px);
            transition:
                opacity  0.4s cubic-bezier(0.4,0,0.2,1),
                transform 0.4s cubic-bezier(0.4,0,0.2,1);
        }
        .${REVEAL_CLASS}.${VISIBLE_CLASS} {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add(VISIBLE_CLASS);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px',
    });

    /**
     * Registra todos los .card dentro de `scope` para scroll-reveal.
     * Se llama también desde el Router tras cargar una vista.
     */
    function observe(scope = document) {
        scope.querySelectorAll('.card').forEach((card, i) => {
            if (card.classList.contains(REVEAL_CLASS)) return;
            card.classList.add(REVEAL_CLASS);
            // Retraso escalonado para grupos de cards
            card.style.transitionDelay = `${Math.min(i * 0.06, 0.4)}s`;
            observer.observe(card);
        });
    }

    // Observar cards iniciales cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => observe());
    } else {
        observe();
    }

    // Exponer para que el Router lo llame tras inyectar vistas
    window.ScrollReveal = { observe };
})();


/* ═══════════════════════════════════════════════════════
   SKELETON LOADER — helpers para tablas
═══════════════════════════════════════════════════════ */

/**
 * Inserta `count` filas skeleton en un <tbody>.
 * @param {HTMLElement|string} tbodyOrId
 * @param {number} cols   Número de columnas
 * @param {number} count  Número de filas skeleton
 */
function showTableSkeleton(tbodyOrId, cols = 4, count = 5) {
    const tbody = typeof tbodyOrId === 'string'
        ? document.getElementById(tbodyOrId)
        : tbodyOrId;

    if (!tbody) return;

    const rows = Array.from({ length: count }, () => {
        const tr = document.createElement('tr');
        tr.className = 'skeleton-row';

        for (let i = 0; i < cols; i++) {
            const td = document.createElement('td');
            // Variar los anchos para que parezca más real
            const widthClass = i === 0 ? 'md' : i === cols - 1 ? 'xs' : 'sm';
            td.innerHTML = `<div class="skeleton skeleton-line ${widthClass}"></div>`;
            tr.appendChild(td);
        }

        return tr;
    });

    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Elimina las filas skeleton del tbody.
 * (Simplemente limpia el tbody; el controlador debe rellenar con datos reales.)
 * @param {HTMLElement|string} tbodyOrId
 */
function hideTableSkeleton(tbodyOrId) {
    const tbody = typeof tbodyOrId === 'string'
        ? document.getElementById(tbodyOrId)
        : tbodyOrId;

    if (!tbody) return;

    tbody.querySelectorAll('.skeleton-row').forEach(row => row.remove());
}

window.showTableSkeleton = showTableSkeleton;
window.hideTableSkeleton = hideTableSkeleton;


/* ═══════════════════════════════════════════════════════
   AUTO-INIT — integración con Router
═══════════════════════════════════════════════════════ */

/**
 * Hook que el Router invoca tras inyectar cada vista.
 * Registra scroll-reveal en las nuevas cards y ripple en botones.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Parchear Router.navigate para disparar ScrollReveal tras cada vista
    const _originalInitController =
        window.Router && window.Router.initController
            ? window.Router.initController.bind(window.Router)
            : null;

    if (window.Router && _originalInitController) {
        window.Router.initController = function (view) {
            _originalInitController(view);
            // Pequeño delay para que el controlador de vista renderice su contenido
            setTimeout(() => {
                if (window.ScrollReveal) {
                    ScrollReveal.observe(
                        document.getElementById('main-content') || document
                    );
                }
            }, 120);
        };
    }
});
