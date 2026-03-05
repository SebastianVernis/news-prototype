# CMS - Sistema de Gestión de Contenidos

## Descripción

Cada uno de los 10 sitios de noticias cuenta con un **panel de administración CMS completo** con autenticación segura mediante token de 64 dígitos (256 bits).

## Estructura del CMS

```
sites/[nombre-sitio]/admin/
├── index.html          # Dashboard principal
├── login.html          # Página de autenticación
├── style.css           # Estilos del CMS
├── script.js           # Lógica del dashboard
└── login.js            # Lógica de autenticación
```

## 🔐 Autenticación

### Token de 64 Dígitos

Cada sitio tiene un **token único hexadecimal de 64 caracteres** que proporciona:
- **256 bits de seguridad**
- Validación de formato estricta
- Almacenamiento seguro en sessionStorage
- Expiración al cerrar el navegador

### Tokens Generados

Los tokens están guardados en: `sites/CMS_TOKENS.txt`

**⚠️ IMPORTANTE:** Guarde este archivo en un lugar seguro. Sin el token, no podrá acceder al panel de administración.

## 🚀 Cómo Acceder al CMS

### Opción 1: Local (Desarrollo)

1. Inicie un servidor web en el directorio del sitio:
```bash
cd sites/radiocinconoticias
python3 -m http.server 8000
```

2. Abra el navegador en: `http://localhost:8000/admin/login.html`

3. Ingrese el token correspondiente al sitio (de `CMS_TOKENS.txt`)

4. ¡Listo! Accederá al dashboard

### Opción 2: Cloudflare Pages

1. Despliegue el sitio:
```bash
wrangler pages deploy ./sites/radiocinconoticias --project-name=radiocinconoticias
```

2. Acceda a: `https://radiocinconoticias.pages.dev/admin/login.html`

3. Ingrese su token

## 📋 Funcionalidades del CMS

### Dashboard
- **Estadísticas en tiempo real:**
  - Total de artículos
  - Artículos publicados
  - Borradores
  - Conteo por categorías

- **Tabla de artículos recientes** con acciones rápidas

### Gestión de Artículos

#### Crear Artículo
1. Navegue a "Nuevo Artículo"
2. Complete los campos:
   - **Título** (requerido)
   - **Slug** (se genera automáticamente)
   - **Extracto** (descripción corta)
   - **Contenido** (requerido, editor de texto completo)
   - **Categoría** (nacional, política, economía, deportes, cultura, tecnología)
   - **Autor**
   - **URL de imagen** destacada
   - **Etiquetas** (separadas por comas)
   - **Estado** (publicado/borrador)
   - **Destacado** (toggle)

3. Click en "Guardar Artículo"

#### Editar Artículo
1. Vaya a "Artículos"
2. Click en el ícono de editar (✏️)
3. Modifique los campos necesarios
4. Click en "Guardar Artículo"

#### Eliminar Artículo
1. Vaya a "Artículos"
2. Click en el ícono de eliminar (🗑️)
3. Confirme la eliminación

### Búsqueda
- Barra de búsqueda en tiempo real
- Filtra por título y categoría
- Resultados instantáneos

### Categorías
- Vista general de artículos por categoría
- Conteo en tiempo real

### Configuración
- **Visualización del token** actual (parcial)
- **Regenerar token** (invalida el anterior)
- **Exportar artículos** en formato JSON

## 🛡️ Seguridad

### Validación del Token
```javascript
// El token debe ser exactamente 64 caracteres hexadecimales
/^[a-fA-F0-9]{64}$/.test(token)
```

### Almacenamiento
- **sessionStorage**: El token se elimina al cerrar el navegador
- **localStorage**: Los artículos se guardan localmente

### Recomendaciones de Seguridad
1. **Nunca comparta su token**
2. **Regenerar token** si sospecha compromiso
3. **Cerrar sesión** después de usar
4. **Usar HTTPS** en producción

