# Flujo Progresivo para Cierre de Testing Full (API + UI) en `sites/Nuevos`

Este documento quedó estructurado en **flujo por sesiones y checklist por sitio** para ejecutar el cierre total de pruebas de forma controlada y trazable.

---

## 0) Objetivo y regla de ejecución

Validar al 100% cada sitio de `sites/Nuevos` en:
1. API full (happy/error/edge)
2. UI full (home/artículo/categoría, navegación y responsive)

**Regla**: no pasar al siguiente sitio hasta cerrar checklist del sitio actual.

---

## 1) Inventario de sitios y sesiones

### 1.1 Sitios objetivo
1. boominformativo  
2. capitalpress  
3. diarioexpress  
4. elpulsomexicano  
5. enfoquecapital  
6. enfoquedirecto  
7. formulacdmx  
8. mexicantimes  
9. mexico360noticias  
10. mradio  
11. noticiashorizonte  
12. pulsodiario  
13. puntoclave  
14. puntonoticias  
15. radarinformativo  
16. reportediario  
17. televisionabc  

### 1.2 Plan de sesiones (progresivo)
- **Sesión 1**: sitios 1–3 (baseline ya tocado)
- **Sesión 2**: sitios 4–7
- **Sesión 3**: sitios 8–11
- **Sesión 4**: sitios 12–14
- **Sesión 5**: sitios 15–17
- **Sesión 6**: consolidación final + reporte maestro

---

## 2) Pre-check obligatorio por sesión

Antes de iniciar una sesión:

- [ ] Entorno HTTP activo (no `file://`)
- [ ] API base accesible: `https://news-api.sebastianvernis.workers.dev/api/articles`
- [ ] Para cada sitio de la sesión existen:
  - [ ] `articulo/index.html`
  - [ ] `categoria/index.html` (si aplica)
  - [ ] `components.js`
- [ ] Marcadores de hidratación presentes:
  - [ ] `Error loading article:`
  - [ ] `Category render error:`

Si algo falla aquí, **no iniciar pruebas UI**; corregir primero.

---

## 3) Flujo exacto por sitio (plantilla de sesión)

Para cada `<site>` ejecutar este orden exacto:

### Paso A — API Full del sitio
- [ ] A1. Listado:
  - `curl ".../api/articles?site=<site>&limit=3"`
- [ ] A2. Categoría nacional:
  - `curl ".../api/articles?site=<site>&category=nacional&limit=3"`
- [ ] A3. Categoría tecnologia:
  - `curl ".../api/articles?site=<site>&category=tecnologia&limit=3"`
- [ ] A4. Extraer `slug_real` del listado:
  - `curl ".../api/articles?site=<site>&limit=1"`
- [ ] A5. Detalle por slug real:
  - `curl ".../api/articles/<slug_real>"`
- [ ] A6. Error path slug inexistente:
  - `curl ".../api/articles/slug-inexistente-prueba-404"`
- [ ] A7. Edge case categoría inexistente:
  - `curl ".../api/articles?site=<site>&category=zzzz-no-existe&limit=3"`

**Resultado API sitio**:
- [ ] PASS API `<site>`
- [ ] FAIL API `<site>` (anotar bug)

---

### Paso B — UI Full del sitio
Abrir en HTTP:

- [ ] B1. Home `.../sites/Nuevos/<site>/index.html`
  - [ ] sin errores JS bloqueantes
  - [ ] layout intacto (sin romper paleta/estilo)
- [ ] B2. Artículo válido `.../articulo/index.html?slug=<slug_real>`
  - [ ] loading -> content
  - [ ] title/category/author/date render
  - [ ] imagen (visible o oculta sin romper)
- [ ] B3. Artículo inválido `slug-inexistente-prueba-404`
  - [ ] muestra estado error
- [ ] B4. Categoría válida `.../categoria/index.html?cat=nacional`
  - [ ] loading -> cards o estado vacío válido
  - [ ] links a artículo correctos
- [ ] B5. Categoría inválida `.../categoria/index.html?cat=zzzz-no-existe`
  - [ ] estado error/no-results
- [ ] B6. Navegación
  - [ ] home -> categoría -> artículo -> volver
- [ ] B7. Responsive
  - [ ] desktop
  - [ ] tablet
  - [ ] mobile
  - [ ] sin overflow horizontal ni solapes

**Resultado UI sitio**:
- [ ] PASS UI `<site>`
- [ ] FAIL UI `<site>` (anotar bug)

---

### Paso C — Cierre del sitio
- [ ] C1. Si API/UI PASS: marcar sitio como **Completado**
- [ ] C2. Si FAIL: abrir ticket de corrección + re-test solo del sitio
- [ ] C3. Registrar evidencia (capturas/log/resultado curl)

---

## 4) Checklist maestro por sitio (tracking rápido)

- [ ] boominformativo
- [ ] capitalpress
- [ ] diarioexpress
- [ ] elpulsomexicano
- [ ] enfoquecapital
- [ ] enfoquedirecto
- [ ] formulacdmx
- [ ] mexicantimes
- [ ] mexico360noticias
- [ ] mradio
- [ ] noticiashorizonte
- [ ] pulsodiario
- [ ] puntoclave
- [ ] puntonoticias
- [ ] radarinformativo
- [ ] reportediario
- [ ] televisionabc

---

## 5) Plantilla de bitácora por sesión

Crear/actualizar:
- `docs/REPORTE_TESTING_FULL_NUEVOS.md`

Usar este bloque por sesión:

```md
## Sesión X (fecha)

### Sitios de la sesión
- sitio-a
- sitio-b
- sitio-c

### Resultado por sitio
#### sitio-a
- API: ✅/❌
- UI: ✅/❌
- Responsive: ✅/❌
- Bugs:
- Evidencia:

#### sitio-b
- API: ✅/❌
- UI: ✅/❌
- Responsive: ✅/❌
- Bugs:
- Evidencia:

### Cierre sesión
- Sitios cerrados:
- Sitios pendientes:
- Riesgos:
- Próxima sesión:
```

---

## 6) Reglas de reproceso (cuando algo falle)

- [ ] Corregir solo archivos del sitio afectado
- [ ] Repetir Paso A + Paso B completos del sitio
- [ ] Si pasa, actualizar checklist maestro
- [ ] Si no pasa, escalar con evidencia y bloquear cierre global

---

## 7) Criterio de cierre final global

Solo cerrar cuando:

- [ ] 17/17 sitios marcados PASS en checklist maestro
- [ ] API full PASS en todos
- [ ] UI full PASS en todos
- [ ] Responsive base PASS en todos
- [ ] Reporte completo en `docs/REPORTE_TESTING_FULL_NUEVOS.md`
- [ ] Sin alteración de paleta/identidad visual por sitio

---

## 8) Comandos base rápidos

```bash
# listado
curl "https://news-api.sebastianvernis.workers.dev/api/articles?site=<site>&limit=3"

# categoría
curl "https://news-api.sebastianvernis.workers.dev/api/articles?site=<site>&category=nacional&limit=3"

# obtener slug real
curl "https://news-api.sebastianvernis.workers.dev/api/articles?site=<site>&limit=1"

# detalle
curl "https://news-api.sebastianvernis.workers.dev/api/articles/<slug_real>"

# error slug
curl "https://news-api.sebastianvernis.workers.dev/api/articles/slug-inexistente-prueba-404"
```

---

Documento reestructurado en flujo progresivo por sesiones + checklist por sitio.
