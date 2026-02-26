# NexoPress - Sistema de Noticias Multi-Sitio (Cloudflare)

NexoPress es una plataforma de noticias de alto rendimiento diseñada íntegramente para el ecosistema de **Cloudflare**. Gestiona 10 sitios de noticias independientes desde un único panel de administración y un núcleo centralizado en Cloudflare Workers y D1.

## 🚀 Arquitectura del Sistema

El proyecto se basa en una arquitectura de **Worker Unificado** que gestiona tanto la API como las tareas programadas (Cron Jobs).

- **Frontend:** 10 sitios estáticos en Cloudflare Pages.
- **Backend (API):** Cloudflare Workers (Hono framework).
- **Base de Datos:** Cloudflare D1 (SQLite).
- **Almacenamiento:** Cloudflare R2 (Imágenes) y KV (Caché/Estado).
- **IA:** Integración con OpenRouter (Gemini 2.0 Flash) para corrección de estilo y parafraseo.

## ✨ Características Principales

- **Ingesta Multi-Formato:** Soporte para RSS y Atom (El País, Proceso, Aristegui, etc.).
- **Parafraseo con IA:** Corrección automática de ortografía y gramática mediante IA.
- **Flujo de Facebook Inteligente:**
  - Publicación automática cada 3 horas por sitio.
  - Filtro de **"Imagen Perfecta"**: Solo publica en Facebook si el artículo tiene una imagen original (evita imágenes de relleno).
  - Tokens de página permanentes (Never Expire).
- **Dashboard Administrativo:**
  - Gestión centralizada de 10 sitios.
  - **Monitor de Sistema:** Seguimiento en tiempo real de crons, tokens de Facebook e historial de publicaciones.
  - Ingesta manual forzada para diagnóstico.

## 📚 Documentación

Para una guía detallada sobre el funcionamiento del sistema, consulta nuestro **[Índice Documental](./docs/INDEX.md)**.

## 🛠️ Estructura del Proyecto

```
├── public/admin/           # Dashboard de Administración (JS/HTML/CSS)
│   ├── views/monitor.html  # Nueva vista de monitoreo de sistema
│   └── js/monitor.js       # Lógica del monitor y diagnósticos
├── src/
│   ├── index.js            # Worker Unificado (API + Cron + FB Flow)
│   └── schema.sql          # Definición completa de la base de datos D1
├── scripts/                # Utilidades de despliegue y mantenimiento
├── backups/archive/        # Archivo de scripts y backups obsoletos
├── wrangler.toml           # Configuración de Cloudflare
└── README.md               # Este archivo
```

## ⚙️ Configuración y Despliegue

### Requisitos
- Cloudflare CLI (`wrangler`)
- Cuenta de OpenRouter (para la IA)
- Tokens de acceso a páginas de Facebook

### Despliegue del Worker
```bash
cd src
wrangler deploy index.js --name news-api --config wrangler.toml
```

### Variables de Entorno Críticas (Secrets)
Es necesario configurar los siguientes secretos en Cloudflare:
- `OPENROUTER_API_KEY`: Para el parafraseo e ingesta.
- `FB_TOKEN_[SITIO]`: Un token permanente por cada uno de los 10 sitios.
- `ADMIN_SETUP_BASE_URL`: URL base para la administración.

## 📊 Monitoreo

El sistema incluye endpoints de diagnóstico protegidos:
- `GET /api/cron/status`: Estado de las últimas tareas automáticas.
- `GET /api/facebook/debug-tokens`: Verifica la validez de los tokens de Facebook.
- `POST /api/cron/ingest`: Dispara una ingesta manual de noticias.

---
© 2026 NexoPress Network. Todos los derechos reservados.
