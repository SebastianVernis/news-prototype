# Despliegue Completo del Sitio Web de Noticias en Cloudflare

Este proyecto contiene un sitio web de noticias completo con todas las características solicitadas, listo para desplegar en Cloudflare Pages y Workers.

## Características del Sitio

- Diseño responsivo moderno
- Preloader con animación
- Slider de artículos destacados
- Ticker de noticias rápidas
- Cuadrícula de artículos con miniaturas circulares
- Barra lateral con categorías y artículos populares
- Sistema de búsqueda avanzado
- Integración con redes sociales
- Panel de administración para gestión de contenido
- Actualización automática de noticias mediante cron jobs

## Requisitos Previos

- Node.js instalado
- Wrangler CLI instalado (`npm install -g wrangler`)
- Cuenta en Cloudflare
- (Opcional) Clave de API de NewsAPI

## Variables de Despliegue

El despliegue completo requiere las siguientes variables:

### Obligatorias:
- `CF_ACCOUNT_ID`: ID de tu cuenta de Cloudflare
- `CF_API_TOKEN`: Token de API con permisos para deploy
- `ADMIN_TOKEN`: Token seguro para autenticación de admin (mínimo 32 caracteres)

### Opcionales:
- `NEWSAPI_KEY`: Clave de API para obtener noticias externas

## Proceso de Despliegue Completo

### Método 1: Despliegue Automático (Recomendado)

1. Asegúrate de tener Wrangler instalado:
   ```bash
   npm install -g wrangler
   ```

2. Ejecuta el script de despliegue completo:
   ```bash
   ./full-deploy.sh
   ```

3. El script te pedirá las variables necesarias y creará todos los recursos automáticamente:
   - Proyecto de Cloudflare Pages
   - Namespaces KV para almacenamiento
   - Base de datos D1 para persistencia
   - Workers para backend y cron jobs
   - Configuración de variables de entorno

### Método 2: Despliegue Manual

1. Actualiza el archivo `wrangler.toml` con tus propios valores:
   ```bash
   # Edita wrangler.toml y reemplaza los placeholders:
   # - your_account_id_here
   # - your_secure_admin_token_here
   # - your_newsapi_key_here
   # - etc.
   ```

2. Crea los recursos manualmente:
   ```bash
   # Crear namespace KV
   wrangler kv:namespace create "ARTICLES_KV"
   
   # Crear base de datos D1
   wrangler d1 create news_db
   
   # Desplegar workers
   wrangler deploy src/index.js --name news-api
   wrangler deploy workers/cron-worker.js --name news-cron
   
   # Desplegar frontend
   wrangler pages deploy ./public --project-name=news-website
   ```

## Recursos Creados

El despliegue completo crea:

- **Cloudflare Pages**: Hosting del frontend
- **Cloudflare Workers**: Backend API y cron jobs
- **KV Namespace**: Almacenamiento de caché
- **D1 Database**: Base de datos SQL para artículos
- **Variables de entorno**: Configuración segura

## Acceso a los Recursos

Después del despliegue:

- **Sitio web**: `https://news-website.pages.dev`
- **API**: `https://news-api.your-account-id.workers.dev`
- **Panel de admin**: `https://news-website.pages.dev/admin.html`
- **Health check**: `https://news-api.your-account-id.workers.dev/api/health`

## Configuración Post-Despliegue

1. Visita el panel de administración con tu token de admin
2. Configura las categorías iniciales
3. Personaliza el branding si es necesario
4. Configura tu dominio personalizado en Cloudflare Dashboard

## Solución de Problemas

Si encuentras problemas:

1. Verifica que tus credenciales de Cloudflare sean correctas
2. Asegúrate de tener permisos suficientes en tu cuenta
3. Revisa el archivo `deployment-config.json` generado después del despliegue
4. Consulta los logs en Cloudflare Dashboard

## Seguridad

- Todos los tokens se almacenan de forma segura usando `wrangler secret:put`
- Autenticación JWT para operaciones de administración
- CORS configurado adecuadamente
- Validación de entradas en todos los endpoints

## Mantenimiento

- Las actualizaciones de noticias ocurren automáticamente según la configuración de cron
- El sistema de caché KV mejora el rendimiento
- Las bases de datos D1 ofrecen persistencia y escalabilidad

¡Tu sitio web de noticias está listo para usar!