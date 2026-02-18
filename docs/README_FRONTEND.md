# Frontend - News Prototype Manager

Interfaz web moderna para gestionar la creación y administración de sitios de noticias generados automáticamente.

## 🎨 Características

- **Dashboard Interactivo**: Visualiza estadísticas y estado del sistema
- **Creador de Sitios**: Interfaz intuitiva para generar múltiples sitios
- **Gestión de Sitios**: Lista, visualiza y administra sitios generados
- **Configuración**: Gestiona API keys y opciones del sistema
- **Diseño Responsive**: Funciona en desktop, tablet y móvil

## 🛠️ Tecnologías

- **React 19** con Hooks
- **Vite** para desarrollo rápido
- **React Router** para navegación
- **Axios** para llamadas API
- **Lucide React** para iconos
- **CSS Modules** para estilos

## 📦 Instalación

```bash
# Instalar dependencias frontend
cd apps/frontend
npm install

# Instalar backend
pip install -r apps/backend/requirements.txt
```

## 🚀 Uso

### Modo Desarrollo

```bash
# Terminal 1: Iniciar frontend
cd apps/frontend
npm run dev

# Terminal 2: Iniciar backend
python3 apps/backend/app.py
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Producción

```bash
# Construir para producción
cd apps/frontend
npm run build

# Vista previa de producción
npm run preview
```

## 📁 Estructura del Proyecto

```
apps/frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   └── Header.jsx       # Navegación principal
│   ├── pages/               # Páginas de la aplicación
│   │   ├── Dashboard.jsx    # Vista principal
│   │   ├── CreateSites.jsx  # Creador de sitios
│   │   ├── SitesList.jsx    # Lista de sitios
│   │   └── Settings.jsx     # Configuración
│   ├── services/            # Servicios y API
│   │   └── api.js          # Cliente API
│   ├── App.jsx             # Componente principal
│   ├── main.jsx            # Punto de entrada
│   └── index.css           # Estilos globales
├── index.html              # HTML base
└── .env.example            # Variables de entorno

apps/backend/
├── app.py                  # Servidor Flask
└── requirements.txt        # Dependencias Python
```

## 🎯 Funcionalidades Principales

### 1. Dashboard
- Estadísticas en tiempo real
- Estado de servicios
- Acciones rápidas
- Métricas de sitios generados

### 2. Crear Sitios
- Configuración de cantidad (1-100 sitios)
- Opciones de metadatos
- Verificación de dominios WHOIS
- Feedback en tiempo real

### 3. Mis Sitios
- Lista de sitios generados
- Vista previa rápida
- Descargar sitios
- Eliminar sitios

### 4. Configuración
- Gestión de API Keys (NewsAPI, NewsData, Blackbox AI)
- Opciones de generación
- Información del sistema

## 🔌 API Backend

El frontend se comunica con un servidor Flask que expone los siguientes endpoints:

### Sitios
- `GET /api/sites` - Lista todos los sitios
- `POST /api/sites/generate` - Genera nuevos sitios
- `GET /api/sites/stats` - Obtiene estadísticas
- `DELETE /api/sites/:id` - Elimina un sitio

### Metadatos
- `GET /api/metadata` - Lista archivos de metadatos
- `GET /api/metadata/:filename` - Obtiene metadatos específicos

### Configuración
- `GET /api/settings` - Obtiene configuración
- `PUT /api/settings` - Actualiza configuración
- `GET /api/settings/status` - Estado del sistema

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# API Keys
NEWSAPI_KEY=tu_clave_newsapi
NEWSDATA_KEY=tu_clave_newsdata
BLACKBOX_API_KEY=tu_clave_blackbox

# Frontend
VITE_API_URL=http://localhost:5000/api
```

### API Keys Requeridas

1. **NewsAPI**: https://newsapi.org/
2. **NewsData**: https://newsdata.io/
3. **Blackbox AI**: Para generación de imágenes

## 🎨 Personalización

### Colores

Los colores se definen en `apps/frontend/src/index.css`:

```css
:root {
  --primary: #2C3E50;
  --secondary: #3498DB;
  --accent: #E74C3C;
  --success: #27AE60;
  --warning: #F39C12;
  --danger: #E74C3C;
}
```

### Componentes

Cada componente tiene su propio archivo CSS para facilitar la personalización:

- `Header.css` - Navegación
- `Dashboard.css` - Dashboard
- `CreateSites.css` - Creador
- `SitesList.css` - Lista
- `Settings.css` - Configuración

## 🐛 Resolución de Problemas

### El frontend no se conecta al backend

1. Verifica que el backend esté corriendo en el puerto 5000
2. Revisa la configuración de `VITE_API_URL` en `.env`
3. Verifica CORS en `apps/backend/app.py`

### Error al generar sitios

1. Verifica las API keys en configuración
2. Revisa los logs del backend
3. Asegúrate de tener los scripts Python instalados

### Estilos no se aplican

1. Limpia el cache: `rm -rf node_modules/.vite`
2. Reinicia el servidor de desarrollo
3. Verifica imports CSS en los componentes

## 📱 Responsive Design

La interfaz es completamente responsive y se adapta a:

- **Desktop**: Layout completo con sidebar
- **Tablet**: Layout adaptado con menú colapsable
- **Mobile**: Vista optimizada con navegación inferior

Breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🚀 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Exportación de sitios en ZIP
- [ ] Editor visual de layouts
- [ ] Preview en tiempo real
- [ ] Análisis de SEO
- [ ] Programación de generaciones
- [ ] Integración con CDN
- [ ] Métricas de rendimiento

## 📝 Licencia

ISC
