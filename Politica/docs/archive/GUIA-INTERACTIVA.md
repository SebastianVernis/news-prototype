# 🎮 Guía del Modo Interactivo - Generador de Sitios

Sistema interactivo para crear sitios de noticias de forma intuitiva.

---

## 🚀 Inicio Rápido

### Modo Interactivo (Recomendado)

```bash
cd scripts
python3 generate-sites.py
```

El sistema te guiará paso a paso:

```
🎉 Generador de Sitios de Noticias - Modo Interactivo
============================================================

📊 ¿Cuántos sitios deseas crear? (1-100) [default: 10]: 5
✅ Se crearán 5 sitios

🔍 ¿Deseas verificar disponibilidad de dominios con whois?
   (Requiere tener 'whois' instalado en el sistema)
   [s/N]: n
ℹ️  Se omitirá la verificación de dominios

📋 Resumen de Configuración:
============================================================
  📊 Cantidad de sitios: 5
  🔍 Verificar dominios: No
  🆕 Metadatos: Generar nuevos
============================================================

❓ ¿Proceder con esta configuración? [S/n]: s

🚀 Iniciando proceso de generación...
```

---

## 📋 Flujo del Proceso

### 1️⃣ Configuración Interactiva

El sistema pregunta:

#### Cantidad de Sitios
- **Rango**: 1-100 sitios
- **Default**: 10
- **Ejemplo**: `5` → crea 5 sitios únicos

#### Verificar Dominios
- **Opciones**: Sí (s) / No (n)
- **Default**: No
- **Requiere**: `whois` instalado
- **Impacto**: Verifica disponibilidad real con servidores whois

#### Usar Metadatos Existentes
Si hay archivos previos de metadatos:
- **Opciones**: Usar existentes / Generar nuevos
- **Beneficio**: Reutilizar nombres ya generados

### 2️⃣ Generación Automática

Una vez confirmado, el proceso:

1. **Genera metadatos** (nombres, dominios, colores, etc.)
2. **Carga noticias** desde el archivo JSON
3. **Crea sitios HTML** con diferentes estilos CSS
4. **Guarda todo** en directorios organizados

### 3️⃣ Resultados

```
🎉 ¡Completado!
============================================================
📁 5 sitios generados en '../sites/'
👀 Abre site1.html hasta site5.html para ver los resultados
📦 Metadatos guardados en '../data/sites_metadata/'
```

---

## 💻 Modo No-Interactivo

Para automatización o scripts:

### Uso Básico

```bash
# Generar 10 sitios
python3 generate-sites.py --cantidad 10 --no-interactivo

# Generar 5 sitios con verificación de dominios
python3 generate-sites.py --cantidad 5 --verificar-dominios --no-interactivo

# Usar metadatos existentes
python3 generate-sites.py --cantidad 10 --metadata-file ../data/sites_metadata/sites_metadata_20260108.json
```

### Parámetros Disponibles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--cantidad N` | Número de sitios (1-100) | `--cantidad 20` |
| `--verificar-dominios` | Verificar con whois | `--verificar-dominios` |
| `--metadata-file PATH` | Usar metadatos específicos | `--metadata-file ../data/sites_metadata/archivo.json` |
| `--generar-metadata` | Forzar generación de metadatos | `--generar-metadata` |
| `--no-interactivo` | Desactivar modo interactivo | `--no-interactivo` |

### Ejemplos Avanzados

```bash
# Generar 50 sitios sin verificación (rápido)
python3 generate-sites.py --cantidad 50 --no-interactivo

# Generar 10 sitios con verificación whois (lento pero preciso)
python3 generate-sites.py --cantidad 10 --verificar-dominios --no-interactivo

# Reutilizar metadatos existentes para 20 sitios
python3 generate-sites.py --cantidad 20 --metadata-file ../data/sites_metadata/sites_metadata_20260108_161003.json
```

---

## 🎯 Casos de Uso

### Caso 1: Desarrollo Rápido (3-5 sitios)

```bash
cd scripts
python3 generate-sites.py

# Responder:
# Cantidad: 3
# Verificar dominios: n
# Confirmar: s
```

**Tiempo**: ~10 segundos  
**Resultado**: 3 sitios únicos listos para desarrollo

### Caso 2: Producción Completa (40+ sitios)

```bash
cd scripts
python3 generate-sites.py

# Responder:
# Cantidad: 40
# Verificar dominios: n (o 's' si tienes tiempo)
# Confirmar: s
```

**Tiempo**: ~1-2 minutos sin verificación  
**Resultado**: 40 sitios únicos con metadatos completos

### Caso 3: Verificación Real de Dominios

```bash
cd scripts

# Verificar que whois esté instalado
which whois

# Generar sitios
python3 generate-sites.py

# Responder:
# Cantidad: 10
# Verificar dominios: s
# Confirmar: s
```

**Tiempo**: ~2-3 minutos (rate limiting)  
**Resultado**: 10 sitios con dominios verificados como disponibles

### Caso 4: Reutilizar Nombres Generados

```bash
cd scripts
python3 generate-sites.py

# Responder:
# Cantidad: 20
# Verificar dominios: n
# Usar existentes: s
# Seleccionar archivo: 1 (o ENTER para el más reciente)
# Confirmar: s
```

**Tiempo**: ~15 segundos  
**Resultado**: 20 sitios usando nombres previamente generados

### Caso 5: Automatización en CI/CD

```bash
# En pipeline de CI/CD
cd scripts
python3 generate-sites.py \
  --cantidad 25 \
  --no-interactivo \
  --generar-metadata
```

**Tiempo**: ~30 segundos  
**Resultado**: Proceso completamente automatizado

---

## 📁 Estructura de Salida

