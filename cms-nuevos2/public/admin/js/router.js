const Router = {
  contentElement: null,
  currentView: null,
  _navigating: false,

  async init() {
    this.contentElement = document.getElementById("main-content");
    window.addEventListener("popstate", () => this.loadFromUrl());
    // Inicializar ripple en todos los botones existentes
    this._initRipple();
    this.loadFromUrl();
  },

  async navigate(view, pushState = true) {
    if (this._navigating) return;
    this._navigating = true;

    try {
      // ── Animación de salida ──
      if (this.currentView && this.contentElement.children.length) {
        this.contentElement.classList.add("view-leaving");
        await this._wait(150);
        this.contentElement.classList.remove("view-leaving");
      }

      // Cargar el fragmento HTML
      const response = await fetch(`views/${view}.html?v=${Date.now()}`);
      if (!response.ok)
        throw new Error(
          `Vista ${view} no encontrada (HTTP ${response.status})`,
        );

      const html = await response.text();
      this.contentElement.innerHTML = html;
      this.currentView = view;

      // ── Animación de entrada ──
      this.contentElement.classList.add("view-entering");
      this.contentElement.addEventListener(
        "animationend",
        () => {
          this.contentElement.classList.remove("view-entering");
        },
        { once: true },
      );

      // Actualizar Sidebar activo
      document.querySelectorAll(".nav-link").forEach((l) => {
        l.classList.toggle("active", l.dataset.view === view);
      });

      if (pushState) {
        const url = `#${view}`;
        if (window.location.hash !== url) history.pushState({ view }, "", url);
      }

      // Registrar ripple en nuevos botones inyectados
      this._initRipple(this.contentElement);

      // Inicializar controlador específico
      console.log(`[Router] Vista: ${view}`);
      this.initController(view);
    } catch (e) {
      console.error("[Router] Error:", e);
      this.contentElement.innerHTML = `
                <div class="card" style="border-left: 5px solid #dc3545; animation: view-enter 0.3s ease forwards;">
                    <h2 style="color:#dc3545; margin-bottom:0.5rem;">
                        <i class="fas fa-exclamation-triangle"></i> Error 404
                    </h2>
                    <p>No se pudo cargar la vista: <strong>${view}</strong></p>
                    <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:0.25rem;">${e.message}</p>
                    <button class="btn btn-outline" style="margin-top:1rem;" onclick="location.reload()">
                        <i class="fas fa-redo"></i> Reintentar
                    </button>
                </div>
            `;
    } finally {
      this._navigating = false;
    }
  },

  loadFromUrl() {
    const view = window.location.hash.replace("#", "") || "dashboard";
    this.navigate(view, false);
  },

  initController(view) {
    // Timeout pequeño para asegurar que el DOM se haya inyectado
    setTimeout(() => {
      switch (view) {
        case "dashboard":
          if (window.initDashboard) initDashboard();
          break;
        case "content-explorer":
          if (window.initContentExplorer) initContentExplorer();
          break;
        case "cms":
          if (window.initCMS) initCMS();
          break;
        case "revision":
          if (window.initRevision) initRevision();
          break;
        case "sites":
          if (window.initSites) initSites();
          break;
        case "categories":
          if (window.initCategories) initCategories();
          break;
        case "articles":
          if (window.initArticles) initArticles();
          break;
        case "editor":
          if (window.initEditor) initEditor();
          break;
        case "facebook":
          if (window.initFacebook) initFacebook();
          break;
        case "monitor":
          if (window.initMonitor) initMonitor();
          break;
        case "featured":
          if (window.initFeatured) initFeatured();
          break;
        case "users":
          if (window.UsersModule) UsersModule.render();
          break;
        case "privacidad":
          /* Vista estática */ break;
        case "terminos":
          /* Vista estática */ break;
        case "borrado":
          /* Vista estática */ break;
      }
    }, 50);
  },

  // ── Helpers ─────────────────────────────────────────────

  /** Promesa de timeout para encadenar con await */
  _wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  },

  /**
   * Registra el efecto ripple en todos los .btn y .nav-link
   * dentro del scope dado (o document si no se pasa).
   */
  _initRipple(scope = document) {
    scope
      .querySelectorAll(".btn:not([data-ripple]), .nav-link:not([data-ripple])")
      .forEach((el) => {
        el.setAttribute("data-ripple", "1");
        el.addEventListener("click", function (e) {
          // No animar si el botón está deshabilitado
          if (this.disabled) return;

          const rect = this.getBoundingClientRect();
          const size = Math.max(rect.width, rect.height) * 2;
          const x = e.clientX - rect.left - size / 2;
          const y = e.clientY - rect.top - size / 2;

          const ripple = document.createElement("span");
          ripple.classList.add("ripple");
          ripple.style.cssText = `
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                `;
          this.appendChild(ripple);
          ripple.addEventListener("animationend", () => ripple.remove(), {
            once: true,
          });
        });
      });
  },
};
