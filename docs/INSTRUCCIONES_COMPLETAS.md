# Instrucciones Completas para Despliegue Manual en Cloudflare

## Introducción

Dado que el despliegue automático no funcionó correctamente debido a problemas de autenticación, hemos preparado este conjunto de instrucciones paso a paso para que puedas configurar manualmente todos los recursos necesarios para tu sitio web de noticias en Cloudflare.

## Requisitos Previos

- Cuenta activa en Cloudflare
- Acceso a un navegador web (se recomienda Firefox para la autenticación)
- Clave de API de NewsAPI (opcional)
- Terminal o línea de comandos

## Pasos para la Configuración Completa

### Paso 1: Crear el Proyecto de Pages
Sigue las instrucciones en: `setup-pages.txt`

### Paso 2: Crear el Namespace KV
Sigue las instrucciones en: `setup-kv.txt`

### Paso 3: Crear la Base de Datos D1
Sigue las instrucciones en: `setup-d1.txt`

### Paso 4: Crear el Worker de API
Sigue las instrucciones en: `setup-api-worker.txt`

### Paso 5: Crear el Worker de Cron
Sigue las instrucciones en: `setup-cron-worker.txt`

### Paso 6: Configurar Variables de Entorno
Sigue las instrucciones en: `setup-env-vars.txt`

### Paso 7: Generar Token de Admin
Sigue las instrucciones en: `setup-admin-token.txt`

### Paso 8: Subir Archivos del Sitio
Sigue las instrucciones en: `setup-upload-files.txt`

## Verificación de Recursos

Puedes usar el script de verificación para comprobar qué recursos tienes disponibles:

```bash
./check-resources.sh
```

## Archivos del Proyecto

Todos los archivos necesarios para tu sitio web de noticias están en la carpeta `public/`:

- `index.html` - Página principal del sitio
- `admin.html` - Panel de administración
- `style.css` - Estilos del sitio
- `script.js` - Funcionalidad del frontend
- `favicon.ico` - Icono del sitio
- `_routes.json` - Configuración de rutas

## Backend Workers

Los archivos para los Workers están en:

- `src/index.js` - Worker principal de la API
- `workers/cron-worker.js` - Worker para tareas programadas

## Panel de Administración

Una vez desplegado todo, podrás acceder al panel de administración en:
`https://[nombre-de-tu-proyecto].pages.dev/admin.html`

Necesitarás tu token de admin para autenticarte.

## API Endpoints

Después del despliegue, estarán disponibles los siguientes endpoints:

- `https://[tu-worker-api].workers.dev/api/articles` - Lista de artículos
- `https://[tu-worker-api].workers.dev/api/categories` - Categorías
- `https://[tu-worker-api].workers.dev/api/search?q=consulta` - Búsqueda

## Actualizaciones Automáticas

El worker de cron se encargará de:

- Obtener nuevas noticias periódicamente
- Actualizar artículos destacados
- Limpiar artículos antiguos
- Generar reportes periódicos

## Solución de Problemas

Si tienes problemas:

1. Verifica que estás usando Firefox para la autenticación con Cloudflare
2. Asegúrate de que tu API Token tiene los permisos correctos
3. Confirma que todos los recursos están creados con los nombres exactos
4. Verifica que las variables de entorno están configuradas correctamente
5. Revisa que los archivos se hayan subido correctamente

## Seguridad

- Guarda tu token de admin en un lugar seguro
- No compartas tus claves de API
- Usa siempre 'Secrets' en lugar de variables normales para información sensible
- Renueva tus tokens periódicamente

## Próximos Pasos

Una vez completes todos los pasos manuales:

1. Prueba el sitio web completo
2. Verifica que el panel de administración funcione
3. Confirma que las actualizaciones automáticas funcionan
4. Prueba las funcionalidades de búsqueda y categorías
5. Configura tu dominio personalizado si lo deseas

¡Tu sitio web de noticias estará completamente operativo cuando completes todos estos pasos!