# 🎨 Generador de Imágenes Artísticas para Noticias

## Descripción

Script automatizado que genera imágenes multimedia abstractas y artísticas basadas en las categorías de noticias del archivo `noticias.txt`.

**✅ IMPORTANTE:** No genera rostros ni personas - todo es interpretación artística abstracta.

## Características

### 🎨 Estilos por Categoría

| Categoría | Colores | Estilo Visual | Descripción |
|-----------|---------|---------------|-------------|
| **Technology** | Azul, Púrpura, Cyan | Circuitos, Ondas, Partículas | Circuitos digitales y ondas tecnológicas |
| **Sports** | Naranja, Verde, Amarillo | Movimiento, Energía | Movimiento y energía abstracta |
| **Politics** | Azul oscuro, Rojo, Gris | Edificios, Monumentos abstractos | Arquitectura y símbolos abstractos |
| **Business** | Azul, Verde, Dorado | Gráficos, Charts | Gráficos y crecimiento visual |
| **Entertainment** | Rosa, Amarillo, Púrpura | Luces, Ondas musicales | Luces y celebración abstracta |
| **Health** | Verde, Azul claro | Formas orgánicas, Bienestar | Formas orgánicas y bienestar |
| **Science** | Púrpura, Cyan, Magenta | Átomos, Moléculas, Espacio | Átomos y conceptos científicos |
| **Environment** | Verde, Eco | Naturaleza, Sostenibilidad | Naturaleza y sostenibilidad |
| **World** | Azul, Naranja, Cyan | Redes, Conexiones globales | Conexiones globales abstractas |
| **Tourism** | Dorado, Azul cielo, Rosa | Paisajes, Horizontes | Paisajes y horizontes |
| **Lifestyle** | Rosa, Lavanda, Melocotón | Minimalismo, Balance | Diseño moderno y equilibrio |

### 🎯 Patrones Visuales

- **Circuitos**: Líneas y conexiones tecnológicas
- **Ondas**: Movimiento sinusoidal dinámico
- **Partículas**: Sistema de puntos interconectados
- **Geométrico**: Formas abstractas (círculos, triángulos, rectángulos)
- **Gráficos**: Charts y líneas de tendencia
- **Redes**: Nodos y conexiones globales

## Instalación

### Dependencias

```bash
pip install Pillow
```

O el script las instalará automáticamente en la primera ejecución.

## Uso

### Ejecución básica

```bash
python3 generate-images.py
```

### Salida

- **Directorio**: `images/news/`
- **Formato**: JPG (calidad 85%)
- **Dimensiones**: 1200x600px (óptimo para web)
- **Nombres**: `{categoria}_{source_id}_{index}.jpg`
- **Índice**: `images/news/index.json`

### Ejemplo de índice generado

```json
[
  {
    "source": "CNN",
    "category": "lifestyle",
    "file": "images/news/lifestyle_cnnespanol_1.jpg",
    "id": "cnnespanol"
  },
  {
    "source": "Contacto Hoy",
    "category": "top",
    "file": "images/news/top_contactohoy_mx_2.jpg",
    "id": "contactohoy_mx"
  }
]
```

## Integración con Templates

### Actualizar base.html

```javascript
// Cargar índice de imágenes
fetch('images/news/index.json')
  .then(response => response.json())
  .then(images => {
    // Asignar imágenes a artículos según categoría
    const featuredImg = document.querySelector('.featured-article img');
    if (featuredImg && images[0]) {
      featuredImg.src = images[0].file;
    }
  });
```

### CSS para imágenes

```css
.article-image img,
.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.article-image img:hover,
.card-image:hover {
  transform: scale(1.05);
}
```

## Personalización

### Cambiar dimensiones

```python
generator = NewsImageGenerator()
generator.width = 1920  # Ancho personalizado
generator.height = 1080  # Alto personalizado
```

### Agregar nueva categoría

```python
CATEGORY_THEMES = {
    'mi_categoria': {
        'colors': [(R, G, B), (R, G, B), (R, G, B)],
        'shapes': ['circuit', 'wave', 'geometric'],
        'description': 'Descripción del estilo'
    }
}
```

### Modificar calidad

```python
img.save(filepath, 'JPEG', quality=95)  # Aumentar calidad
```

## Efectos Visuales

1. **Gradientes**: Fondos con transiciones suaves de color
2. **Blur artístico**: Efecto Gaussian blur sutil (radius=1)
3. **Transparencias**: Capas RGBA para superposiciones
4. **Sombras**: Texto con sombra para mejor legibilidad
5. **Aleatoriedad**: Cada imagen es única gracias a variaciones random

## Ventajas

✅ **Sin copyright**: Todas las imágenes son generadas, no stock photos  
✅ **Consistencia**: Estilo coherente por categoría  
✅ **Personalizable**: Fácil de ajustar colores y estilos  
✅ **Rápido**: Genera 62+ imágenes en segundos  
✅ **Ético**: Sin rostros ni personas, solo arte abstracto  
✅ **Ligero**: JPG optimizado para web  

## Próximos pasos

1. Ejecutar el script: `python3 generate-images.py`
2. Verificar imágenes en `images/news/`
3. Integrar con templates HTML
4. Ajustar estilos según necesidad

## Notas técnicas

- **Fonts**: Usa DejaVu Sans Bold (incluido en sistemas Linux)
- **Fallback**: Si no encuentra font, usa default de PIL
- **Encoding**: UTF-8 para soportar caracteres especiales
- **Error handling**: Try/except para fonts y operaciones de imagen

## Ejemplo de ejecución

```
🎨 Generando imágenes artísticas para 62 fuentes de noticias...
======================================================================

[1/62] CNN
  📁 Categoría: lifestyle
  🎨 Estilo: Diseño moderno y equilibrio
  ✅ Generada: lifestyle_cnnespanol_1.jpg

[2/62] Contacto Hoy
  📁 Categoría: top
  🎨 Estilo: Diseño abstracto y geométrico
  ✅ Generada: top_contactohoy_mx_2.jpg

...

======================================================================
✨ Proceso completado: 62 imágenes generadas
📂 Directorio: /home/admin/news-prototype/images/news
📋 Índice guardado: /home/admin/news-prototype/images/news/index.json
```

---

**Creado con Python + Pillow | Sin IA generativa | 100% Arte Programático**
