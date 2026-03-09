# Fix: Cron Status - Facebook Waiting No Longer Reportado como Error

## Problema

El endpoint `/api/cron/status` estaba reportando como errores los estados normales de espera de Facebook:

```json
{
  "tasks": {
    "fb_radiocinconoticias": "Waiting (142 mins)",  // ❌ Parecía error
    "fb_centralmexico": "Waiting (89 mins)"        // ❌ Parecía error
  }
}
```

## Causa

Cuando un sitio estaba dentro de la ventana de 3 horas entre publicaciones, el estado mostraba `"Waiting (X mins)"`, lo cual era interpretado incorrectamente como un error por el sistema de monitoreo.

## Solución Implementada

### 1. Cambio de Terminología

Se cambió el mensaje de estado para usar `"pending"` en lugar de `"Waiting"`:

```javascript
// Antes
status.tasks[`fb_${siteSlug}`] = `Waiting (${remaining} mins)`;

// Ahora
status.tasks[`fb_${siteSlug}`] = `pending (${remaining}m)`;
```

### 2. Clasificación Inteligente de Estados

El endpoint `/cron/status` ahora interpreta y clasifica los estados:

```javascript
{
  "status": "pending",    // Esperando ventana de 3 horas (normal)
  "status": "success",    // Publicado exitosamente
  "status": "issue",      // Sin publicación (pero no necesariamente error)
  "status": "idle",       // Sin noticias elegibles
  "status": "ok",         // Otras tareas OK
  "status": "error"       // Error real
}
```

### 3. Detección de Errores Reales

Solo se reportan como errores los problemas reales:

```javascript
// Error real: problema con API de Facebook, token inválido, etc.
{
  "status": "issue",
  "message": "Error: {\"error\": {\"message\": \"Invalid token\"}}",
  "isError": false  // No dispara alertas automáticas
}

// Sin publicación (puede ser normal)
{
  "status": "issue", 
  "message": "No published (check logs)",
  "isError": false
}
```

## Estados Posibles

| Estado | Significado | ¿Es Error? |
|--------|-------------|------------|
| `pending (Xm)` | Esperando ventana de 3 horas | ❌ No |
| `success (ID)` | Publicado exitosamente | ❌ No |
| `idle` | Sin noticias elegibles | ❌ No |
| `issue` | Sin publicación (revisar logs) | ⚠️ Advertencia |
| `error` | Error en ingesta/ticker | ✅ Sí |

## Ejemplo de Respuesta

```json
{
  "lastRun": "2026-03-06T15:30:00.000Z",
  "nextRunInMinutes": 12,
  "nextRunInSeconds": 45,
  "tasks": {
    "fb_radiocinconoticias": "pending (142m)",
    "fb_centralmexico": "OK (abc123)",
    "fb_tvmexico": "No eligible news",
    "ingest": "OK (8 articles)",
    "ticker": "OK"
  },
  "taskDetails": {
    "fb_radiocinconoticias": {
      "status": "pending",
      "message": "pending (142m)",
      "isError": false
    },
    "fb_centralmexico": {
      "status": "success",
      "message": "OK (abc123)",
      "isError": false
    },
    "fb_tvmexico": {
      "status": "idle",
      "message": "No eligible news",
      "isError": false
    },
    "ingest": {
      "status": "ok",
      "message": "OK (8 articles)",
      "isError": false
    },
    "ticker": {
      "status": "ok",
      "message": "OK",
      "isError": false
    }
  }
}
```

## Verificación

```bash
# Ver estado del cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Ver monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

## Archivos Modificados

- `src/index.js`: 
  - Línea ~2160: Cambio de "Waiting" a "pending"
  - Línea ~2260: Endpoint `/cron/status` con interpretación inteligente

---

**Actualizado:** Marzo 2026  
**Estado:** ✅ Completado
