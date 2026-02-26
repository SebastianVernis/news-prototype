# Guía de Despliegue Completo

## Descripción

El script `deploy-full.sh` automatiza el despliegue completo del proyecto Cloudflare News a través de múltiples pasos:

1. **Validación de Base de Datos** - Compara estado local vs remoto
2. **Gestión Interactiva de Usuarios** - CRUD completo de usuarios
3. **Worker de API** - Despliega el backend
4. **CMS (Admin)** - Despliega el panel de administración
5. **Sitios** - Despliega los 10 sitios estáticos

## Uso

```
bash
bash scripts/deploy/deploy-full.sh
```

## Requisitos

- Wrangler CLI instalado (`npm install -g wrangler`)
- Sesión activa en Cloudflare (`wrangler login`)
- Base de datos D1 configurada en `src/wrangler.toml`

## Pasos del Despliegue

### 0. Validación de Base de Datos

El script muestra automáticamente el estado de la base de datos:

- Artículos parafaseados
- Artículos CMS
- Sitios registrados
- Categorías
- Usuarios

También muestra listas completas de:
- Usuarios (ID, nombre, email, rol, estado)
- Sitios (ID, nombre, slug, URL, estado)
- Artículos CMS (ID, título, sitio, categoría, estado)

#### Opciones de Sincronización

```
   1. Ver artículos parafraseados
   2. Ver artículos CMS
   3. Sincronizar desde archivos SQL locales
   0. Continuar con gestión de usuarios
```

**Sincronización**: El script busca archivos SQL en `data/*.sql` y los ejecuta en la base de datos remota.

### 1. Gestión de Usuarios (Interactivo)

Antes del despliegue, puedes gestionar usuarios:

```
   ┌─────────────────────────────────┐
   │  MENÚ DE GESTIÓN DE USUARIOS   │
   ├─────────────────────────────────┤
   │  1. Listar usuarios             │
   │  2. Crear usuario               │
   │  3. Editar usuario              │
   │  4. Eliminar usuario            │
   │  5. Activar usuario             │
   │  0. Continuar con despliegue    │
   └─────────────────────────────────┘
```

#### 1. Listar usuarios
Muestra todos los usuarios con su ID, nombre, email, rol, estado y fecha de creación.

#### 2. Crear usuario
Crea un nuevo usuario solicitando:
- Nombre de usuario
- Email
- Rol (admin/editor)

#### 3. Editar usuario
Edita un usuario existente:
- ID del usuario a editar
- Nuevo nombre (opcional)
- Nuevo email (opcional)
- Nuevo rol (admin/editor, opcional)
- Estado activo (1=si, 0=no, opcional)

#### 4. Eliminar usuario
Elimina un usuario por ID. Requiere confirmación escribiendo "SI".

#### 5. Activar usuario
Activa un usuario existente (establece ACTIVO=1).

### 2. Worker de API

Despliega el worker desde `src/` a Cloudflare Workers.

### 3. CMS (Admin)

Despliega el panel de administración desde `public/` a Cloudflare Pages.

### 4. Sitios

Despliega los 10 sitios a sus proyectos de Cloudflare Pages:
- radiocinconoticias
- centralmexico
- tvmexico
- cbnnoticias
- mexicoinformado
- nodoinformativo
- bitacoraurbana
- reportecentralmx
- verticenoticias
- noticiasobjetivo

## Salida

El script genera un archivo `DEPLOY_URLS.txt` con todas las URLs desplegadas.

## Solución de Problemas

### Error: wrangler no está instalado
```
bash
npm install -g wrangler
```

### Error: No se encontró database_id
Asegúrate de tener configurado el `database_id` en `src/wrangler.toml`

### Error al desplegar sitios
Verifica que el directorio del sitio exista en `sites/`

### Error al ejecutar comandos D1
Verifica que la base de datos D1 esté correctamente configurada y que tengas permisos.
