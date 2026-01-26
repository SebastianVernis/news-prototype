# 🚀 Guía de Inicio Rápido

## Instalación y Configuración

### 1. Instalar Dependencias

#### Backend (Python)
```bash
# Activar tu entorno virtual
source ~/Soluciones_Digitales/bin/activate

# Instalar dependencias
pip install -r backend/requirements.txt
```

#### Frontend (Node.js)
```bash
npm install
```

### 2. Configurar Variables de Entorno

Edita el archivo `.env` en la raíz del proyecto:

```bash
# APIs de noticias (opcionales pero recomendadas)
NEWSAPI_KEY=tu_clave_aqui
NEWSDATA_KEY=tu_clave_aqui

# Blackbox AI para generación de imágenes
BLACKBOX_API_KEY=tu_clave_aqui
```

### 3. Iniciar la Aplicación

#### Terminal 1 - Backend
```bash
npm run backend
```

#### Terminal 2 - Frontend
```bash
npm run dev
```

La aplicación se abrirá automáticamente en `http://localhost:3000`

## 🎯 Uso Básico

### Dashboard
- Ver estadísticas de sitios generados
- Estado del sistema en tiempo real
- Accesos rápidos a funciones principales

### Crear Sitios
1. Ve a "Crear Sitios"
2. Configura la cantidad (1-100 sitios)
3. Opciones:
   - **Generar metadatos**: Crea nombres, dominios y configuraciones únicas
   - **Verificar dominios**: Consulta WHOIS para verificar disponibilidad (más lento)
4. Click en "Generar Sitios"

### Ver Sitios
- Lista todos los sitios generados
- Ver sitio en nueva pestaña
- Eliminar sitios individualmente

### Configuración
- Configurar claves de API
- Ajustar valores predeterminados
- Ver información del sistema

## 📁 Estructura de Archivos

```
news-prototype/
├── backend/           # API Flask
├── frontend/          # Aplicación React
├── scripts/           # Scripts de generación
├── sites/             # Sitios HTML generados
├── data/              # Metadatos y datos
└── templates/         # Templates CSS
```

## 🔧 Comandos Útiles

```bash
# Desarrollo
npm run dev              # Iniciar frontend
npm run backend          # Iniciar backend

# Producción
npm run build            # Build frontend
npm run preview          # Preview build

# Backend
npm run backend:install  # Instalar deps Python
```

## 💡 Tips

1. **Primera vez**: Genera 5 sitios para probar
2. **Verificación de dominios**: Solo usa esto cuando realmente necesites verificar disponibilidad (es lento)
3. **API Keys**: Configura las claves en Settings para obtener noticias reales
4. **Metadatos**: Los archivos de metadatos se guardan automáticamente en `data/sites_metadata/`

## 🐛 Solución de Problemas

### Error: Module 'flask' not found
```bash
# Asegúrate de estar en el venv correcto
source ~/Soluciones_Digitales/bin/activate
pip install -r backend/requirements.txt
```

### Error: CORS
El frontend tiene configurado un proxy. Si ves errores CORS:
- Verifica que el backend esté corriendo en puerto 5000
- Revisa `vite.config.js` para el proxy

### Puerto ocupado
```bash
# Cambiar puerto del backend en backend/app.py (línea final)
# Cambiar puerto del frontend en vite.config.js
```

## 📝 Próximos Pasos

1. Configura tus API keys en Settings
2. Genera tus primeros sitios
3. Explora los diferentes layouts generados
4. Personaliza los templates CSS en `templates/`
