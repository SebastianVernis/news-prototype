# Mejoras de Calidad en Generación de Artículos

**Fecha de implementación:** 2026-01-20  
**Objetivo:** Garantizar calidad profesional en todos los artículos generados

---

## 🎯 Objetivo de las Mejoras

Asegurar que TODOS los artículos generados en TODOS los sitios tengan:

1. **Párrafos correctamente separados** (no bloques de texto)
2. **Gramática y puntuación impecable**
3. **Estructura narrativa profesional**
4. **Longitud y formato adecuados**

---

## 📝 Especificaciones de Calidad

### Estructura de Párrafos

- **Cantidad:** 8-12 párrafos por artículo
- **Separación:** Doble salto de línea (`\n\n`) entre párrafos
- **Longitud:** 80-150 palabras por párrafo
- **Oraciones:** 3-5 oraciones por párrafo
- **Formato HTML:** Cada párrafo en su propio tag `<p>`

### Gramática y Puntuación

- **Puntos (.)** - Terminar oraciones completas
- **Comas (,)** - Separar ideas dentro de oraciones
- **Punto y coma (;)** - Conectar ideas relacionadas
- **Dos puntos (:)** - Antes de listas o explicaciones
- **Longitud de oraciones:** Máximo 30-35 palabras
- **Concordancia:** Género y número correctos

### Calidad Editorial

- **Tono:** Periodístico profesional
- **Estilo:** Apropiado para lectores informados
- **Vocabulario:** Rico pero accesible
- **Transiciones:** Lógicas entre párrafos
- **Primer párrafo:** Con clase `lead` para destacar

---

## 🔧 Archivos Modificados

### 1. `core/scripts/paraphrase.py`

**Cambios principales:**

```python
# ANTES: Prompt básico
prompt = f"""Eres un periodista especializado en política. Reescribe..."""

# DESPUÉS: Prompt detallado con instrucciones de formato
prompt = f"""Eres un periodista senior especializado en política...

INSTRUCCIONES CRÍTICAS DE FORMATO Y CALIDAD:

1. ESTRUCTURA DE PÁRRAFOS (MUY IMPORTANTE):
   - Escribe 8-12 párrafos SEPARADOS con doble salto de línea
   - Cada párrafo: 3-5 oraciones (100-150 palabras)
   - NUNCA escribas todo en un solo bloque
   ...

2. GRAMÁTICA Y PUNTUACIÓN:
   - Usa puntos (.) para terminar oraciones
   - Usa comas (,) correctamente
   ...
```

**System message mejorado:**

```python
"content": "Eres un periodista senior de un medio prestigioso con excelente 
            dominio del español. Escribes artículos profundos, bien investigados 
            y con autoridad. SIEMPRE separas el contenido en párrafos distintos 
            usando doble salto de línea. Tienes impecable gramática, puntuación 
            y estructura narrativa."
```

**Tokens aumentados:**
- ANTES: `max_tokens: 3000`
- DESPUÉS: `max_tokens: 4000`

**Timeout ajustado:**
- Línea 102: `timeout=90` (ya estaba correcto)

---

### 2. `core/scripts/article-expander.py`

**Cambios principales:**

```python
# ANTES: Instrucciones simples
INSTRUCCIONES ESPECÍFICAS:
1. Estructura: Usa un enfoque de {structure}
2. Divide en 5-7 párrafos bien estructurados
...

# DESPUÉS: Instrucciones detalladas
INSTRUCCIONES CRÍTICAS DE FORMATO Y CALIDAD:

1. ESTRUCTURA DE PÁRRAFOS (MUY IMPORTANTE):
   - Escribe 8-10 párrafos SEPARADOS con doble salto de línea
   - NUNCA escribas todo en un solo bloque
   ...

2. GRAMÁTICA Y PUNTUACIÓN:
   [Reglas detalladas]
   ...
```

**Limpieza de markdown:**

```python
# Nuevo: Remover markdown headers (#)
lines = expanded.split('\n')
cleaned_lines = []
for line in lines:
    if line.strip().startswith('#'):
        cleaned_lines.append(line.lstrip('#').strip())
    else:
        cleaned_lines.append(line)
```

**Tokens aumentados:**
- ANTES: `max_tokens: 2000`
- DESPUÉS: `max_tokens: 3000`

**Timeout ajustado:**
- Línea 156: `timeout=90` (actualizado desde 45s)

---

### 3. `core/scripts/master_orchestrator.py`

**Verificado y correcto:**

```python
# Línea 667: Método _formatear_contenido_html
parrafos = texto.strip().split('\n\n')  # ✅ Usa \n\n correctamente

# Línea 678-681: Renderizado HTML
if i == 0:
    html_parrafos.append(f'<p class="lead">{parrafo}</p>')
else:
    html_parrafos.append(f'<p>{parrafo}</p>')
```

**No requiere cambios** - Ya implementa correctamente:
- División por `\n\n`
- Limpieza de espacios múltiples
- Tags `<p>` individuales
- Clase `lead` para primer párrafo

---

### 4. `core/scripts/servir_ejemplos.py`

**Error corregido:**

```python
# ANTES (línea 300): String literal
split('\\n\\n')  # ❌ No funcionaba

# DESPUÉS:
split('\n\n')    # ✅ Salto de línea real
```

**CSS ya correcto:**

```css
.article-text p {
    margin-bottom: 1.5rem;
    text-align: justify;
}
```

---

## 📊 Resultados de Tests

### Test de Calidad (`test_calidad_parrafos.py`)

