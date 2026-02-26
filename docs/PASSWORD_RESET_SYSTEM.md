# Sistema de Generación de Contraseñas para Usuarios

Este documento explica cómo generar enlaces seguros para que los usuarios nuevos puedan configurar sus contraseñas.

## Flujo de Trabajo

### 1. El administrador genera un enlace

**Opción A: Usando la interfaz web**

1. Ve a `/admin/generate-password-link.html`
2. Ingresa tu `ADMIN_TOKEN`
3. Ingresa el nombre de usuario para el cual quieres generar el enlace
4. Haz clic en "Generar Link"
5. Copia el enlace generado y envíalo al usuario

**Opción B: Usando la API directamente**

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/auth/generate-password-token \
  -H "Authorization: Bearer TU_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "nombre_usuario"}'
```

Respuesta:
```json
{
  "success": true,
  "token": "uuid-del-token-temporal",
  "expiresAt": "2026-02-24T12:00:00.000Z",
  "setupUrl": "https://www.noticiasobjetivo.click/admin/setup-password.html?user=nombre_usuario&t=uuid-del-token-temporal",
  "message": "Token generado exitosamente. Válido por 24 horas."
}
```

### 2. El usuario recibe el enlace

El enlace tiene esta forma:
```
https://www.noticiasobjetivo.click/admin/setup-password.html?user=nombre_usuario&t=token-temporal
```

### 3. El usuario configura su contraseña

1. El usuario hace clic en el enlace
2. El sistema valida que el token sea válido y no haya expirado
3. El usuario ingresa su nueva contraseña (mínimo 8 caracteres, con mayúsculas, números y carácter especial)
4. El usuario confirma la contraseña
5. Hace clic en "Guardar contraseña"

### 4. Contraseña configurada

Una vez guardada:
- El token temporal se marca como "usado" y ya no puede utilizarse nuevamente
- La contraseña del usuario queda configurada en la base de datos
- El usuario puede iniciar sesión con su nueva contraseña

## Endpoints de la API

### POST /api/auth/generate-password-token

Genera un token temporal para configuración de contraseña.

**Headers:**
- `Authorization: Bearer <ADMIN_TOKEN>`

**Body:**
```json
{
  "username": "nombre_usuario"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "token": "uuid-temporal",
  "expiresAt": "2026-02-24T12:00:00.000Z",
  "setupUrl": "https://dominio.com/admin/setup-password.html?user=nombre&t=token",
  "message": "Token generado exitosamente. Válido por 24 horas."
}
```

**Respuestas de error:**
- `400` - Usuario requerido
- `401` - Token de administrador inválido
- `404` - Usuario no encontrado o inactivo
- `500` - Error interno del servidor

---

### GET /api/auth/validate-password-token

Valida si un token temporal es válido.

**Query params:**
- `user` - Nombre de usuario
- `t` - Token temporal

**Respuesta exitosa (200):**
```json
{
  "valid": true,
  "username": "nombre_usuario"
}
```

**Respuesta de token inválido (404):**
```json
{
  "valid": false,
  "error": "Token inválido o expirado"
}
```

---

### POST /api/auth/setup-password

Establece la contraseña para un usuario. Acepta tanto `ADMIN_TOKEN` como tokens temporales.

**Headers:**
- `Authorization: Bearer <ADMIN_TOKEN_o_TOKEN_TEMPORAL>`

**Body:**
```json
{
  "username": "nombre_usuario",
  "passwordHash": "sha256-hash-de-la-contraseña"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Contraseña configurada correctamente"
}
```

**Respuestas de error:**
- `400` - Usuario y hash de contraseña requeridos
- `401` - Token inválido o expirado (para tokens temporales)
- `404` - Usuario no encontrado o inactivo
- `500` - Error interno del servidor

---

## Seguridad

### Características del sistema:

1. **Tokens temporales**: Los tokens generados expiran después de 24 horas
2. **Un solo uso**: Cada token solo puede utilizarse una vez
3. **Validación del usuario**: El token está vinculado a un usuario específico
4. **Hash SHA-256**: Las contraseñas se almacenan como hash SHA-256 en la base de datos
5. **Requisitos de contraseña**: 
   - Mínimo 8 caracteres
   - Al menos una mayúscula
   - Al menos un número
   - Al menos un carácter especial

### Tabla de la base de datos:

El sistema crea automáticamente la tabla `PASSWORD_RESET_TOKENS`:

```sql
CREATE TABLE PASSWORD_RESET_TOKENS (
  ID TEXT PRIMARY KEY,
  USER_ID TEXT NOT NULL,
  TOKEN TEXT UNIQUE NOT NULL,
  EXPIRES_AT TEXT NOT NULL,
  USED INTEGER DEFAULT 0,
  CREATED_AT TEXT NOT NULL
)
```

## Páginas Web

### /admin/generate-password-link.html

Interfaz para que el administrador genere enlaces de configuración de contraseña.

**Características:**
- Formulario para ingresar ADMIN_TOKEN y username
- Generación del enlace con un clic
- Botón para copiar el enlace al portapapeles
- Instrucciones integradas
- Opción para generar múltiples enlaces

### /admin/setup-password.html

Página que recibe el usuario final para configurar su contraseña.

**Características:**
- Validación automática del token al cargar
- Medidor de fortaleza de contraseña en tiempo real
- Requisitos visuales de contraseña
- Confirmación de contraseña
- Manejo de errores claro
- Redirección a login después del éxito

## Ejemplo de Uso Completo

### Paso 1: Crear usuario (solo admin)

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/auth/users \
  -H "Authorization: Bearer TU_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez", "email": "juan@example.com", "role": "editor"}'
```

### Paso 2: Generar enlace para Juan

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/auth/generate-password-token \
  -H "Authorization: Bearer TU_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez"}'
```

### Paso 3: Enviar enlace a Juan

Copiar el `setupUrl` de la respuesta y enviarlo por email o WhatsApp.

### Paso 4: Juan configura su contraseña

Juan abre el enlace, ingresa su contraseña y la confirma.

### Paso 5: Juan inicia sesión

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez", "password": "su_contraseña"}'
```

## Troubleshooting

### "Token inválido o expirado"

- El token tiene más de 24 horas de antigüedad
- El token ya fue utilizado
- El token fue mal copiado/pegado

**Solución**: Generar un nuevo token desde el panel de administración.

### "Usuario no encontrado o inactivo"

- El usuario no existe en la base de datos
- El usuario está inactivo (ACTIVO = 0)

**Solución**: Verificar que el usuario existe y está activo.

### "Token de administrador inválido"

- El ADMIN_TOKEN es incorrecto
- El ADMIN_TOKEN no está configurado

**Solución**: Verificar el ADMIN_TOKEN en las variables de entorno.

## Variables de Entorno

```env
ADMIN_TOKEN=tu_token_secreto_de_administrador
SITE_URL=https://www.noticiasobjetivo.click
```

- `ADMIN_TOKEN`: Requerido para operaciones administrativas
- `SITE_URL`: Opcional, usado para generar URLs base correctas
