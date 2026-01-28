# 🎯 Protocolo de Pre-Creación de Sitios - Resumen Rápido

Sistema completo para preparar sitios de noticias antes de su creación:
- ✅ Nombres convincentes aleatorios
- ✅ Verificación de disponibilidad de dominios
- ✅ Metadatos JSON completos para site-builder

---

## 🚀 Inicio Rápido

### 1. Generar Metadatos de Sitios

```bash
cd scripts

# Generar 5 sitios (sin verificar dominios)
python3 site_pre_creation.py --cantidad 5

# Generar 5 sitios con verificación whois (requiere whois instalado)
python3 site_pre_creation.py --cantidad 5 --verificar-dominios
```

### 2. Integrar con Generador de Sitios

```bash
# Generar metadatos y crear sitios HTML automáticamente
python3 generate-sites.py --generar-metadata

# Usar archivo de metadatos existente
python3 generate-sites.py --metadata-file ../data/sites_metadata/sites_metadata_20260108_161003.json
```

---

## 📦 Qué Genera

### Archivo de Metadatos Completo
`data/sites_metadata/sites_metadata_TIMESTAMP.json`

Contiene array de sitios con:
- Nombre y tagline
- Dominio (verificado o no)
- Paleta de colores
- Especificaciones de logo
- Categorías de contenido
- Información de contacto
- URLs de redes sociales
- Metadatos SEO

### Archivo para Site-Builder
`data/sites_metadata/builder_site_ID.json`

Formato optimizado para constructores de sitios, incluye:
- Configuración de marca (nombre, colores, logo)
- Estructura del sitio (categorías, navegación)
- Información de contacto y redes sociales
- Metadatos SEO completos

---

## 🎨 Características

### Generación de Nombres (8 estilos)
- **Clásico**: El Diario Nacional
- **Moderno**: NotiMX Digital
- **Técnico**: InfoPress24
- **Regional**: El Mexicano Hoy
- **Compuesto**: DiarioNacionalMX
- **Abreviado**: DNM News
- **Descriptivo**: Noticias de México
- **Innovador**: MX360 Media

### Verificación de Dominios
- Consultas whois reales (opcional)
- Múltiples TLDs: .com, .mx, .com.mx, .news, .info
- Rate limiting automático
- Cache de resultados

### Metadatos Generados
- **Colores**: 6 paletas profesionales
- **Logo**: Especificaciones completas (fuente, estilo, dimensiones)
- **Categorías**: 7-9 categorías de noticias
- **SEO**: Títulos, descripciones, keywords optimizados
- **Contacto**: Emails, teléfono, dirección
- **Redes**: URLs para 6 plataformas sociales

---

## 📋 Módulos

### `site_name_generator.py`
Genera nombres y taglines convincentes.

```python
from site_name_generator import SiteNameGenerator

generator = SiteNameGenerator()
sitio = generator.generar_sitio_completo(estilo="moderno")

print(sitio['nombre'])           # "NotiMX Digital"
print(sitio['tagline'])          # "Noticias 24 Horas al Día"
print(sitio['dominio_completo']) # "notimxdigital.news"
```

### `domain_verifier.py`
Verifica disponibilidad con whois.

```python
from domain_verifier import DomainVerifier

verifier = DomainVerifier()
resultado = verifier.verificar_dominio("ejemplo.com")

if resultado['disponible']:
    print("✅ Dominio disponible")
```

### `site_pre_creation.py`
Protocolo completo de pre-creación.

```python
from site_pre_creation import SitePreCreation

protocolo = SitePreCreation()

# Generar 10 sitios
sitios = protocolo.crear_batch_sitios(
    cantidad=10,
    verificar_dominios=False,
    guardar_archivo=True
)

# Exportar para site-builder
builder_file = protocolo.exportar_para_site_builder(sitios[0])
```

---

## 🔧 Requisitos

### Python 3.8+
Incluido en el proyecto.

### whois (opcional, para verificación)
```bash
# Ubuntu/Debian
sudo apt-get install whois

# Fedora/RHEL
sudo dnf install whois

# MacOS (preinstalado)
# No requiere instalación
```

---

## 📊 Ejemplo de Salida