**NewsParaphraser:**
- ✅ 12 párrafos generados
- ✅ Promedio 101.6 palabras/párrafo
- ✅ Promedio 4.0 oraciones/párrafo
- ✅ Usa doble salto de línea
- ✅ **PASS**

**ArticleExpander:**
- ✅ 10 párrafos generados
- ✅ Usa doble salto de línea
- ⚠️ Primer párrafo puede ser título (se limpia con regex)
- ✅ Resto de párrafos con buena estructura

---

## 🌐 Flujo Completo de Generación

### Paso 1: Descarga de Noticias
```
newsapi.py → noticias originales
```

### Paso 2: Parafraseo (NewsParaphraser)
```
Input:  Noticia original (200-400 palabras)
Output: Artículo parafraseado (1,500-2,000 palabras)
        - 12 párrafos bien separados
        - Gramática profesional
        - Formato: full_text con \n\n
```

### Paso 3: Expansión (ArticleExpander) [OPCIONAL]
```
Input:  Artículo parafraseado
Output: Artículo expandido (800-1,200 palabras)
        - 8-10 párrafos
        - Estructura específica aplicada
```

### Paso 4: Generación HTML (master_orchestrator)
```
Input:  full_text con \n\n
Process: _formatear_contenido_html()
         - split('\n\n')
         - Wrap en <p> tags
         - Primer párrafo: <p class="lead">
Output: HTML con párrafos correctamente renderizados
```

---

## ✅ Checklist de Verificación

Para cada artículo generado, verificar:

- [ ] Tiene 8-12 párrafos separados
- [ ] Cada párrafo está en su propio tag `<p>`
- [ ] Primer párrafo tiene clase `lead`
- [ ] Separación visual clara en el navegador
- [ ] Puntuación correcta al final de cada oración
- [ ] Sin bloques de texto monolíticos
- [ ] Longitud de párrafos entre 80-150 palabras
- [ ] 3-5 oraciones por párrafo
- [ ] Gramática y ortografía correctas
- [ ] Tono periodístico profesional

---

## 🧪 Comandos de Testing

### Test rápido de parafraseo
```bash
python3 core/scripts/test/test_paraphrase_quick.py
```

### Test completo de calidad
```bash
python3 core/scripts/test/test_calidad_parrafos.py
```

### Test de timeouts y endpoint
```bash
python3 core/scripts/test/test_api_timeout.py
```

### Generar 2 ejemplos completos
```bash
python3 core/scripts/generar_2_ejemplos.py
```

### Servir ejemplos en navegador
```bash
python3 core/scripts/servir_ejemplos.py
# Visitar: http://localhost:8001 y http://localhost:8002
```

---

## 🎓 Ejemplos de Calidad

### Ejemplo 1: José Woldenberg (Puerto 8001)

**Estadísticas:**
- Párrafos: 12
- Palabras totales: 1,683
- Promedio palabras/párrafo: 140
- Oraciones/párrafo: 3-4

**Primer párrafo:**
```
El destacado politólogo y expresidente del Instituto Federal Electoral (IFE), 
José Woldenberg Karakowsky, ha lanzado una advertencia contundente sobre los 
riesgos que enfrenta la democracia mexicana en el contexto de una eventual 
reforma electoral impulsada por la llamada Cuarta Transformación. En una 
entrevista para el programa La Silla Roja de El Financiero Televisión...
```

**Renderizado HTML:**
```html
<p class="lead">El destacado politólogo...</p>
<p>Woldenberg Karakowsky expresó...</p>
<p>El expresidente del IFE realizó...</p>
...
```

### Ejemplo 2: Trump orden mundial (Puerto 8002)

**Estadísticas:**
- Párrafos: 12
- Palabras totales: 1,289
- Promedio palabras/párrafo: 107
- Oraciones/párrafo: 3-4

---

## 🔄 Proceso de Mejora Continua

### Si se detectan problemas:

1. **Ejecutar tests de calidad**
   ```bash
   python3 core/scripts/test/test_calidad_parrafos.py
   ```

2. **Revisar configuración de prompts**
   - `core/scripts/paraphrase.py` líneas 55-115
   - `core/scripts/article-expander.py` líneas 87-145

3. **Verificar renderizado HTML**
   - `core/scripts/master_orchestrator.py` línea 667 (`_formatear_contenido_html`)
   - Templates HTML en `core/scripts/servir_ejemplos.py`

4. **Ajustar parámetros si es necesario**
   - `max_tokens`: 4000 (paraphrase), 3000 (expander)
   - `temperature`: 0.7 (balance creatividad/coherencia)
   - `timeout`: 90s (ambos módulos)

---

## 📚 Referencias

- **Documentación Blackbox API:** https://docs.blackbox.ai/api-reference
- **Análisis de timeouts:** `docs/testing/ANALISIS-PARAFRASEO-TIMEOUT.md`
- **Estructura del proyecto:** `ESTRUCTURA-PROYECTO.md`

---

## ✨ Próximos Pasos

1. ✅ Implementar mejoras en paraphrase.py
2. ✅ Implementar mejoras en article-expander.py
3. ✅ Verificar master_orchestrator.py
4. ✅ Corregir servir_ejemplos.py
5. ✅ Crear tests de calidad
6. ⏳ Generar sitio completo de prueba
7. ⏳ Verificar calidad en producción
8. ⏳ Documentar mejores prácticas

---

**Última actualización:** 2026-01-20 02:45:00  
**Estado:** ✅ Implementado y verificado  
**Próxima revisión:** Después de generar primer sitio completo