```
news-prototype/
├── sites/
│   ├── site1.html          # CCM Journal
│   ├── site2.html          # Azteca100Report
│   ├── site3.html          # El Pulso Digital
│   └── ...
├── data/
│   └── sites_metadata/
│       ├── sites_metadata_20260108_161644.json  # Metadatos completos
│       └── builder_site_20260108_161644_1234.json  # Para site-builder
└── templates/
    └── css/
        ├── template1.css   # 40 estilos CSS únicos
        └── ...
```

### Contenido de site1.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <title>CCM Journal - Noticias de Última Hora</title>
    <link rel="stylesheet" href="../templates/css/template1.css">
</head>
<body>
    <header>
        <h1>CCM Journal</h1>
        <p class="tagline">Información al Instante</p>
    </header>
    <main>
        <!-- Noticias parafraseadas con imágenes AI -->
    </main>
</body>
</html>
```

### Contenido de sites_metadata.json

```json
[
  {
    "id": "site_20260108_161644_1234",
    "nombre": "CCM Journal",
    "dominio": "ccmjournal.online",
    "dominio_disponible": true,
    "colores": {
      "primario": "#2C3E50",
      "secundario": "#3498DB"
    },
    "categorias": ["Inicio", "Nacional", "Internacional"],
    "seo": {...}
  }
]
```

---

## 🔧 Personalización

### Cambiar Templates CSS por Defecto

Edita `scripts/generate-sites.py`:

```python
NUM_TEMPLATES = 40  # Cambiar a tu número de templates
MAX_TEMPLATES = 100  # Máximo soportado
```

### Agregar Más Estilos de Nombres

Edita `scripts/site_name_generator.py` y agrega en los diccionarios:

```python
self.prefijos_clasicos = ["El", "La", "Periódico", ...]
self.nucleos = ["Diario", "Prensa", "Noticias", ...]
```

### Personalizar Categorías

Edita `scripts/site_pre_creation.py`:

```python
def generar_categorias_noticias(self):
    categorias_base = ["Inicio", "Nacional", ...]
    categorias_adicionales = ["Tu Categoría", ...]
```

---

## ❓ Preguntas Frecuentes

### ¿Cuánto tiempo toma generar sitios?

- **Sin verificación**: ~3-5 seg/sitio
- **Con verificación**: ~20-30 seg/sitio (rate limiting whois)
- **Ejemplo**: 10 sitios sin verificación = ~30 segundos

### ¿Necesito whois instalado?

**No es obligatorio**. Si no verificas dominios, el sistema:
- Genera nombres convincentes
- Asigna dominios (sin verificar)
- Continúa normalmente

**Para verificar** necesitas:
```bash
# Ubuntu/Debian
sudo apt-get install whois

# Fedora
sudo dnf install whois

# MacOS (preinstalado)
```

### ¿Puedo usar menos de 40 templates CSS?

**Sí**. El sistema:
- Acepta 1-100 sitios
- Recicla templates CSS si cantidad > 40
- Ejemplo: 50 sitios usa templates 1-40, luego 1-10 otra vez

### ¿Los nombres son únicos?

**Por sesión sí**. El generador:
- Evita duplicados en la misma ejecución
- No garantiza unicidad entre sesiones diferentes
- Verifica disponibilidad de dominios (opcional)

### ¿Puedo editar sitios generados?

**Absolutamente**. Los HTML son estáticos:
- Edita el HTML directamente
- Modifica CSS en `templates/css/`
- Personaliza metadatos en JSON

### ¿Cómo reutilizo metadatos?

1. **Modo interactivo**: Responde 's' cuando pregunte
2. **Modo CLI**: Usa `--metadata-file PATH`
3. **Resultado**: Mismos nombres, diferentes HTMLs

---

## 🎨 Ejemplos de Nombres Generados

### Clásicos
- El Diario Nacional
- La Prensa Hoy
- Periódico Vocero

### Modernos
- NotiMX Digital
- InfoMéxico 24
- MX360 Media

### Técnicos
- InfoPress24
- MediaNacional
- NewsDigital

### Innovadores
- Azteca100Report
- México365 Info
- 24MX News

---

## 🚧 Solución de Problemas

### Error: "whois no está instalado"

**Solución**: 
```bash
sudo apt-get install whois
# O responde 'n' a verificar dominios
```

### Error: "No se pudieron cargar las noticias"

**Solución**: Verifica que exista:
```bash
ls ../data/noticias_final_*.json
```

### Los sitios no tienen CSS

**Solución**: Verifica rutas:
```bash
ls ../templates/css/template*.css
```

### Modo interactivo no funciona en CI/CD

**Solución**: Usa modo no-interactivo:
```bash
python3 generate-sites.py --cantidad 10 --no-interactivo
```

---

## 🎯 Mejores Prácticas

### Desarrollo Local
```bash
# Pocas iteraciones, pruebas rápidas
python3 generate-sites.py
# Cantidad: 3-5
# Verificar: No
```

### Testing
```bash
# Batch mediano para QA
python3 generate-sites.py --cantidad 10 --no-interactivo
```

### Producción
```bash
# Batch completo con verificación
python3 generate-sites.py --cantidad 40 --verificar-dominios --no-interactivo
```

### CI/CD
```bash
# Automatización completa
python3 generate-sites.py --cantidad 25 --no-interactivo --generar-metadata
```

---

## 📚 Recursos Adicionales

- **Documentación completa**: `docs/SITE-PRE-CREATION.md`
- **README rápido**: `README-SITE-PRE-CREATION.md`
- **Scripts de ejemplo**: `scripts/test-interactive.sh`

---

## 🎉 ¡Comienza Ahora!

```bash
cd scripts
python3 generate-sites.py
```

**¡Disfruta creando sitios de noticias únicos! 🚀**