### Ejecución
```bash
$ python3 site_pre_creation.py --cantidad 3

🚀 Generando metadatos para 3 sitios...
============================================================

📝 Sitio 1/3
   Nombre: Periódico Vocero
   Dominio: periodicovocero.mx
   Disponible: ✅

📝 Sitio 2/3
   Nombre: PressActualDigital
   Dominio: pressactualdigital.online
   Disponible: ✅

📝 Sitio 3/3
   Nombre: El México Ahora
   Dominio: mexicoahora.mx
   Disponible: ✅

💾 Metadatos guardados en: ../data/sites_metadata/sites_metadata_20260108_161003.json

📊 Resumen:
   Total de sitios: 3
   Dominios verificados: 0
   Dominios disponibles: 3

✅ ¡Proceso completado!
```

### Estructura JSON Generada
```json
{
  "id": "site_20260108_161003_9314",
  "nombre": "Periódico Vocero",
  "tagline": "Rápido, Preciso, Confiable",
  "dominio": "periodicovocero.mx",
  "dominio_disponible": true,
  "colores": {
    "primario": "#27AE60",
    "secundario": "#16A085",
    "acento": "#F39C12"
  },
  "logo": {
    "nombre_completo": "Periódico Vocero",
    "iniciales": "PV",
    "estilo": "modern",
    "tipo": "wordmark",
    "fuente_sugerida": "Lato"
  },
  "categorias": ["Inicio", "Nacional", "Política", "..."],
  "contacto": {
    "email_general": "contacto@periodicovocero.mx",
    "telefono": "+52 55 9871 5585"
  },
  "seo": {
    "titulo": "Periódico Vocero - Rápido, Preciso, Confiable",
    "descripcion": "Tu fuente confiable de noticias...",
    "keywords": ["noticias", "méxico", "actualidad"]
  }
}
```

---

## 🔄 Flujo de Trabajo

```
1. GENERACIÓN DE METADATOS
   ├─ Nombres convincentes (8 estilos)
   ├─ Verificación de dominios (opcional)
   ├─ Colores y especificaciones de logo
   ├─ Categorías y estructura
   └─ SEO y contacto

2. GUARDADO
   ├─ sites_metadata_TIMESTAMP.json (completo)
   └─ builder_site_ID.json (optimizado)

3. INTEGRACIÓN
   ├─ Usar en generate-sites.py
   ├─ Generar logos con IA
   └─ Crear sitios HTML con noticias
```

---

## 🎯 Casos de Uso

### Caso 1: Generar 40 Sitios Únicos
```bash
cd scripts

# Generar metadatos
python3 site_pre_creation.py --cantidad 40

# Crear sitios HTML
python3 generate-sites.py --metadata-file ../data/sites_metadata/sites_metadata_*.json
```

### Caso 2: Verificar Disponibilidad Real
```bash
# Requiere whois instalado
python3 site_pre_creation.py --cantidad 10 --verificar-dominios
```

### Caso 3: Flujo Completo Automatizado
```bash
# Todo en un comando
python3 generate-sites.py --generar-metadata
```

### Caso 4: Pool de Sitios para Uso Futuro
```bash
# Generar 100 metadatos para reusar
python3 site_pre_creation.py --cantidad 100 --output ../data/sites_pool
```

---

## 📖 Documentación Completa

Ver `docs/SITE-PRE-CREATION.md` para:
- Guía completa de uso
- Personalización avanzada
- Integración con site-builder
- Estructura detallada de metadatos
- Ejemplos de código
- Solución de problemas

---

## ✅ Testing

```bash
# Probar generador de nombres
python3 site_name_generator.py

# Probar verificador de dominios
python3 domain_verifier.py

# Probar protocolo completo
python3 site_pre_creation.py --cantidad 3
```

---

## 🎉 Listo para Usar

Sistema completo implementado y funcional:
- ✅ 3 módulos principales
- ✅ Integrado con generate-sites.py
- ✅ Documentación completa
- ✅ Ejemplos funcionales

```bash
# Comienza ahora
cd scripts
python3 site_pre_creation.py --cantidad 5
```

---

**Parte del proyecto news-prototype**
