# Sistema de Links para Generar Contraseña

## Resumen

Se ha implementado un sistema completo para que los administradores puedan generar enlaces seguros y temporales para que los usuarios nuevos configuren sus contraseñas.

## Archivos Creados/Modificados

### Backend (API)

**`src/index.js`** - Nuevos endpoints:
- `POST /api/auth/generate-password-token` - Genera token temporal (24h)
- `GET /api/auth/validate-password-token` - Valida token temporal
- `POST /api/auth/setup-password` - Ahora acepta tokens temporales además del ADMIN_TOKEN

### Frontend (Admin)

**`public/admin/generate-password-link.html`**
- Página independiente para generar links
- Interfaz simple y directa
- No requiere login, solo ADMIN_TOKEN

**`public/admin/setup-password.html`** (modificado)
- Ahora valida el token con el backend
- Usa token temporal en lugar de adminToken
- Mejoras en la validación de contraseña

**`public/admin/index.html`** (modificado)
- Agregado menú "Usuarios"
- Referencia al script users.js

**`public/admin/js/users.js`** (nuevo)
- Módulo para gestión de usuarios
- Generación de links desde el modal
- Listado de usuarios

**`public/admin/views/users.html`** (nuevo)
- Vista para la sección de Usuarios
- Tabla de usuarios con acciones
- Modal para generar links

**`public/admin/css/admin.css`** (modificado)
- Estilos para la página de usuarios
- Estilos para modales
- Estilos para badges y alertas

**`public/admin/js/router.js`** (modificado)
- Soporte para vista 'users'

### Documentación

**`docs/PASSWORD_RESET_SYSTEM.md`**
- Documentación completa del sistema
- Endpoints de la API
- Ejemplos de uso
- Consideraciones de seguridad

**`docs/QUICK_START_PASSWORD_LINK.md`**
- Guía rápida de inicio
- Pasos simples para generar links

## Flujo de Uso

### Opción 1: Desde el Panel de Administración (Recomendado)

1. Inicia sesión en `/admin/`
2. Ve a "Usuarios" en el menú
3. Haz clic en "Generar Link de Contraseña" junto al usuario
4. Copia el link generado
5. Envía el link al usuario

### Opción 2: Página Directa

1. Ve a `/admin/generate-password-link.html`
2. Ingresa tu ADMIN_TOKEN
3. Ingresa el nombre de usuario
4. Haz clic en "Generar Link"
5. Copia y envía el link

### Opción 3: API Directamente

```bash
curl -X POST "https://news-api.sebastianvernis.workers.dev/api/auth/generate-password-token" \
  -H "Authorization: Bearer TU_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez"}'
```

## Características de Seguridad

✅ **Tokens temporales**: Vencen a las 24 horas
✅ **Un solo uso**: Se invalidan después de usarse
✅ **Vinculados al usuario**: Cada token es específico para un usuario
✅ **Validación en backend**: El token se verifica contra la base de datos
✅ **Contraseñas seguras**: Requisitos mínimos de fortaleza
✅ **Hash SHA-256**: Las contraseñas se almacenan encriptadas

## Requisitos de Contraseña

- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos un número
- Al menos un carácter especial

## Endpoints de la API

| Método | Endpoint | Descripción | Auth Requerida |
|--------|----------|-------------|----------------|
| POST | `/api/auth/generate-password-token` | Genera token temporal | ADMIN_TOKEN |
| GET | `/api/auth/validate-password-token` | Valida token | Ninguna |
| POST | `/api/auth/setup-password` | Establece contraseña | ADMIN_TOKEN o Token Temporal |
| GET | `/api/auth/users` | Lista usuarios | ADMIN_TOKEN |
| POST | `/api/auth/users` | Crea usuario | ADMIN_TOKEN |
| POST | `/api/auth/login` | Login | Ninguna |

## Base de Datos

El sistema crea automáticamente la tabla `PASSWORD_RESET_TOKENS`:

```sql
CREATE TABLE IF NOT EXISTS PASSWORD_RESET_TOKENS (
  ID TEXT PRIMARY KEY,
  USER_ID TEXT NOT NULL,
  TOKEN TEXT UNIQUE NOT NULL,
  EXPIRES_AT TEXT NOT NULL,
  USED INTEGER DEFAULT 0,
  CREATED_AT TEXT NOT NULL
)
```

## URLs Importantes

| Página | URL |
|--------|-----|
| Generar Link (página directa) | `/admin/generate-password-link.html` |
| Configurar Contraseña (usuario) | `/admin/setup-password.html?user=USERNAME&t=TOKEN` |
| Gestión de Usuarios (admin) | `/admin/#users` |

## Próximos Pasos Sugeridos

1. **Deploy**: Subir los cambios a Cloudflare Workers
2. **Migración**: Ejecutar SQL para crear tabla PASSWORD_RESET_TOKENS (si es necesario)
3. **Pruebas**: Probar el flujo completo con un usuario de prueba
4. **Comunicación**: Informar al equipo sobre la nueva funcionalidad

## Comandos Útiles

```bash
# Deploy del worker
npx wrangler deploy src/index.js --name news-api

# Deploy del admin (Pages)
npx wrangler pages deploy ./public --project-name=your-project-name

# Test local del API
npx wrangler dev src/index.js --port 8787
```

## Troubleshooting

### "Token inválido o expirado"
- El token tiene más de 24 horas
- El token ya fue usado
- El token se copió mal

**Solución**: Generar nuevo token

### "Usuario no encontrado"
- El usuario no existe en la BD
- El usuario está inactivo

**Solución**: Verificar en la tabla USUARIOS

### Error 401 en generate-password-token
- ADMIN_TOKEN incorrecto
- ADMIN_TOKEN no configurado

**Solución**: Verificar variables de entorno

## Contacto

Para soporte o preguntas sobre esta funcionalidad, revisar la documentación completa en:
- `docs/PASSWORD_RESET_SYSTEM.md` - Documentación técnica completa
- `docs/QUICK_START_PASSWORD_LINK.md` - Guía rápida
