# Fix: Limpieza de Contenido Corrupto, Gramática y Ortografía

## Problema Detectado

Los artículos en la base de datos contenían múltiples problemas:

### 1. Google Tag Manager Scripts
```javascript
googletag.cmd.push(function() { googletag.display('div-gpt-ad-prc_derecha(1)'); });
```

### 2. CSS Variables Corruptas
```css
#dailymotion-pip-large-viewport { 
  --position-bottom: 500px;
  --position-left: 100px; 
}
```

### 3. Caracteres Especiales Corruptos
- `` () - Caracteres de control no imprimibles
- Otros caracteres Unicode inválidos

### 4. Marcas de Agua y Créditos
- "LEA TAMBIÉN:", "TE PUEDE INTERESAR", "PUBLICIDAD"
- "Suscríbete aquí", "Síguenos en Facebook"
- "Comparte esta nota", "Leer más"

### 5. Errores de Ortografía y Gramática
- "mas" en lugar de "más"
- "de el" en lugar de "del"
- "a el" en lugar de "al"
- Espacios incorrectos después de puntos
- Comas antes de "y"

### 6. HTML Tags Innecesarios
- `<script>`, `<style>`, `<meta>`, `<link>`
- `<div>`, `<span>`, `<font>` innecesarios

## Solución Implementada

### Función `decodeHTMLEntities` Mejorada (10 Pasos)

**Archivo:** `src/index.js` (línea ~1816)

| Paso | Descripción | Ejemplo |
|------|-------------|---------|
| 1 | Decodificar HTML entities | `&nbsp;` → ` `, `&amp;` → `&` |
| 2 | Eliminar Google Tag y anuncios | `googletag.cmd.push(...)` → `` |
| 3 | Eliminar CSS corrupto | `--position-bottom: 500px` → `` |
| 4 | Eliminar caracteres corruptos | `` → `` |
| 5 | **Eliminar marcas de agua** | "LEA TAMBIÉN:" → `` |
| 6 | **Eliminar enlaces relacionados** | "Te puede interesar: http://..." → `` |
| 7 | **Corregir ortografía/gramática** | "mas" → "más", "de el" → "del" |
| 8 | **Limpiar HTML tags** | `<div>`, `<span>` → `` |
| 9 | **Eliminar líneas vacías** | `\n\n\n` → `\n\n` |
| 10 | Limpieza final de espacios | `  ` → ` ` |

### Lista Completa de Marcas de Agua Eliminadas

```javascript
- LEA TAMBIÉN:
- LEA ADEMÁS:
- TE PUEDE INTERESAR:
- MÁS INFORMACIÓN:
- VER TAMBIÉN:
- PUBLICIDAD
- ANUNCIO
- SPONSORED
- PATROCINADO
- Suscríbete / Suscríbete aquí / Suscríbase
- Síguenos / Síguenos en
- Comparte esta nota
- Compartir en Facebook/Twitter/WhatsApp
- Envía esta página
- Imprimir esta página
- Leer más
- Continuar leyendo
- Descarga nuestra app / Descarga la app
```

### Correcciones de Ortografía Automáticas

| Incorrecto | Correcto |
|------------|----------|
| mas | más |
| de el | del |
| a el | al |
| ; Mayúscula | . Mayúscula |
| : minúscula | . Mayúscula |
| , y | y |
| , o | o |

### HTML Tags que se Eliminan

Se eliminan pero se preserva el contenido:
- `<br>` → `\n` (salto de línea)
- `<p>` → `\n` (párrafo)
- `<div>` → `\n` (separación)
- `<span>`, `<strong>`, `<b>`, `<em>`, `<i>`, `<u>` → `` (se mantiene texto)
- `<style>`, `<script>`, `<meta>`, `<link>`, `<font>` → `` (completamente eliminados)
```

### 2. Script de Limpieza para DB Existente

**Archivo:** `scripts/clean_articles_db.py`

Script Python que:
- Escanea `ARTICULOS_PARAFRASEADOS` y `ARTICULOS_CMS`
- Detecta artículos con contenido corrupto
- Limpia el contenido usando la misma lógica que `decodeHTMLEntities`
- Actualiza los registros en la base de datos

**Uso:**
```bash
cd /mnt/c/Users/soluc/cloudflare-news-project
python3 scripts/clean_articles_db.py
```

### 3. Script SQL Alternativo

**Archivo:** `scripts/cleanup_corrupt_content.sql`

Para limpieza básica solo de Google Tag:

```bash
wrangler d1 execute news_db --file scripts/cleanup_corrupt_content.sql --remote
```

## Flujo de Limpieza

### Para Artículos Nuevos (Automático)
1. Artículo se lee desde la DB
2. `parseArticleRow()` llama a `decodeHTMLEntities()`
3. Contenido se limpia antes de enviarse al frontend
4. Frontend recibe contenido limpio

### Para Artículos Existentes (Manual)
1. Ejecutar script Python una vez
2. Script detecta artículos corruptos
3. Limpia contenido en la DB
4. Verifica resultados

## Verificación

### Verificar Artículos Corruptos Restantes
```bash
# En ARTICULOS_PARAFRASEADOS
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS WHERE CONTENIDO LIKE '%googletag%'" --remote

