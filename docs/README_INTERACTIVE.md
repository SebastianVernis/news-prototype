# Asistente de Despliegue Interactivo para el Sitio Web de Noticias

Este proyecto incluye múltiples opciones para desplegar tu sitio web de noticias en Cloudflare, desde métodos completamente interactivos hasta soluciones automatizadas.

## Opciones de Despliegue Disponibles

### 1. Despliegue Interactivo (Recomendado para primer uso)

El script `deploy-interactive.sh` te guía paso a paso para ingresar todas las variables necesarias:

```bash
./deploy-interactive.sh
```

Este asistente:
- Solicita interactivamente todas las credenciales necesarias
- Valida que los valores ingresados sean correctos
- Confirma los valores antes de proceder
- Crea todos los recursos necesarios en Cloudflare
- Configura variables de entorno de forma segura
- Proporciona un resumen completo del despliegue

### 2. Despliegue Automático

El script `full-deploy.sh` realiza un despliegue completamente automatizado:

```bash
./full-deploy.sh
```

Este script requiere que tengas previamente configuradas las variables en:
- Archivo `wrangler.toml`
- Archivo `.dev.vars` (opcional)

### 3. Menú de Despliegue

El script `deploy-menu.sh` proporciona una interfaz de menú para elegir tu opción preferida:

```bash
./deploy-menu.sh
```

Este menú te permite:
- Seleccionar entre diferentes opciones de despliegue
- Verificar el estado de tu configuración
- Acceder a la documentación
- Probar localmente

## Variables Requeridas

Independientemente del método elegido, necesitarás:

### Obligatorias:
- **Account ID de Cloudflare**: Lo encuentras en https://dash.cloudflare.com
- **API Token de Cloudflare**: Crea un token con permisos para Pages, Workers, KV, y D1
- **Admin Token**: Token seguro para autenticación de admin (mínimo 32 caracteres)
- **Nombre del Proyecto**: Nombre para tu proyecto de Pages

### Opcionales:
- **NewsAPI Key**: Para integración con fuentes de noticias externas
- **Dominio Personalizado**: Si deseas usar tu propio dominio

## Proceso de Despliegue Interactivo

Al ejecutar `./deploy-interactive.sh`, seguirás estos pasos:

1. **Entrada de credenciales**: Ingresa tus credenciales de Cloudflare
2. **Validación**: El sistema verifica que los valores sean correctos
3. **Confirmación**: Revisa y confirma todos los valores antes de continuar
4. **Creación de recursos**: El sistema crea todos los recursos necesarios
5. **Configuración**: Se configuran variables de entorno de forma segura
6. **Despliegue**: Se despliegan todos los componentes
7. **Resumen**: Se proporciona un resumen completo del despliegue

## Recursos Creados

El despliegue completo crea:

- **Proyecto de Pages**: Hosting del frontend
- **Workers**: Backend API y cron jobs
- **KV Namespace**: Almacenamiento de caché
- **D1 Database**: Base de datos SQL para artículos
- **Variables de entorno**: Configuración segura

## Acceso a los Recursos

Después del despliegue:

- **Sitio web**: `https://tu-proyecto.pages.dev`
- **API**: `https://tu-worker.your-account.workers.dev`
- **Panel de admin**: `https://tu-proyecto.pages.dev/admin.html`
- **Health check**: `https://tu-worker.your-account.workers.dev/api/health`

## Seguridad

- Todos los tokens se almacenan de forma segura usando `wrangler secret:put`
- Autenticación JWT para operaciones de administración
- CORS configurado adecuadamente
- Validación de entradas en todos los endpoints

## Solución de Problemas

Si tienes problemas:

1. Asegúrate de tener Wrangler instalado: `npm install -g wrangler`
2. Verifica que tus credenciales de Cloudflare sean correctas
3. Revisa que tengas permisos suficientes en tu cuenta
4. Consulta el archivo `deployment-config.json` generado después del despliegue
5. Revisa los logs en Cloudflare Dashboard

## Prueba Local

Para probar el frontend localmente sin desplegar a Cloudflare:

```bash
# Opción 1: Con http-server
cd public
npx http-server

# Opción 2: Con Python
cd public
python3 -m http.server 8080
```

## Próximos Pasos

Después de un despliegue exitoso:

1. Visita tu sitio web para verificar que todo funciona correctamente
2. Accede al panel de administración con tu token de admin
3. Configura tus categorías iniciales
4. Personaliza el branding si es necesario
5. Configura tu dominio personalizado en Cloudflare Dashboard (si aplica)

¡Tu sitio web de noticias está listo para usar con cualquiera de estas opciones de despliegue!