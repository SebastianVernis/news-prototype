# Reporte: Limpieza de Tablas Obsoletas - NexoPress DB

**Fecha:** 2026-03-11  
**Objetivo:** Identificar y planificar eliminación de tablas y columnas obsoletas

---

## 1. Tablas Obsoletas (Para Eliminar)

### 1.1 FACEBOOK_QUEUE ✅ ELIMINADA
- **Registros:** 111 (eliminados)
- **Estado:** ✅ **ELIMINADA** - 2026-03-11
- **Reemplazo:** Timer en KV (`last_fb_post_{slug}`)
- **Acción:** ✅ COMPLETADA

**Código relacionado:**
- `src/routes/facebook.js` - Endpoint `/facebook/queue` (redirige a monitor)
- `src/cron/facebook.js` - Función `processFacebookQueue()` eliminada
- `src/cron/master.js` - Usa `processFBTimer()` en su lugar

### 1.2 ARTICULOS_ORIGINALES ⚠️ POSIBLEMENTE OBSOLETA
- **Registros:** 171
- **Estado:** ⚠️ Verificar si se usa en el flujo actual
- **Flujo actual:** RSS → ARTICULOS_PARAFRASEADOS → ARTICULOS_SITIO_*
- **Acción:** Investigar uso antes de eliminar

### 1.3 REVISION_CONTENIDO ⚠️ POCOS REGISTROS
- **Registros:** 1
- **Estado:** ⚠️ Verificar si la mesa de revisión se usa
- **Acción:** Investigar uso del feature de revisión

---

## 2. Columnas Obsoletas por Eliminar

### 2.1 ARTICULOS_PARAFRASEADOS
| Columna | Estado | Acción |
|---------|--------|--------|
| `SITIO_DESTINO` | ⚠️ En desuso | Mantener por compatibilidad |
| `FB_REQUERIDO` | ✅ Se usa | Mantener |
| `FB_PUBLICADO` | ❌ No existe | N/A |
| `ES_BREVE` | ✅ Se usa | Mantener |

### 2.2 ARTICULOS_CMS
| Columna | Estado | Acción |
|---------|--------|--------|
| `SITIOS_DESTINO` | ✅ Se usa | Mantener |
| `FB_PUBLICADO` | ✅ Se usa | Mantener |
| `FB_FECHA` | ✅ Se usa | Mantener |
| `FB_REQUERIDO` | ✅ Se usa | Mantener |

---

## 3. Tablas ACTIVAS (No tocar)

### 3.1 Principales
| Tabla | Registros | Estado |
|-------|-----------|--------|
| `ARTICULOS_PARAFRASEADOS` | 359 | ✅ ACTIVA |
| `ARTICULOS_CMS` | 11 | ✅ ACTIVA |
| `SITIOS` | 27 | ✅ ACTIVA |

### 3.2 ARTICULOS_SITIO_* (27 tablas)
Todas las tablas por sitio están ACTIVAS y en uso:

**Sitios Estables (10):**
- ✅ ARTICULOS_SITIO_RADIOCINCONOTICIAS
- ✅ ARTICULOS_SITIO_CENTRALMEXICO
- ✅ ARTICULOS_SITIO_TVMEXICO
- ✅ ARTICULOS_SITIO_CBNNOTICIAS
- ✅ ARTICULOS_SITIO_MEXICOINFORMADO
- ✅ ARTICULOS_SITIO_NODOINFORMATIVO
- ✅ ARTICULOS_SITIO_BITACORAURBANA
- ✅ ARTICULOS_SITIO_REPORTECENTRALMX
- ✅ ARTICULOS_SITIO_VERTICENOTICIAS
- ✅ ARTICULOS_SITIO_NOTICIASOBJETIVO

**Sitios Nuevos (17):**
- ✅ ARTICULOS_SITIO_BOOMINFORMATIVO
- ✅ ARTICULOS_SITIO_CAPITALPRESS
- ✅ ARTICULOS_SITIO_DIARIOEXPRESS
- ✅ ARTICULOS_SITIO_ELPULSOMEXICANO
- ✅ ARTICULOS_SITIO_ENFOQUECAPITAL
- ✅ ARTICULOS_SITIO_ENFOQUEDIRECTO
- ✅ ARTICULOS_SITIO_FORMULACDMX
- ✅ ARTICULOS_SITIO_MEXICANTIMES
- ✅ ARTICULOS_SITIO_MEXICO360NOTICIAS
- ✅ ARTICULOS_SITIO_MRADIO
- ✅ ARTICULOS_SITIO_NOTICIASHORIZONTE
- ✅ ARTICULOS_SITIO_PULSODIARIO
- ✅ ARTICULOS_SITIO_PUNTOCLAVE
- ✅ ARTICULOS_SITIO_PUNTONOTICIAS
- ✅ ARTICULOS_SITIO_RADARINFORMATIVO
- ✅ ARTICULOS_SITIO_REPORTEDIARIO
- ✅ ARTICULOS_SITIO_TELEVISIONABC

