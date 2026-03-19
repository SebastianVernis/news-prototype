/**
 * NexoPress CMS — Theme Manager
 * Dark / Light mode con persistencia en localStorage
 * y soporte a prefers-color-scheme.
 */

const ThemeManager = (() => {
    const STORAGE_KEY = 'NEXOPRESS_THEME';
    const DARK_CLASS  = 'dark-mode';

    /** Lee la preferencia almacenada o detecta la del sistema */
    function getPreferred() {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) return stored;
        return window.matchMedia('(prefers-color-scheme: dark)').matches
            ? 'dark'
            : 'light';
    }

    /** Aplica el tema al <html> y actualiza todos los botones toggle */
    function apply(theme) {
        const isDark = theme === 'dark';
        document.documentElement.classList.toggle(DARK_CLASS, isDark);

        // Actualizar todos los botones de toggle que existan en el DOM
        document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
            const iconEl = btn.querySelector('i');
            const labelEl = btn.querySelector('.theme-label');

            if (iconEl) {
                iconEl.className = isDark
                    ? 'fas fa-sun'
                    : 'fas fa-moon';
            }
            if (labelEl) {
                labelEl.textContent = isDark ? 'Modo claro' : 'Modo oscuro';
            }

            btn.setAttribute('aria-label',
                isDark ? 'Activar modo claro' : 'Activar modo oscuro');
            btn.setAttribute('title',
                isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
        });
    }

    /** Guarda y aplica */
    function set(theme) {
        localStorage.setItem(STORAGE_KEY, theme);
        apply(theme);
    }

    /** Alterna entre dark y light */
    function toggle() {
        const current = localStorage.getItem(STORAGE_KEY)
            || (document.documentElement.classList.contains(DARK_CLASS)
                ? 'dark' : 'light');
        set(current === 'dark' ? 'light' : 'dark');
    }

    /** Devuelve el tema activo */
    function current() {
        return document.documentElement.classList.contains(DARK_CLASS)
            ? 'dark'
            : 'light';
    }

    /**
     * Inicializa el manager:
     *  - Aplica el tema preferido antes del primer paint
     *  - Registra listener para cambios del sistema
     *  - Delega clicks en botones data-theme-toggle
     */
    function init() {
        // Aplicar tema inicial (sin transición para evitar flash)
        document.documentElement.style.setProperty(
            '--theme-transition', 'none');
        apply(getPreferred());

        // Habilitar transiciones después del primer frame
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                document.documentElement.style.removeProperty(
                    '--theme-transition');
            });
        });

        // Escuchar cambios del sistema operativo
        const mq = window.matchMedia('(prefers-color-scheme: dark)');
        mq.addEventListener('change', e => {
            // Solo reaccionar si el usuario no fijó preferencia manual
            if (!localStorage.getItem(STORAGE_KEY)) {
                apply(e.matches ? 'dark' : 'light');
            }
        });

        // Delegación de eventos para botones toggle
        document.addEventListener('click', e => {
            const btn = e.target.closest('[data-theme-toggle]');
            if (btn) {
                toggle();
                // Micro-animación de rotación en el ícono
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.classList.add('theme-icon-spin');
                    icon.addEventListener('animationend', () => {
                        icon.classList.remove('theme-icon-spin');
                    }, { once: true });
                }
            }
        });

        console.log('[ThemeManager] Inicializado — tema:', getPreferred());
    }

    return { init, toggle, set, current, apply };
})();

// Auto-inicializar lo antes posible para evitar FOUC
ThemeManager.init();
