# Estructura del Proyecto - NexoPress

## Descripción General

NexoPress es una plataforma unificada para la gestión de 10 sitios de noticias en el ecosistema Cloudflare.

---

## Raíz del Proyecto (`/`)

```
├── README.md               # Documentación principal
├── PROJECT_STATUS.txt      # Estado operativo y hitos
├── PROJECT_STRUCTURE.md    # Este archivo
├── TODO.md                 # Tareas pendientes
├── package.json            # Dependencias Node.js
└── wrangler.toml           # Referencia de configuración
```

---

## Carpetas Principales

### 📁 `src/` - Núcleo del Sistema (Worker Unificado)
- **index.js**: El Worker principal que maneja la API, las tareas programadas (Cron) y el flujo de Facebook.
- **schema.sql**: Definición de la base de datos D1.
- **wrangler.toml**: Configuración de despliegue del backend.

### 📁 `public/` - Panel de Administración (CMS)
- **admin/**: Interfaz de gestión del sistema (PWA).
- **functions/**: Funciones intermedias para Pages.
- **_routes.json**: Configuración de enrutamiento dinámico.

### 📁 `docs/` - Centro de Documentación
- **INDEX.md**: Punto de entrada a toda la documentación.
- **SYSTEM_MONITOR.md**: Guía del sistema de monitoreo.
- **API_REFERENCE.md**: Lista de endpoints y autenticación.
- **archive/**: Documentación histórica y de fases previas.

### 📁 `sites/` - Sitios de Noticias (Pages)
- Contiene las carpetas individuales para cada uno de los 10 dominios (`bitacoraurbana`, `tvmexico`, etc.).

### 📁 `tools/` y `scripts/` - Utilidades
- Herramientas auxiliares para mantenimiento, correcciones masivas y despliegues técnicos.

### 📁 `backups/` - Almacenamiento Local
- **archive/**: Contenedor de archivos temporales, reportes antiguos y backups de base de datos SQL.

### 📁 `assets/` - Recursos Compartidos
- Imágenes de respaldo y archivos estáticos generales.

---

## Flujo Operativo Actual

1. **Ingesta Automática:** El worker unificado (`src/index.js`) descarga noticias cada 30 min via RSS/Atom.
2. **IA:** Las noticias se procesan con Gemini para corregir estilo y gramática.
3. **Facebook:** El sistema selecciona artículos con "Imagen Perfecta" y los publica en las páginas de cada sitio cada 3 horas.
4. **Dashboard:** El administrador supervisa todo desde la sección "Monitor Sistema".

---
**Última actualización**: 26 de Febrero, 2026