---

## 4. Plan de Limpieza - ESTADO

### Fase 1: Eliminar FACEBOOK_QUEUE ✅ COMPLETADA
```sql
-- Ejecutado: 2026-03-11
DROP TABLE IF EXISTS FACEBOOK_QUEUE;
```

**Estado:** ✅ COMPLETADA
- Tabla eliminada de D1
- No hay referencias en código
- Worker desplegado

### Fase 2: Investigar ARTICULOS_ORIGINALES ⏳ PENDIENTE
- [ ] Verificar si hay código que inserte en esta tabla
- [ ] Verificar si hay código que lea de esta tabla
- [ ] Si no se usa: migrar datos útiles y DROP

### Fase 3: Investigar REVISION_CONTENIDO ⏳ PENDIENTE
- [ ] Verificar feature de "Mesa de Revisión" en CMS
- [ ] Si no se usa: migrar datos y DROP

### Fase 4: Limpieza de Código ✅ COMPLETADA
- [x] Eliminar imports de `FACEBOOK_QUEUE`
- [x] Eliminar funciones obsoletas (`processFacebookQueue`)
- [x] Actualizar documentación

---

## 5. SITIOS - Dominios Actuales

Todos los 27 sitios tienen dominios configurados con `www.`:

| Slug | Dominio | FB Activo |
|------|---------|-----------|
| radiocinconoticias | www.radiocinconoticias.click | ✅ |
| centralmexico | www.centralmexico.online | ✅ |
| tvmexico | www.tvmexiconews.site | ✅ |
| cbnnoticias | www.cbnnoticias.click | ✅ |
| mexicoinformado | www.mexicoinformado.lat | ✅ |
| nodoinformativo | www.nodoinformativo.lat | ✅ |
| bitacoraurbana | www.bitacoraurbana.lat | ✅ |
| reportecentralmx | www.reportecentral.site | ✅ |
| verticenoticias | www.verticenoticias.today | ✅ |
| noticiasobjetivo | www.noticiasobjetivo.click | ✅ |
| boominformativo | www.boominformativo.top | ✅ |
| capitalpress | www.capitalpress.lat | ✅ |
| diarioexpress | www.diarioexpress.click | ✅ |
| elpulsomexicano | www.elpulsomexicano.lat | ✅ |
| enfoquecapital | www.enfoquecapital.top | ✅ |
| enfoquedirecto | www.enfoquedirecto.lat | ❌ |
| formulacdmx | www.formulacdmx.top | ✅ |
| mexicantimes | www.mexicantimes.top | ✅ |
| mexico360noticias | www.mexico360noticias.click | ✅ |
| mradio | www.mradio.lat | ✅ |
| noticiashorizonte | www.noticiashorizonte.click | ❌ |
| pulsodiario | www.pulsodiario.lat | ✅ |
| puntoclave | www.puntoclave.lat | ✅ |
| puntonoticias | www.puntonoticias.website | ✅ |
| radarinformativo | www.radarinformativo.online | ✅ |
| reportediario | www.reportediario.online | ✅ |
| televisionabc | www.televisionabc.lat | ✅ |

**Nota:** Los dominios con `www.` funcionan correctamente porque el código elimina el `www.` al construir URLs para Facebook.

---

## 6. Recomendaciones - ESTADO

1. ✅ **FACEBOOK_QUEUE eliminada** - Completado el 2026-03-11
2. ⏳ **Mantener ARTICULOS_ORIGINALES** por ahora - Puede tener datos históricos útiles
3. ⏳ **Mantener REVISION_CONTENIDO** - Feature puede ser útil en el futuro
4. ✅ **Dominios actualizados** - Todos sin `www.` (2026-03-11)
5. ✅ **No eliminar columnas de ARTICULOS_PARAFRASEADOS** - Mantener compatibilidad hacia atrás

---

*Reporte generado: 2026-03-11*  
*Última actualización: 2026-03-11 - FACEBOOK_QUEUE eliminada*
