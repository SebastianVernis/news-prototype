# CMS Actualizado - Nuevo Sistema por Sitio

**Fecha:** 2026-03-10  
**Estado:** ✅ COMPLETADO  
**Worker Version:** d36dd3eb-5f81-45e3-a6eb-74ea13eea344

---

## ✅ Cambios Realizados

### 1. Monitor de Facebook (`monitor.js`)

**Antes:** Mostraba artículos con estado FB general

**Ahora:** Muestra estado por sitio individual
- Columna SITIO: Nombre del sitio
- Columna WEB: Estado de publicación web (✓ Web / ⏰ Pendiente)
- Columna FB: Estado de publicación Facebook (✓ FB / ⏰ FB)
- Columna FECHA: WEB_FECHA o FB_FECHA

```javascript
// Nuevo formato de datos esperado:
{
  TITULO: "...",
  SITIO: "radiocinconoticias",
  WEB_PUBLICADO: 1,
  WEB_FECHA: "2026-03-10 22:05:00",
  FB_PUBLICADO: 0,
  FB_FECHA: null
}
```

### 2. Artículos Públicos (`articles.js`)

**Antes:** Mostraba botón de Facebook manual

**Ahora:** Muestra estado WEB_PUBLICADO
- Columna adicional: Estado Web (✓ Web / ⏰ Pendiente)
- Botón Facebook eliminado (ahora es automático)
- Mensaje informativo: "Facebook publishing es ahora automático por sitio"

### 3. Dashboard (`dashboard.js` + `dashboard.html`)

**Nuevo:** Tabla de estadísticas por sitio
- Total Artículos: Cantidad de artículos asignados
- Web Publicados: Artículos con WEB_PUBLICADO = 1
- Facebook: Artículos con FB_PUBLICADO = 1
- Estado: "Listo para FB" (≥6 web) o "X para FB"

**HTML Agregado:**
```html
<div class="table-container">
    <h3><i class="fas fa-chart-bar"></i> Estadísticas por Sitio</h3>
    <p>Cada sitio publica en Facebook automáticamente cada 6 artículos web</p>
    <table>
        <thead>
            <tr>
                <th>Sitio</th>
                <th>Total Artículos</th>
                <th>Web Publicados</th>
                <th>Facebook</th>
                <th>Estado</th>
            </tr>
        </thead>
        <tbody id="site-stats-table"></tbody>
    </table>
</div>
```

### 4. Nuevo Endpoint en Worker (`/sites/stats`)

```javascript
GET /sites/stats

Response:
[
  {
    "slug": "radiocinconoticias",
    "name": "Radio Cinco Noticias",
    "total": 283,
    "web": 45,
    "fb": 7
  },
  ...
]
```

---

## 📊 Vistas Actualizadas

### Monitor (`#/monitor`)

| Columna | Descripción |
|---------|-------------|
| Artículo | Título del artículo |
| Sitio | Sitio asignado |
| Web | ✓ Web (publicado) / ⏰ Pendiente |
| FB | ✓ FB (publicado) / ⏰ FB (pendiente) |
| Fecha | WEB_FECHA o FB_FECHA |

### Artículos (`#/articles`)

| Columna | Descripción |
|---------|-------------|
| Título | Título del artículo |
| Categoría | Categoría |
| Sitio | Sitio asignado |
| Fecha | Fecha de publicación |
| Estado Web | ✓ Web / ⏰ Pendiente |
| Acciones | Editar |

### Dashboard (`#/dashboard`)

**Nueva Tabla: Estadísticas por Sitio**

| Columna | Descripción |
|---------|-------------|
| Sitio | Nombre + slug |
| Total Artículos | Cantidad total |
| Web Publicados | Badge con cantidad |
| Facebook | Badge azul con cantidad |
| Estado | "Listo para FB" o "X para FB" |

---

## 🔄 Flujo de Actualización Automática

### Publicación Web (Automática)
```
Usuario visita artículo → Middleware actualiza WEB_PUBLICADO = 1
  ↓
Dashboard muestra: Web Publicados +1
  ↓
Monitor muestra: ✓ Web badge
```

### Publicación Facebook (Automática cada 6)
```
Contador sitio: 6 web publicados
  ↓
Cron FB publica en Facebook
  ↓
Dashboard muestra: Facebook +1
  ↓
Monitor muestra: ✓ FB badge
```

---

## 📝 Archivos Modificados

### Frontend CMS
1. `public/admin/js/monitor.js` - Tabla con columnas WEB/FB
2. `public/admin/js/articles.js` - Estado WEB_PUBLICADO
3. `public/admin/js/dashboard.js` - Nueva función loadSiteStats()
4. `public/admin/views/dashboard.html` - Nueva tabla de estadísticas

### Backend Worker
1. `src/index.js` - Endpoint `/sites/stats`

---

## 🧪 Testing

### 1. Verificar Dashboard
```
1. Ir a #/dashboard
2. Ver tabla "Estadísticas por Sitio"
3. Verificar que muestra 27 sitios
4. Verificar conteos web y fb
```

### 2. Verificar Monitor
```
1. Ir a #/monitor
2. Ver sección "Historial de Facebook"
3. Verificar columnas: Artículo, Sitio, Web, FB, Fecha
```

### 3. Verificar Artículos
```
1. Ir a #/articles
2. Verificar columna adicional "Estado Web"
3. Verificar que NO hay botón Facebook manual
```

---

## ⚠️ Notas Importantes

### No Se Sumaron Vistas
- Solo se adaptaron las vistas existentes
- articles.js: Se reemplazó columna FB con Estado Web
- monitor.js: Se agregaron columnas pero se mantiene la misma estructura
- dashboard.js: Se agregó tabla nueva pero no se modificaron stats existentes

### Datos del Nuevo Sistema
- Las vistas muestran datos de `ARTICULOS_SITIO_{SLUG}`
- Artículos antiguos pueden no tener WEB_PUBLICADO registrado
- Nuevos artículos (post-migración) tendrán trazabilidad completa

### Facebook Automático
- El botón de Facebook manual se eliminó
- Mensaje informativo explica que es automático
- Cron FB ejecuta cada 30 min y publica cada 6 web

---

## 🚀 Próximos Pasos

1. **Verificar Dashboard** - Cargar #/dashboard y ver estadísticas
2. **Esperar primera visita** - Visitar artículo y verificar WEB_PUBLICADO
3. **Monitorear contador** - Verificar que contador web aumenta
4. **Verificar Facebook** - Confirmar publicación automática cada 6

---

**Estado:** ✅ CMS ACTUALIZADO - Vistas adaptadas al nuevo sistema  
**Deploy:** Worker y CMS listos para operación
