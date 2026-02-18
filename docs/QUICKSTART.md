# 🚀 Guía de Inicio Rápido

## Instalación y Configuración

### 1. Instalar Dependencias

#### Backend (Python)
```bash
# Activar tu entorno virtual
source ~/Soluciones_Digitales/bin/activate

# Instalar dependencias
pip install -r core/requirements.txt
pip install -r apps/backend/requirements.txt
```

#### Frontend (Node.js)
```bash
cd apps/frontend
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
python3 apps/backend/app.py
```

#### Terminal 2 - Frontend
```bash
cd apps/frontend
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
├── apps/backend/           # API Flask
├── apps/frontend/          # Aplicación React
├── core/scripts/           # Scripts de generación
├── output/sites/             # Sitios HTML generados
├── content/data/              # Metadatos y datos
└── content/templates/         # Templates CSS
```

## 🔧 Comandos Útiles

```bash
# Desarrollo
cd apps/frontend && npm run dev  # Iniciar frontend
python3 apps/backend/app.py      # Iniciar backend

# Producción
npm run build            # Build frontend
npm run preview          # Preview build

# Backend
pip install -r apps/backend/requirements.txt  # Instalar deps Python
```

## 💡 Tips

1. **Primera vez**: Genera 5 sitios para probar
2. **Verificación de dominios**: Solo usa esto cuando realmente necesites verificar disponibilidad (es lento)
3. **API Keys**: Configura las claves en Settings para obtener noticias reales
4. **Metadatos**: Los archivos de metadatos se guardan automáticamente en `content/data/sites_metadata/`

## 🐛 Solución de Problemas

### Error: Module 'flask' not found
```bash
# Asegúrate de estar en el venv correcto
source ~/Soluciones_Digitales/bin/activate
pip install -r apps/backend/requirements.txt
```

### Error: CORS
El frontend tiene configurado un proxy. Si ves errores CORS:
- Verifica que el backend esté corriendo en puerto 5000
- Revisa `apps/frontend/vite.config.js` para el proxy

### Puerto ocupado
```bash
# Cambiar puerto del backend en apps/backend/app.py (línea final)
# Cambiar puerto del frontend en apps/frontend/vite.config.js
```

## 📝 Próximos Pasos

1. Configura tus API keys en Settings
2. Genera tus primeros sitios
3. Explora los diferentes layouts generados
4. Personaliza los templates CSS en `content/templates/`
