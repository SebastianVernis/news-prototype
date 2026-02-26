# Guía Rápida: Generar Link para Usuario Nuevo

## ¿Qué necesitas?

- Tu `ADMIN_TOKEN`
- El nombre de usuario de la persona que va a recibir el link

## Método 1: Interfaz Web (Recomendado)

1. **Ve a la página de generación:**
   ```
   https://www.noticiasobjetivo.click/admin/generate-password-link.html
   ```

2. **Completa el formulario:**
   - Ingresa tu `ADMIN_TOKEN`
   - Ingresa el nombre de usuario (ej: `juan.perez`)

3. **Genera el link:**
   - Haz clic en "Generar Link"
   - Copia el link generado

4. **Envía el link al usuario:**
   - Por email, WhatsApp, etc.
   - El link es válido por 24 horas

## Método 2: API Directamente

```bash
# Generar token
curl -X POST "https://news-api.sebastianvernis.workers.dev/api/auth/generate-password-token" \
  -H "Authorization: Bearer TU_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "juan.perez"}'
```

El response incluirá un `setupUrl` que puedes enviar al usuario.

## ¿Qué pasa después?

1. El usuario recibe el link
2. Hace clic en el link
3. El sistema valida que el token sea válido
4. El usuario crea su contraseña (mínimo 8 caracteres con mayúsculas, números y carácter especial)
5. El usuario confirma la contraseña
6. ¡Listo! Ya puede iniciar sesión

## Endpoints Relacionados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/auth/generate-password-token` | POST | Genera token temporal |
| `/api/auth/validate-password-token` | GET | Valida token temporal |
| `/api/auth/setup-password` | POST | Establece contraseña |
| `/api/auth/login` | POST | Login de usuario |

## Archivos Creados

- **Backend:** `src/index.js` (endpoints agregados)
- **Admin UI:** `public/admin/generate-password-link.html` (generador de links)
- **User UI:** `public/admin/setup-password.html` (página que usa el usuario)
- **Docs:** `docs/PASSWORD_RESET_SYSTEM.md` (documentación completa)

## Seguridad

- ✅ Tokens temporales (24 horas)
- ✅ Un solo uso por token
- ✅ Vinculado a usuario específico
- ✅ Contraseñas con hash SHA-256
- ✅ Requisitos de fortaleza de contraseña