## 💾 Almacenamiento de Datos

### LocalStorage
Los artículos se almacenan en el navegador del usuario:
```javascript
localStorage.setItem('cms_articles_[sitio]', JSON.stringify(articles));
```

**Limitaciones:**
- Los datos son locales al navegador
- No hay sincronización entre dispositivos
- Ideal para desarrollo y sitios pequeños

### Exportar Datos
Para respaldar o migrar artículos:
1. Vaya a Configuración
2. Click en "Exportar Artículos (JSON)"
3. Guarde el archivo `articles-export.json`

### Importar Datos (Manual)
```javascript
// En la consola del navegador:
const data = /* pegar contenido del JSON */;
localStorage.setItem('cms_articles_[sitio]', JSON.stringify(data));
location.reload();
```

## 🎨 Personalización

### Colores del CMS
El CMS hereda los colores de cada sitio:
```css
:root {
    --primary: #color-primario;
    --secondary: #color-acento;
}
```

### Branding
- Logo del sitio en el header
- Ícono personalizado por sitio
- Nombre del sitio en la sidebar

## 📱 Diseño Responsivo

El CMS es completamente responsivo:
- **Escritorio:** Sidebar fija, dashboard completo
- **Tablet:** Sidebar colapsable
- **Móvil:** Menú hamburguesa, vista simplificada

## 🔧 Comandos Útiles

### Limpiar Datos del CMS
```javascript
// En la consola del navegador:
localStorage.removeItem('cms_articles_[sitio]');
sessionStorage.clear();
location.reload();
```

### Ver Artículos Guardados
```javascript
// En la consola del navegador:
const articles = JSON.parse(localStorage.getItem('cms_articles_[sitio]'));
console.table(articles);
```

### Generar Token de Prueba
```javascript
// En la consola del navegador (login):
function generateSampleToken() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, b => b.toString(16).padStart(2, '0')).join('');
}
generateSampleToken();
```

## 🐛 Solución de Problemas

### "Token inválido"
- Verifique que el token tenga exactamente 64 caracteres
- Asegúrese de copiar todo el token (sin espacios)
- El token debe ser hexadecimal (0-9, a-f)

### "No se cargan los artículos"
- Verifique que haya permitido localStorage
- Intente limpiar el caché del navegador
- Revise la consola para errores

### "El CMS no carga"
- Verifique que los archivos estén en la carpeta `/admin`
- Asegúrese de usar un servidor web (no abrir directamente)
- Revise la consola del navegador para errores

## 📊 Estadísticas del CMS

| Sitio | Token | Artículos por Defecto |
|-------|-------|----------------------|
| Radio Cinco Noticias | Ver `CMS_TOKENS.txt` | 1 |
| Central México | Ver `CMS_TOKENS.txt` | 1 |
| TV México | Ver `CMS_TOKENS.txt` | 1 |
| CBN Noticias | Ver `CMS_TOKENS.txt` | 1 |
| México Informado | Ver `CMS_TOKENS.txt` | 1 |
| Nodo Informativo | Ver `CMS_TOKENS.txt` | 1 |
| Bitácora Urbana | Ver `CMS_TOKENS.txt` | 1 |
| Reporte Central MX | Ver `CMS_TOKENS.txt` | 1 |
| Vértice Noticias | Ver `CMS_TOKENS.txt` | 1 |
| Vanguardia Tecámac | Ver `CMS_TOKENS.txt` | 1 |

## 🔮 Próximas Características

- [ ] Integración con API backend
- [ ] Subida de imágenes (drag & drop)
- [ ] Editor WYSIWYG completo
- [ ] Programación de publicaciones
- [ ] Múltiples usuarios
- [ ] Historial de revisiones
- [ ] SEO meta tags editor
- [ ] Analytics integrado

---

**Generado:** 19 de Febrero, 2026  
**Versión del CMS:** 1.0.0  
**Seguridad:** Token 256-bit
