# 🎯 Protocolo de Pre-Creación de Sitios

Sistema completo para generar nombres convincentes de sitios de noticias, verificar disponibilidad de dominios y crear metadatos JSON para integración con el site-builder.

---

## 📋 Índice

1. [Características](#-características)
2. [Componentes](#-componentes)
3. [Instalación](#-instalación)
4. [Uso Básico](#-uso-básico)
5. [Uso Avanzado](#-uso-avanzado)
6. [Integración con Site-Builder](#-integración-con-site-builder)
7. [Estructura de Metadatos](#-estructura-de-metadatos)
8. [Ejemplos](#-ejemplos)

---

## ✨ Características

### Generación de Nombres
- **8 estilos diferentes**: clásico, moderno, técnico, regional, compuesto, abreviado, descriptivo, innovador
- **Nombres convincentes**: combinaciones realistas para sitios de noticias
- **Anti-duplicados**: evita repetir nombres en la misma sesión
- **Taglines automáticos**: genera eslóganes apropiados al nombre

### Verificación de Dominios
- **Integración con whois**: verifica disponibilidad real de dominios
- **Múltiples TLDs**: .com, .mx, .com.mx, .news, .info, etc.
- **Rate limiting**: protección contra bloqueos por consultas excesivas
- **Cache inteligente**: evita consultas repetidas

### Generación de Metadatos
- **Información completa**: nombre, dominio, colores, categorías, contacto
- **Paletas de colores**: 6 esquemas profesionales predefinidos
- **Metadatos SEO**: títulos, descripciones, keywords optimizados
- **Redes sociales**: URLs placeholder para todas las plataformas
- **Especificaciones de logo**: dimensiones, estilos, colores

---

## 🔧 Componentes

### 1. `site_name_generator.py`
Generador de nombres y taglines para sitios de noticias.

**Características:**
- 8 estilos de nombres diferentes
- Componentes modulares (prefijos, núcleos, sufijos)
- Generación de dominios optimizados
- Sistema anti-duplicados

### 2. `domain_verifier.py`
Verificador de disponibilidad de dominios usando whois.

**Características:**
- Consultas whois nativas
- Análisis inteligente de respuestas
- Rate limiting configurable
- Cache de consultas
- Soporte multi-TLD

### 3. `site_pre_creation.py`
Protocolo completo de pre-creación.

**Características:**
- Generación batch de metadatos
- Verificación opcional de dominios
- Exportación para site-builder
- Metadatos completos (SEO, colores, logo, etc.)

---

## 📥 Instalación

### Requisitos

```bash
# Python 3.8+
python3 --version

# whois (para verificación de dominios)
# Ubuntu/Debian:
sudo apt-get install whois

# Fedora/RHEL:
sudo dnf install whois

# MacOS: viene preinstalado
```

### Instalar Módulos

Los módulos están en `scripts/`:
- `site_name_generator.py`
- `domain_verifier.py`
- `site_pre_creation.py`

No requieren dependencias adicionales más allá de las del proyecto principal.

---

## 🚀 Uso Básico

### Generar Nombres de Sitios

```bash
cd scripts
python3 site_name_generator.py
```

**Salida:**
```
🎨 Generador de Nombres de Sitios de Noticias
============================================================

📋 Generando 10 nombres de sitios de ejemplo:

1. El Diario Digital
   Tagline: La Verdad en Cada Historia
   Dominio: diariodigital.com.mx
   Estilo: clasico

2. InfoMX 24
   Tagline: Noticias 24 Horas al Día
   Dominio: infomx24.news
   Estilo: moderno
...
```

### Verificar Dominios

```bash
cd scripts
python3 domain_verifier.py
```

**Salida:**
```
🔍 Verificador de Disponibilidad de Dominios
============================================================

✅ whois está instalado

🧪 Probando con 2 dominios:

Verificando 1/2: google.com... ⛔ REGISTRADO
Verificando 2/2: ejemplo-no-existe-xyz123456789.com... ✅ DISPONIBLE
```

### Generar Metadatos Completos

```bash
cd scripts

# Generar 5 sitios sin verificar dominios
python3 site_pre_creation.py --cantidad 5

# Generar 5 sitios verificando dominios
python3 site_pre_creation.py --cantidad 5 --verificar-dominios
```

**Salida:**
```
🚀 Generando metadatos para 5 sitios...
============================================================

📝 Sitio 1/5
   Nombre: El Observador Nacional
   Dominio: observadornacional.com
   Disponible: ✅

📝 Sitio 2/5
   Nombre: NotiMX Digital
   Dominio: notimxdigital.mx
   Disponible: ✅
...

💾 Metadatos guardados en: ../data/sites_metadata/sites_metadata_20260108_1430.json

📊 Resumen:
   Total de sitios: 5
   Dominios verificados: 5
   Dominios disponibles: 4

📦 Ejemplo para site-builder: ../data/sites_metadata/builder_site_20260108_1430_1234.json

✅ ¡Proceso completado!
```

---

## 🎓 Uso Avanzado

### Integración con generate-sites.py

El generador de sitios ahora soporta metadatos:

```bash
cd scripts

# Generar metadatos y crear sitios HTML
python3 generate-sites.py --generar-metadata

# Generar metadatos con verificación de dominios
python3 generate-sites.py --generar-metadata --verificar-dominios

# Usar archivo de metadatos específico
python3 generate-sites.py --metadata-file ../data/sites_metadata/sites_metadata_20260108_1430.json
```

### Uso Programático

```python
from site_pre_creation import SitePreCreation

# Crear protocolo
protocolo = SitePreCreation(output_dir="../data/sites_metadata")

# Generar un sitio
metadata = protocolo.crear_metadata_sitio(
    estilo_nombre="moderno",
    verificar_dominio=True
)

print(f"Sitio: {metadata['nombre']}")
print(f"Dominio: {metadata['dominio']}")
print(f"Disponible: {metadata['dominio_disponible']}")

# Generar múltiples sitios
sitios = protocolo.crear_batch_sitios(
    cantidad=10,
    verificar_dominios=False,
    guardar_archivo=True
)

# Exportar para site-builder
builder_file = protocolo.exportar_para_site_builder(metadata)
```

### Solo Generar Nombres (sin verificación)

```python
from site_name_generator import SiteNameGenerator

generator = SiteNameGenerator()

# Generar nombre aleatorio
sitio = generator.generar_sitio_completo()

# Generar nombre con estilo específico
sitio_clasico = generator.generar_sitio_completo(estilo="clasico")
sitio_moderno = generator.generar_sitio_completo(estilo="moderno")

print(sitio['nombre'])      # "El Diario Digital"
print(sitio['tagline'])     # "La Verdad en Cada Historia"
print(sitio['dominio_completo'])  # "diariodigital.com"
```

### Solo Verificar Dominios

```python
from domain_verifier import DomainVerifier

verifier = DomainVerifier(rate_limit_delay=2.0)

# Verificar un dominio
resultado = verifier.verificar_dominio("example.com")

if resultado['disponible']:
    print("✅ Dominio disponible")
elif resultado['registrado']:
    print("⛔ Dominio registrado")
    print(f"Registrar: {resultado['info_adicional'].get('registrar')}")

# Verificar múltiples dominios
dominios = ["site1.com", "site2.mx", "site3.news"]
resultados = verifier.verificar_dominios_batch(dominios)
```

---

## 🔗 Integración con Site-Builder

El sistema genera archivos JSON optimizados para integración con constructores de sitios.

### Formato de Salida para Site-Builder

```json
{
  "site_id": "site_20260108_143025_1234",
  "name": "El Observador Digital",
  "tagline": "La Verdad en Cada Historia",
  "domain": "observadordigital.com",
  "colors": {
    "primario": "#2C3E50",
    "secundario": "#3498DB",
    "acento": "#E74C3C",
    "texto": "#2C3E50",
    "fondo": "#ECF0F1"
  },
  "logo_specs": {
    "nombre_completo": "El Observador Digital",
    "iniciales": "EOD",
    "estilo": "modern",
    "tipo": "wordmark",
    "fuente_sugerida": "Montserrat",
    "dimensiones": {
      "logo_principal": "500x200",
      "favicon": "64x64",
      "social": "1200x630"
    }
  },
  "categories": [
    "Inicio", "Nacional", "Internacional", "Política",
    "Tecnología", "Deportes", "Cultura"
  ],
  "contact": {
    "email_general": "contacto@observadordigital.com",
    "email_redaccion": "redaccion@observadordigital.com",
    "telefono": "+52 55 1234 5678"
  },
  "social": {
    "facebook": "https://facebook.com/observadordigital",
    "twitter": "https://twitter.com/observadordigital",
    "instagram": "https://instagram.com/observadordigital"
  },
  "seo": {
    "titulo": "El Observador Digital - La Verdad en Cada Historia",
    "descripcion": "Tu fuente confiable de noticias e información...",
    "keywords": ["noticias", "méxico", "actualidad", "política"]
  }
}
```

### Usar en Site-Builder

```python
import json
from pathlib import Path

# Cargar metadata
with open('builder_site_20260108_143025_1234.json', 'r') as f:
    site_config = json.load(f)

# Usar en tu constructor
nombre = site_config['name']
colores = site_config['colors']
logo_specs = site_config['logo_specs']

# Generar logo con especificaciones
generate_logo(
    text=logo_specs['nombre_completo'],
    font=logo_specs['fuente_sugerida'],
    color_primary=colores['primario'],
    color_secondary=colores['secundario'],
    size=logo_specs['dimensiones']['logo_principal']
)

# Crear sitio con configuración
create_site(
    name=site_config['name'],
    domain=site_config['domain'],
    categories=site_config['categories'],
    colors=site_config['colors']
)
```

---

## 📊 Estructura de Metadatos

### Metadata Completa

```json
{
  "id": "site_20260108_143025_1234",
  "nombre": "El Observador Digital",
  "tagline": "La Verdad en Cada Historia",
  "estilo": "clasico",
  
  "dominio": "observadordigital.com",
  "dominio_verificado": true,
  "dominio_disponible": true,
  
  "colores": {
    "primario": "#2C3E50",
    "secundario": "#3498DB",
    "acento": "#E74C3C",
    "texto": "#2C3E50",
    "fondo": "#ECF0F1"
  },
  
  "logo": {
    "nombre_completo": "El Observador Digital",
    "iniciales": "EOD",
    "estilo": "modern",
    "tipo": "wordmark",
    "colores": { "..." },
    "fuente_sugerida": "Montserrat",
    "peso_fuente": "bold",
    "formato_salida": ["png", "svg"],
    "dimensiones": {
      "logo_principal": "500x200",
      "favicon": "64x64",
      "social": "1200x630"
    }
  },
  
  "categorias": [
    "Inicio", "Nacional", "Internacional", "Política",
    "Economía", "Deportes", "Cultura"
  ],
  
  "contacto": {
    "email_general": "contacto@observadordigital.com",
    "email_redaccion": "redaccion@observadordigital.com",
    "email_publicidad": "publicidad@observadordigital.com",
    "telefono": "+52 55 1234 5678",
    "direccion": "Ciudad de México, México",
    "horario": "Disponible 24/7"
  },
  
  "redes_sociales": {
    "facebook": "https://facebook.com/observadordigital",
    "twitter": "https://twitter.com/observadordigital",
    "instagram": "https://instagram.com/observadordigital",
    "youtube": "https://youtube.com/@observadordigital",
    "linkedin": "https://linkedin.com/company/observadordigital",
    "telegram": "https://t.me/observadordigital"
  },
  
  "seo": {
    "titulo": "El Observador Digital - La Verdad en Cada Historia",
    "descripcion": "Tu fuente confiable de noticias e información actualizada...",
    "keywords": ["noticias", "méxico", "actualidad", "política", "observadordigital"],
    "og_type": "website",
    "og_locale": "es_MX",
    "twitter_card": "summary_large_image"
  },
  
  "fecha_creacion": "2026-01-08T14:30:25.123456",
  "version": "1.0",
  "estado": "pre-creado"
}
```

---

## 📚 Ejemplos

### Ejemplo 1: Flujo Completo con Verificación

```bash
cd scripts

# 1. Generar metadatos con verificación de dominios
python3 site_pre_creation.py --cantidad 10 --verificar-dominios

# 2. Generar sitios HTML usando los metadatos
python3 generate-sites.py --metadata-file ../data/sites_metadata/sites_metadata_TIMESTAMP.json

# 3. Ver resultados
cd ../sites
ls -la
```

### Ejemplo 2: Generación Rápida sin Verificación

```bash
cd scripts

# Todo en un comando
python3 generate-sites.py --generar-metadata
```

### Ejemplo 3: Solo Metadatos para Uso Posterior

```bash
cd scripts

# Generar 50 metadatos de sitios
python3 site_pre_creation.py --cantidad 50 --output ../data/sites_pool

# Usar más tarde
python3 generate-sites.py --metadata-file ../data/sites_pool/sites_metadata_*.json
```

### Ejemplo 4: Personalización Avanzada

```python
from site_pre_creation import SitePreCreation

protocolo = SitePreCreation()

# Generar sitios con estilos específicos
estilos = ["clasico", "moderno", "tecnico"]
sitios = []

for estilo in estilos:
    for _ in range(3):  # 3 de cada estilo
        metadata = protocolo.crear_metadata_sitio(
            estilo_nombre=estilo,
            verificar_dominio=False
        )
        sitios.append(metadata)

# Guardar batch personalizado
import json
with open('sitios_personalizados.json', 'w') as f:
    json.dump(sitios, f, indent=2, ensure_ascii=False)
```

---

## 🎨 Estilos de Nombres

### 1. Clásico
Formato tradicional de periódicos.

**Ejemplos:**
- El Diario Nacional
- La Prensa Hoy
- El Observador Digital

### 2. Moderno
Nombres actuales y dinámicos.

**Ejemplos:**
- NotiMX Digital
- InfoMéxico 24
- México360 Media

### 3. Técnico
Nombres compactos y tecnológicos.

**Ejemplos:**
- InfoPress24
- MediaNacional
- NewsDigital

### 4. Regional
Enfoque en ubicación geográfica.

**Ejemplos:**
- El Mexicano Hoy
- Noticias México Actual
- México Digital

### 5. Compuesto
Palabras unidas sin espacios.

**Ejemplos:**
- DiarioNacionalMX
- NoticiasAztecas
- InformadorMexicano

### 6. Abreviado
Iniciales + descriptor.

**Ejemplos:**
- DNM News
- IMN Media
- PMD Press

### 7. Descriptivo
Nombres auto-explicativos.

**Ejemplos:**
- Noticias de México
- Información Nacional
- Actualidad Mexicana

### 8. Innovador
Nombres creativos y únicos.

**Ejemplos:**
- MX360 Media
- 24México News
- México365 Info

---

## 🔐 Notas de Seguridad

### Rate Limiting
El verificador de dominios implementa rate limiting automático:
- Delay de 2 segundos entre consultas (configurable)
- Protección contra bloqueos de servidores whois
- Cache de resultados para evitar consultas repetidas

### Privacy
- No se almacenan datos sensibles
- URLs de redes sociales son placeholders
- Información de contacto es genérica

---

## 🚧 Limitaciones

### Verificación de Dominios
- Requiere `whois` instalado en el sistema
- Respuestas de whois varían según TLD
- Algunos TLDs tienen protección anti-scraping
- Rate limiting puede ralentizar verificaciones masivas

### Nombres
- No garantiza que el nombre sea original 100%
- Nombres generados pueden coincidir con sitios existentes
- Verificación solo técnica, no legal

---

## 📈 Roadmap

### Próximas Mejoras
- [ ] Integración con APIs de verificación de dominios
- [ ] Generación automática de logos con IA
- [ ] Verificación de marcas registradas
- [ ] Análisis de SEO competitivo
- [ ] Sugerencias de nombres basadas en keywords
- [ ] Integración con registradores de dominios

---

## 🤝 Contribuir

Mejoras sugeridas son bienvenidas:
- Nuevos estilos de nombres
- Más paletas de colores
- Mejor análisis de whois
- Integración con más TLDs

---

## 📄 Licencia

MIT License - Parte del proyecto news-prototype

---

**🎉 ¡Sistema de Pre-Creación Listo para Usar!**

```bash
# Inicio rápido
cd scripts
python3 site_pre_creation.py --cantidad 10
```
