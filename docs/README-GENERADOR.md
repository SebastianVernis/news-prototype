# 📰 News Prototype - Generador Automático de Sitios de Noticias

> Sistema automatizado que genera sitios web de noticias únicos y completos en 2-3 minutos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CSS](https://img.shields.io/badge/CSS-Modular-1572B6.svg)](https://www.w3.org/Style/CSS/)
[![AI](https://img.shields.io/badge/AI-Blackbox-black.svg)](https://blackbox.ai)

---

## 🎯 ¿Qué hace este sistema?

Genera sitios web de noticias **completamente funcionales** con:

✅ **20 artículos únicos** de 800 palabras cada uno  
✅ **21 imágenes AI** (20 artículos + 1 logo)  
✅ **25 páginas HTML** (index + 20 artículos + 4 legales)  
✅ **CSS responsivo** con 6,000 combinaciones posibles  
✅ **Páginas legales** completas (Términos, Privacidad, FAQs)  
✅ **16.5 millones** de combinaciones únicas totales  

**Tiempo:** 2-3 minutos por sitio completo

---

## 🚀 Quick Start (3 pasos)

```bash
# 1. Configurar API keys
echo "BLACKBOX_API_KEY=tu_api_key" > .env
echo "NEWS_API_KEY=tu_api_key" >> .env

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar sitio
python scripts/master_orchestrator.py
```

¡Listo! Tu sitio está en `generated_sites/site_1/`

---

## 📊 Output

```
generated_sites/site_1/
├── 📄 index.html              ← Página principal (12 noticias)
├── 📄 article_1.html          ← Artículo completo (800 palabras)
├── 📄 article_2.html          
...
├── 📄 article_20.html         
├── 📄 terminos.html           ← Términos y Condiciones
├── 📄 privacidad.html         ← Política de Privacidad (GDPR)
├── 📄 faqs.html               ← 10 Preguntas Frecuentes
├── 📄 acerca.html             ← Acerca de Nosotros
├── 🎨 style.css               ← CSS modular completo
├── 🖼️ logo.jpg                ← Logo generado con IA
└── 📁 images/
    ├── news_1.jpg
    ...
    └── news_20.jpg

27 archivos totales | 2-3 minutos
```

---

## ✨ Características

### 🤖 Contenido Inteligente
- **NewsAPI** - 20 noticias de tecnología
- **8 estilos de parafraseo** (profesional, casual, técnico, narrativo...)
- **8 estructuras** (pirámide invertida, cronológica, analítica...)
- **800 palabras por artículo** - Contenido profesional completo
- **20 autores ficticios** - Nombres aleatorios únicos

### 🎨 Diseño Modular
- **20 paletas de colores** únicas
- **15 combinaciones de fuentes** profesionales
- **20 layouts CSS** estructurales
- **6,000 templates** posibles (20 × 15 × 20)
- **43,200 configuraciones HTML** (layouts × headers × navs)

### 🖼️ Imágenes AI
- **Flux Schnell** - Modelo rápido de Blackbox AI
- **Prompts personalizados** por título y descripción
- **21 imágenes por sitio** (20 artículos + 1 logo)

### 📱 CSS Moderno
- **28 variables CSS** (colores, spacing, shadows, radius)
- **CSS Grid responsivo** con auto-fit
- **Tipografía fluida** con clamp()
- **Mobile-first** (5 breakpoints)
- **7 niveles spacing** (4px a 64px)

### 📄 Páginas Legales
- Términos y Condiciones (10 secciones)
- Política de Privacidad (GDPR-compliant)
- FAQs (10 preguntas)
- Acerca de Nosotros (misión, valores)

---

## 🔄 Flujo del Sistema

```
1. NewsAPI           → 20 noticias originales        (5-10s)
2. Parafraseo        → 20 artículos parafraseados    (30-60s)
3. Expansión         → 20 artículos 800 palabras     (incluido)
4. Imágenes AI       → 20 imágenes + 1 logo          (40-80s)
5. Metadata          → Nombre, dominio, colores      (2-5s)
6. CSS               → Paleta + Fuente + Layout      (1-2s)
7. HTML              → 25 páginas completas          (2-5s)

TOTAL: ~2-3 minutos
```

---

## 🛠️ Comandos

### Usando Menú Interactivo (RECOMENDADO)
```bash
./menu.sh
# → Seleccionar opción del menú
```

### CLI Directo
```bash
# Básico (sin verificar dominios)
python scripts/master_orchestrator.py

# Con verificación de dominios (requiere whois)
python scripts/master_orchestrator.py --verificar-dominios

# Usar noticias en cache
python scripts/master_orchestrator.py --usar-cache

# Directorio personalizado
python scripts/master_orchestrator.py --output-dir /path/to/output
```

### Servir Sitios
```bash
# Desde el menú (recomendado)
./menu.sh → 1 → 6 → Seleccionar modo

# CLI directo
python scripts/serve_sites.py              # Servir site_1 en puerto 8000
python scripts/serve_sites.py --site site_2 --port 8002
python scripts/serve_sites.py --all       # Servir todos
python scripts/serve_sites.py --list      # Listar sitios
```

---

## 📖 Documentación

| Archivo | Descripción |
|---------|-------------|
| **[RESUMEN-FLUJO.md](./RESUMEN-FLUJO.md)** | Resumen ejecutivo rápido ⚡ |
| **[DIAGRAMA-FLUJO-COMPLETO.md](./DIAGRAMA-FLUJO-COMPLETO.md)** | Flujo detallado con ejemplos 📊 |
| **[AGENTS.md](./AGENTS.md)** | Guía para agentes IA 🤖 |

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| Noticias procesadas | 20 |
| Palabras por artículo | 800 |
| Páginas HTML | 25 |
| Imágenes AI | 21 |
| CSS Variables | 28 |
| Breakpoints | 5 |
| Combinaciones CSS | 6,000 |
| Configuraciones HTML | 43,200 |
| **Combinaciones totales** | **16.5 millones** |
| **Tiempo** | **2-3 minutos** |

---

## 🎨 CSS Variables

```css
:root {
    /* Colores */
    --primary-color: #2C3E50;
    --secondary-color: #3498DB;
    
    /* Spacing (Tailwind-style) */
    --space-xs: 0.25rem;   /* 4px */
    --space-sm: 0.5rem;    /* 8px */
    --space-md: 1rem;      /* 16px */
    --space-lg: 1.5rem;    /* 24px */
    --space-xl: 2rem;      /* 32px */
    --space-2xl: 3rem;     /* 48px */
    --space-3xl: 4rem;     /* 64px */
    
    /* Breakpoints */
    --breakpoint-sm: 640px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 1024px;
    --breakpoint-xl: 1280px;
    --breakpoint-2xl: 1536px;
}
```

---

## 🔧 Requisitos

### Python
- Python 3.8+
- pip

### Dependencias
```bash
requests>=2.31.0
python-dotenv>=1.0.0
```

### APIs
- **Blackbox AI** - Para parafraseo, expansión e imágenes
- **NewsAPI** - Para noticias (opcional con `--usar-cache`)

### Opcional
- `whois` - Para verificación de dominios

---

## 🐛 Troubleshooting

### Error: "BLACKBOX_API_KEY no encontrada"
```bash
echo "BLACKBOX_API_KEY=tu_api_key_aqui" > .env
```

### Error: "whois no instalado"
```bash
# Ubuntu/Debian
sudo apt-get install whois

# macOS
brew install whois

# O ejecutar sin verificar
python scripts/master_orchestrator.py  # Sin --verificar-dominios
```

### Imágenes no se generan
- Verificar API key de Blackbox AI
- Verificar conexión a internet
- Revisar logs en consola

---

## 📁 Estructura del Proyecto

```
Tecnología/
├── scripts/                    # 16 módulos Python
│   ├── master_orchestrator.py # Orquestador principal
│   ├── paraphrase.py          # 8 estilos de parafraseo
│   ├── article-expander.py    # Expansión a 800 palabras
│   ├── generate-images-ai.py  # Imágenes con Flux Schnell
│   ├── template_combiner.py   # 6,000 combinaciones CSS
│   └── ...
├── data/                       # Noticias y metadata
├── templates/css/              # 6,000 templates CSS
├── generated_sites/            # Sitios generados
└── docs/                       # Documentación
```

---

## 🎯 Roadmap

### ✅ Implementado
- [x] Descarga de noticias (NewsAPI)
- [x] Parafraseo (8 estilos)
- [x] Expansión (800 palabras, 8 estructuras)
- [x] Imágenes AI (Flux Schnell)
- [x] 6,000 templates CSS
- [x] 43,200 configuraciones HTML
- [x] Páginas legales completas
- [x] Responsive design
- [x] CSS Grid y Flexbox
- [x] Tipografía fluida
- [x] Sistema de variables

### 🚀 Futuro
- [ ] Deploy automático (Vercel/Netlify)
- [ ] Sitemap.xml
- [ ] robots.txt
- [ ] Open Graph tags
- [ ] RSS feed
- [ ] AMP pages
- [ ] PWA
- [ ] Lazy loading
- [ ] i18n
- [ ] Panel admin

---

## 📜 Licencia

MIT License - Proyecto educativo de código abierto

**Nota:** Los sitios generados son para demostración. El contenido es parafraseado desde fuentes públicas y debe revisarse antes de publicación real.

---

## 🤝 Contribuciones

1. Revisa `AGENTS.md` para reglas
2. Lee `DIAGRAMA-FLUJO-COMPLETO.md` para entender el flujo
3. Prueba con diferentes configuraciones
4. Abre un issue o PR

---

## 📞 Soporte

- **Documentación:** Ver archivos `.md` en el proyecto
- **Issues:** GitHub Issues
- **Guía de agentes:** `AGENTS.md`

---

## 🎉 Ejemplo de Uso

```bash
# 1. Setup
git clone <repo>
cd Tecnología
echo "BLACKBOX_API_KEY=xxx" > .env
pip install -r requirements.txt

# 2. Generar sitio
python scripts/master_orchestrator.py

# 3. Ver resultado (OPCIÓN A: Menú)
./menu.sh
# → 1 (Generación) → 6 (Servir) → 1 (Último)
# Abrir: http://localhost:8000

# O (OPCIÓN B: CLI directo)
python scripts/serve_sites.py
# Abrir: http://localhost:8000

# O (OPCIÓN C: Manual)
cd generated_sites/site_1
python -m http.server 8000
```

**¡En 2-3 minutos tienes un sitio de noticias completo!** 🚀

---

**Última actualización:** 2026-01-15 14:50  
**Versión:** 2.0  
**Autor:** Sistema de Generación Automática de Sitios de Noticias
