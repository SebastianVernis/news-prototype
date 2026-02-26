# Proyecto de Sitio Web de Noticias - Cloudflare

## Resumen del Proyecto

Este proyecto contiene un sitio web de noticias completo con todas las características solicitadas, listo para desplegar en Cloudflare Pages y Workers.

## Contenido del Proyecto

### Archivos de Configuración
- `wrangler.toml` - Archivo de configuración corregido para Cloudflare
- `package.json` - Dependencias del proyecto

### Frontend (Carpeta `public/`)
- `index.html` - Página principal
- `admin.html` - Panel de administración
- `style.css` - Estilos del sitio
- `script.js` - Funcionalidad del frontend
- `favicon.ico` - Icono del sitio
- `_routes.json` - Configuración de rutas

### Backend (Carpetas `src/` y `workers/`)
- `src/index.js` - Worker principal de la API
- `workers/cron-worker.js` - Worker para tareas programadas
- `functions/api/articles/index.js` - Función de Pages para artículos

### Scripts de Despliegue
- `deploy-menu.sh` - Menú de despliegue
- `deploy-interactive.sh` - Despliegue interactivo corregido
- `full-deploy.sh` - Despliegue automático
- `build.sh` - Proceso de build
- `check-resources.sh` - Verificación de recursos

### Instrucciones de Configuración Manual
- `setup-pages.txt` - Crear proyecto de Pages
- `setup-kv.txt` - Crear namespace KV
- `setup-d1.txt` - Crear base de datos D1
- `setup-api-worker.txt` - Crear worker de API
- `setup-cron-worker.txt` - Crear worker de cron
- `setup-env-vars.txt` - Configurar variables de entorno
- `setup-admin-token.txt` - Generar token de admin
- `setup-upload-files.txt` - Subir archivos del sitio
- `setup-complete.txt` - Resumen de configuración completa

### Documentación
- `README.md` - Documentación general
- `README_DEPLOY.md` - Instrucciones de despliegue
- `README_INTERACTIVE.md` - Despliegue interactivo
- `README_CORRECTION.md` - Corrección de errores
- `DOCUMENTACION.md` - Documentación técnica en español
- `SUMMARY.md` - Resumen del proyecto
- `INSTRUCCIONES_COMPLETAS.md` - Instrucciones completas para despliegue manual

## Características del Sitio

- Diseño responsivo moderno
- Preloader con efectos animados
- Slider de artículos destacados
- Ticker de noticias rápidas
- Cuadrícula de artículos con miniaturas circulares
- Barra lateral con categorías y artículos populares
- Sistema de búsqueda avanzado
- Integración con redes sociales
- Panel de administración para gestión de contenido
- Actualización automática de noticias mediante cron jobs
- Headers y footers estilizados en todas las páginas

## Pasos para Despliegue Manual

Dado que el despliegue automático puede tener problemas de autenticación, sigue estos pasos:

1. Lee `INSTRUCCIONES_COMPLETAS.md` para obtener el flujo completo
2. Sigue cada archivo `setup-*.txt` en orden para crear los recursos
3. Usa `check-resources.sh` para verificar tu progreso
4. Genera tu token de admin siguiendo `setup-admin-token.txt`
5. Sube los archivos del sitio como se indica en `setup-upload-files.txt`

## Acceso a los Recursos

Después del despliegue completo:

- **Sitio web**: `https://noticias-hoy.pages.dev` (o tu dominio personalizado)
- **Panel de admin**: `https://noticias-hoy.pages.dev/admin.html`
- **API**: `https://news-api.[tu-subdominio].workers.dev`
- **Cron**: `https://news-cron.[tu-subdominio].workers.dev`

## Seguridad

- Todos los tokens se almacenan de forma segura como 'Secrets' en Cloudflare
- Autenticación JWT para operaciones de administración
- CORS configurado adecuadamente
- Validación de entradas en todos los endpoints

¡Tu sitio web de noticias está listo para configurar y desplegar siguiendo las instrucciones detalladas!