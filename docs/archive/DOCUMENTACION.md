# Documentación del Proyecto: Sitio Web de Noticias - Despliegue en Cloudflare

## Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Características del Sitio Web](#características-del-sitio-web)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Despliegue en Cloudflare](#despliegue-en-cloudflare)
5. [Configuración del Backend](#configuración-del-backend)
6. [API Endpoints](#api-endpoints)
7. [Panel de Administración](#panel-de-administración)
8. [Tareas Programadas (Cron)](#tareas-programadas-cron)
9. [Personalización y Marca](#personalización-y-marca)
10. [Desarrollo Local](#desarrollo-local)
11. [Solución de Problemas](#solución-de-problemas)

## Descripción del Proyecto

Este es un sitio web completo de noticias diseñado para despliegarse en Cloudflare Pages con funcionalidad de backend impulsada por Cloudflare Workers. El proyecto incluye todas las características solicitadas: diseño responsivo, preloader, slider de artículos destacados, ticker de noticias rápidas, cuadrícula de artículos con miniaturas circulares, barra lateral con categorías y populares, sistema de búsqueda, iconos sociales, y un panel de administración para gestión de contenido.

## Características del Sitio Web

- **Diseño responsivo**: Compatible con móviles, tablets y escritorio
- **Preloader animado**: Efecto de carga con animación
- **Slider de artículos destacados**: Carrusel para artículos principales
- **Ticker de noticias rápidas**: Barra deslizante para noticias de última hora
- **Cuadrícula de artículos**: Layout flexible con miniaturas circulares
- **Barra lateral**: Categorías, artículos populares y formulario de newsletter
- **Plantilla de artículos**: Diseño optimizado para lectura
- **Sistema de búsqueda**: Filtrado por categorías y términos
- **Iconos sociales**: Integración con redes sociales
- **Páginas de categorías**: Navegación específica por temas
- **Sistema de marca**: Fácil personalización para diferentes dominios

## Estructura del Proyecto

```
cloudflare-news-project/
├── public/                 # Recursos estáticos (HTML, CSS, JS)
│   ├── index.html          # Página principal
│   ├── admin.html          # Panel de administración
│   ├── style.css           # Hoja de estilos
│   ├── script.js           # JavaScript del cliente
│   ├── favicon.ico         # Icono del sitio
│   └── images/             # Recursos de imagen
├── src/                    # Código fuente del backend
│   └── index.js            # Worker principal de la API
├── workers/                # Workers especializados
│   └── cron-worker.js      # Worker para tareas programadas
├── functions/              # Funciones de Cloudflare Pages
│   └── api/
│       └── articles/
│           └── index.js    # Endpoint de artículos
├── wrangler.toml           # Configuración de Cloudflare
├── package.json            # Dependencias y scripts
├── deploy.sh               # Script de despliegue
├── build.sh                # Script de construcción
└── README.md               # Documentación principal
```

## Despliegue en Cloudflare

### Requisitos Previos

- Cuenta en Cloudflare
- CLI de Wrangler instalado (`npm install -g wrangler`)
- Acceso al ID de cuenta de Cloudflare

### Despliegue del Frontend (Cloudflare Pages)

1. Prepara tus recursos estáticos en el directorio `public`
2. Inicia sesión en Wrangler: `wrangler login`
3. Despliega a Cloudflare Pages:
   ```bash
   wrangler pages deploy ./public --project-name=nombre-de-tu-proyecto
   ```

### Despliegue del Backend (Cloudflare Workers)

1. Actualiza el archivo `wrangler.toml` con tus detalles de cuenta
2. Despliega el worker:
   ```bash
   wrangler deploy src/index.js --name news-api
   ```

### Configuración del Entorno

Crea un archivo `.dev.vars` para desarrollo local:

```env
CF_ACCOUNT_ID=your_account_id
CF_API_TOKEN=your_api_token
DATABASE_URL=your_database_url
ADMIN_TOKEN=your_admin_token
```

## Configuración del Backend

### Base de Datos

El backend utiliza Cloudflare D1 para almacenamiento persistente y KV para caché rápida. Las tablas principales son:

- `articles`: Contiene todos los artículos de noticias
- `categories`: Categorías de noticias
- `users`: Usuarios administradores

### Variables de Entorno

- `ADMIN_TOKEN`: Token para autenticación de administrador
- `SITE_TITLE`: Título del sitio
- `SITE_DESCRIPTION`: Descripción del sitio
- `DATABASE_URL`: URL de conexión a la base de datos

## API Endpoints

El backend proporciona los siguientes endpoints de API:

- `GET /api/articles` - Obtener todos los artículos con paginación
- `GET /api/articles/:slug` - Obtener un artículo específico
- `POST /api/articles` - Crear un nuevo artículo (solo admin)
- `PUT /api/articles/:id` - Actualizar un artículo (solo admin)
- `DELETE /api/articles/:id` - Eliminar un artículo (solo admin)
- `PATCH /api/articles/:id/featured` - Alternar estado destacado
- `GET /api/categories` - Obtener todas las categorías
- `GET /api/search?q=query` - Buscar artículos
- `GET /api/articles/featured` - Obtener artículos destacados
- `GET /api/articles/popular` - Obtener artículos populares

### Autenticación

Los endpoints de administración requieren un token de autenticación en el encabezado `Authorization: Bearer YOUR_TOKEN`.

## Panel de Administración

### Acceso

Accede al panel de administración en `/admin.html` para gestionar contenido. Necesitarás un token de administrador para acceder.

### Funcionalidades

- **Gestión de artículos**: Crear, editar y eliminar artículos
- **Categorías**: Administrar categorías de noticias
- **Artículos destacados**: Marcar artículos como destacados
- **Usuarios**: Gestión de usuarios administradores
- **Estadísticas**: Métricas básicas del sitio

## Tareas Programadas (Cron)

Tareas programadas que se ejecutan automáticamente:

- **Obtener noticias cada hora**: Busca nuevas noticias de fuentes externas
- **Actualizar artículos destacados cada 30 minutos**: Rotación de artículos destacados
- **Limpiar artículos antiguos diariamente**: Elimina artículos muy antiguos
- **Generar reportes semanales**: Reportes analíticos semanales

### Configuración de Cron

Las tareas están configuradas en `wrangler.toml`:

```toml
[[triggers]]
crons = [
  "0 * * * *",      # Cada hora
  "*/30 * * * *",   # Cada 30 minutos
  "0 2 * * *",      # Diariamente a las 2 AM
  "0 9 * * 0"       # Semanalmente los domingos a las 9 AM
]
```

## Personalización y Marca

### Cambiar la Marca

Para personalizar el sitio para tu dominio:

1. Actualiza el `SITE_TITLE` y `SITE_DESCRIPTION` en `wrangler.toml`
2. Modifica el archivo `public/style.css` para ajustar colores y branding
3. Actualiza el favicon en `public/favicon.ico`
4. Cambia el placeholder del logo en los archivos HTML

### Paleta de Colores

Las variables CSS definidas en `:root` permiten fácil personalización:

```css
--primary-color: #667eea;    /* Color primario */
--secondary-color: #764ba2;  /* Color secundario */
--accent-color: #f093fb;     /* Color de acento */
```

## Desarrollo Local

### Configuración Inicial

1. Instala dependencias: `npm install`
2. Ejecuta servidor de desarrollo: `npm run dev`
3. Realiza tus cambios
4. Prueba la compilación: `npm run build`
5. Despliega cuando estés listo

### Desarrollo con Wrangler

Para simular el entorno de Cloudflare localmente:

```bash
wrangler pages dev ./public
```

## Solución de Problemas

### Problemas Comunes

1. **Credenciales de Cloudflare incorrectas**: Verifica que tus credenciales de Cloudflare sean correctas
2. **Espacios de nombres KV no configurados**: Verifica que tus espacios de nombres KV y bases de datos D1 estén correctamente configurados
3. **Variables de entorno no establecidas**: Asegúrate de que todas las variables de entorno estén configuradas
4. **Errores de despliegue**: Revisa el panel de control de Cloudflare para ver errores de despliegue

### Verificación de Salud

Consulta `/api/health` para verificar el estado del backend.

### Registro de Errores

Los errores se registran en la consola de Cloudflare Workers y pueden verse en el panel de control.

## Seguridad

- Todas las rutas de administración están protegidas con autenticación
- Validación de entrada en todos los endpoints
- CORS configurado adecuadamente
- Uso de HTTPS obligatorio

## Rendimiento

- Recursos estáticos servidos desde Cloudflare CDN
- Caché implementada con Cloudflare KV
- Compresión de recursos
- Lazy loading para imágenes

## Mantenimiento

### Copias de Seguridad

Las bases de datos D1 se copian automáticamente. Para copias manuales:

```bash
wrangler d1 backup create DB_NAME
```

### Monitoreo

- Supervisión de tiempos de respuesta
- Seguimiento de errores
- Métricas de uso

## Actualizaciones

Para actualizar el sistema:

1. Realiza una copia de seguridad
2. Prueba cambios en entorno de staging
3. Implementa en producción
4. Verifica funcionalidad

## Soporte

Para obtener más información, visita la [documentación de Cloudflare Pages](https://developers.cloudflare.com/pages/) y [documentación de Workers](https://developers.cloudflare.com/workers/).

---

**Versión**: 1.0  
**Fecha**: Febrero 2026  
**Soporte**: Para soporte adicional, contacta al equipo de desarrollo