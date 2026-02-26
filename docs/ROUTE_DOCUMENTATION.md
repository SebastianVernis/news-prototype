# Documentación del Sistema de Rutas - Sitio Web de Noticias

## Estructura de Rutas

### Rutas Principales
- `/` - Página principal con noticias destacadas
- `/categoria/nacional` - Noticias nacionales
- `/categoria/internacional` - Noticias internacionales
- `/categoria/politica` - Noticias políticas
- `/categoria/economia` - Noticias económicas
- `/categoria/deportes` - Noticias deportivas
- `/categoria/cultura` - Noticias culturales
- `/categoria/opinion` - Artículos de opinión

### Rutas de Contenido
- `/articulo/[titulo-del-articulo]` - Página individual de artículo
- `/articulo/presidente-plan-economico` - Ejemplo de artículo
- `/articulo/reformas-legislativas` - Otro ejemplo

### Rutas de Páginas Legales
- `/acerca-de` - Página "Acerca de"
- `/contacto` - Página de contacto
- `/privacidad` - Política de privacidad
- `/terminos` - Términos de uso
- `/archivo` - Archivo de noticias

## Configuración de Rutas

### _routes.json
El archivo `_routes.json` en el directorio público define qué rutas deben ser manejadas por el worker dinámico:

```json
{
  "version": 1,
  "include": [
    "/*"
  ],
  "exclude": [
    "/static/*",
    "/assets/*",
    "/favicon.ico",
    "/sitemap.xml",
    "/robots.txt"
  ]
}
```

### _worker.js
El archivo `_worker.js` maneja las rutas dinámicas y proporciona funcionalidad adicional para las páginas de Cloudflare.

## Funcionamiento de las Rutas

1. **Rutas Estáticas**: Archivos HTML, CSS, JS, imágenes se sirven directamente
2. **Rutas Dinámicas**: Categorías y artículos se manejan con el sistema de worker
3. **API Routes**: Rutas que comienzan con `/api/` se manejan como endpoints API

## Enlaces Internos

Todos los enlaces internos deben usar rutas absolutas para funcionar correctamente:

✅ Correcto:
```html
<a href="/categoria/nacional">Nacional</a>
<a href="/articulo/titulo-del-articulo">Leer artículo</a>
<a href="/acerca-de">Acerca de</a>
```

❌ Incorrecto:
```html
<a href="./categoria/nacional">Nacional</a>
<a href="articulo/titulo-del-articulo">Leer artículo</a>
```

## Implementación de Navegación

La navegación principal en el sitio incluye:
- Enlaces a categorías principales
- Enlaces a páginas legales
- Enlaces a artículos populares
- Sistema de búsqueda funcional

## Solución de Problemas Comunes

### Problemas de Enrutamiento
- Verificar que todos los enlaces usen rutas absolutas
- Asegurarse de que los archivos HTML estén en las rutas correctas
- Confirmar que el archivo `_routes.json` esté correctamente configurado

### Páginas que Redirigen al Index
- Verificar que no haya redirecciones incorrectas en el código
- Asegurarse de que las rutas coincidan con los archivos existentes
- Probar las rutas en diferentes navegadores

## Pruebas de Funcionalidad

Después de cada despliegue, verificar:

1. Página principal carga correctamente
2. Enlaces de categorías funcionan
3. Enlaces de artículos funcionan
4. Páginas legales son accesibles
5. Navegación funciona en todas las páginas
6. Sistema de búsqueda funciona
7. Sidebar con categorías funciona

## Mantenimiento

- Actualizar `_routes.json` cuando se agreguen nuevas rutas dinámicas
- Verificar periódicamente que todos los enlaces internos funcionen
- Asegurarse de que las páginas nuevas se generen en las rutas correctas
- Probar la navegación en diferentes dispositivos y navegadores