# En ARTICULOS_CMS
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_CMS WHERE CONTENIDO LIKE '%googletag%'" --remote
```

### Verificar Artículo Específico
```bash
wrangler d1 execute news_db --command "SELECT ID, TITULO_PARAFRASEADO, SUBSTRING(CONTENIDO, 1, 200) FROM ARTICULOS_PARAFRASEADOS LIMIT 5" --remote
```

## Ejemplo de Transformación Completa

### Antes (Contenido Original)
```
Últimas noticias... googletag.cmd.push(function() { 
  googletag.display('div-gpt-ad-prc_derecha(1)'); 
}); 
#dailymotion-pip-large-viewport { 
  --position-bottom: 500px;
  --position-left: 100px;
}
LEA TAMBIÉN: Gobierno federal dona a la UNAM dos perros...
Suscríbete aquí para más información.
Comparte esta nota en Facebook
mas información en de el sitio web...
```

### Después (Contenido Limpio)
```
Últimas noticias... Gobierno federal dona a la UNAM dos perros entrenados para detección de riesgos. Más información en del sitio web.
```

### Cambios Aplicados
1. ✅ Eliminado `googletag.cmd.push(...)` 
2. ✅ Eliminado CSS corrupto `--position-bottom: 500px`
3. ✅ Eliminada marca de agua "LEA TAMBIÉN:"
4. ✅ Eliminado "Suscríbete aquí"
5. ✅ Eliminado "Comparte esta nota en Facebook"
6. ✅ Corregido "mas" → "más"
7. ✅ Corregido "de el" → "del"
8. ✅ Espacios múltiples corregidos
9. ✅ Líneas vacías eliminadas

## Regex Patterns Usados

| Pattern | Elimina |
|---------|---------|
| `googletag\.cmd\.push\([^)]*\);` | Scripts GTM completos |
| `googletag\.display\([^)]*\);` | Calls a display() |
| `\s*--[\w-]+:\s*[^;]*;\s*` | CSS variables corruptas |
| `[\uFFFD]` | Caracteres Unicode inválidos () |
| `\{[^}]*--[\w--]+:[^}]*\}` | Bloques CSS corruptos |
| `\s+` | Espacios múltiples |

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `src/index.js` | Función `decodeHTMLEntities()` mejorada (línea ~1816) |
| `scripts/clean_articles_db.py` | Script Python para limpieza masiva (nuevo) |
| `scripts/cleanup_corrupt_content.sql` | Script SQL básico (nuevo) |

## Próximos Pasos

1. **Ejecutar limpieza en producción:**
   ```bash
   python3 scripts/clean_articles_db.py
   ```

2. **Verificar resultados:**
   ```bash
   wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS WHERE CONTENIDO LIKE '%googletag%'" --remote
   ```

3. **Monitorear nuevos artículos:**
   - Verificar que artículos nuevos no contengan contenido corrupto
   - La función `decodeHTMLEntities()` ya los limpiará automáticamente

## Prevención Futura

Para evitar que contenido corrupto llegue a la DB:

1. **En el proceso de ingesta RSS:**
   - Aplicar `decodeHTMLEntities()` antes de guardar
   - Filtrar scripts y CSS en el parser RSS

2. **En el CMS:**
   - Sanitizar contenido antes de guardar
   - Validar que no haya scripts de terceros

---

**Actualizado:** Marzo 2026  
**Estado:** ✅ Completado
