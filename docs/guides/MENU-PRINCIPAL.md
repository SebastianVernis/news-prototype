# 🎮 Menú Principal Interactivo

> Sistema unificado para acceder a todas las funcionalidades del generador

---

## 🚀 Inicio Rápido

```bash
# Desde la raíz del proyecto
./core/menu.sh

# O directamente con Python
python core/menu.py
```

---

## 📋 Opciones Disponibles

### 1️⃣ **Generación de Sitios** 🏗️

```
1) 🚀 Generar sitio completo (20 noticias, modo rápido)
   → python core/scripts/master_orchestrator.py
   → Tiempo: 2-3 minutos
   → Output: output/generated_sites/site_1/

2) 🔍 Generar sitio con verificación de dominios
   → python core/scripts/master_orchestrator.py --verificar-dominios
   → Tiempo: 3-5 minutos (incluye WHOIS)

3) 💾 Generar usando cache de noticias
   → python core/scripts/master_orchestrator.py --usar-cache
   → Tiempo: 1-2 minutos (sin descargar noticias)

4) ⚙️  Generar con opciones personalizadas
   → Permite ingresar argumentos personalizados
   → Ejemplo: --output-dir /custom/path

5) 📊 Ver último sitio generado
   → Muestra ubicación del último sitio
   → Comando para visualizar en navegador

6) 🌐 Servir sitios en navegador ⭐ NUEVO
   ├── 1) Servir último sitio (site_1) en puerto 8000
   ├── 2) Seleccionar sitio específico
   ├── 3) Servir todos los sitios (puertos múltiples)
   └── 4) Listar todos los sitios disponibles
```

### 2️⃣ **Tests y Verificación** 🧪

```
1) ✅ Test de integración de módulos
   → python core/scripts/test/test_modulos_completo.py
   → Verifica los 16 módulos del sistema
   → Tiempo: ~5 segundos

2) 🚀 Test de flujo completo
   → python core/scripts/test/test_flujo_completo.py
   → Test end-to-end con 2 artículos
   → Tiempo: 30-60 segundos

3) 🤖 Test de Blackbox API
   → python core/scripts/test/test_blackbox.py
   → Verifica conexión con Blackbox AI

4) 📝 Test de parafraseo rápido
   → python core/scripts/test/test_paraphrase_quick.py
   → Test del sistema de parafraseo

5) 🔗 Test de integración general
   → python core/scripts/test/test_integration.py
   → Test de integración de componentes

6) 📊 Ver resultados del último test
   → Muestra resultados guardados del último test
```

### 3️⃣ **Documentación** 📚

```
1) 📖 README - Guía principal
   → README.md
   → Documentación del proyecto completo

2) 🚀 README-GENERADOR - Quick Start
   → README-GENERADOR.md
   → Inicio rápido del generador

3) 📊 RESUMEN-FLUJO - Resumen ejecutivo
   → RESUMEN-FLUJO.md
   → Resumen de 1 página

4) 🔄 DIAGRAMA-FLUJO-COMPLETO - Arquitectura
   → DIAGRAMA-FLUJO-COMPLETO.md
   → Flujo detallado paso a paso

5) 🤖 AGENTS - Guía para desarrolladores
   → AGENTS.md
   → Reglas, mejores prácticas, historial

6) ✅ VERIFICACION-MODULOS - Test de integración
   → VERIFICACION-MODULOS.md
   → Verificación de 16 módulos

7) 📑 INDEX-DOCUMENTACION - Índice completo
   → INDEX-DOCUMENTACION.md
   → Navegación por toda la documentación

8) 📂 Ver estructura del proyecto
   → Muestra árbol de directorios
```

### 4️⃣ **Utilidades** 🔧

```
1) 🧹 Limpiar archivos generados
   → Elimina output/generated_sites/, output/generated_sites_test/, test_output_modules/
   → Requiere confirmación

2) 📊 Ver estadísticas del sistema
   → Muestra estadísticas de módulos y combinaciones

3) 🔍 Verificar API keys
   → Verifica que las API keys estén configuradas
   → Muestra claves enmascaradas

4) 📁 Abrir directorio de sitios generados
   → Lista sitios en output/generated_sites/

5) 💾 Ver archivos de datos
   → Lista archivos JSON en content/data/

6) 🎨 Ver templates CSS disponibles
   → Lista templates en content/templates/css/
```

---

## ⌨️ Navegación

| Tecla | Acción |
|-------|--------|
| `1-9` | Seleccionar opción del menú actual |
| `0` | Volver al menú anterior |
| `q` | Salir del programa |
| `Ctrl+C` | Salir inmediatamente |

---

## 🎨 Características del Menú

✅ **Interfaz con colores** - Mejor legibilidad  
✅ **Navegación intuitiva** - Menús anidados  
✅ **Ejecución de scripts** - Directo desde el menú  
✅ **Visualización de docs** - Con bat/less/cat  
✅ **Servidor HTTP integrado** - ⭐ Servir sitios sin salir del menú  
✅ **Múltiples sitios** - Servir todos simultáneamente  
✅ **Confirmaciones** - Para operaciones destructivas  
✅ **Estadísticas** - Información del sistema  
✅ **Verificación de estado** - API keys, archivos, etc.  

---

## 🔧 Requisitos

### Sistema:
- Python 3.8+
- Bash shell (Linux/macOS) o Git Bash (Windows)

### Opcional (mejora la experiencia):
```bash
# Para mejor visualización de documentación
sudo apt-get install bat  # Ubuntu/Debian
brew install bat          # macOS
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Generar y visualizar un sitio

```bash
./core/menu.sh
# Seleccionar: 1 (Generación de Sitios)
# Seleccionar: 1 (Generar sitio completo)
# Esperar 2-3 minutos
# ✅ Sitio en output/generated_sites/site_1/

# Visualizar en navegador
# Seleccionar: 6 (Servir sitios)
# Seleccionar: 1 (Servir último sitio)
# Abrir: http://localhost:8000
# Ctrl+C para detener
```

### Ejemplo 2: Verificar que todo funciona

```bash
./core/menu.sh
# Seleccionar: 2 (Tests y Verificación)
# Seleccionar: 1 (Test de integración de módulos)
# Ver resultado: ✅ 16/16 módulos verificados
```

### Ejemplo 3: Leer documentación

```bash
./core/menu.sh
# Seleccionar: 3 (Documentación)
# Seleccionar: 3 (RESUMEN-FLUJO)
# Leer con less/bat (q para salir)
```

### Ejemplo 4: Verificar configuración

```bash
./core/menu.sh
# Seleccionar: 4 (Utilidades)
# Seleccionar: 3 (Verificar API keys)
# Ver estado de las claves
```

### Ejemplo 5: Servir un sitio específico

```bash
./core/menu.sh
# Seleccionar: 1 (Generación de Sitios)
# Seleccionar: 6 (Servir sitios)
# Seleccionar: 2 (Seleccionar sitio específico)
# Ingresar número del sitio (ej: 2)
# Ingresar puerto (ej: 8002 o Enter para 8000)
# Abrir navegador en http://localhost:8002
# Ctrl+C para detener
```

### Ejemplo 6: Servir múltiples sitios simultáneamente

```bash
./core/menu.sh
# Seleccionar: 1 (Generación de Sitios)
# Seleccionar: 6 (Servir sitios)
# Seleccionar: 3 (Servir todos los sitios)
# Confirmar con 's'
# Ver URLs: http://localhost:8000, :8001, :8002, etc.
# Para detener: pkill -f 'http.server'
```

---

## 🎯 Flujo de Trabajo Recomendado

### Primera vez:

```
1. ./core/menu.sh
2. → 4 (Utilidades) → 3 (Verificar API keys)
3. Si falta alguna: Configurar .env
4. → 2 (Tests) → 1 (Test de módulos)
5. Si ✅: → 1 (Generación) → 1 (Generar sitio)
6. → 1 (Generación) → 6 (Servir sitios) → 1 (Último sitio)
7. Abrir http://localhost:8000 en navegador
8. Explorar el sitio generado
9. Ctrl+C para detener servidor
```

### Desarrollo:

```
1. Editar código
2. ./core/menu.sh → 2 (Tests) → 1 (Verificar módulos)
3. Si ✅: → 2 (Tests) → 2 (Test flujo completo)
4. Si ✅: → 1 (Generación) → 3 (Usar cache)
5. → 1 (Generación) → 6 (Servir) → 1 (Último sitio)
6. Verificar cambios en http://localhost:8000
7. Ctrl+C cuando termine
```

### Producción:

```
# CLI directo (sin menú)
python core/scripts/master_orchestrator.py --usar-cache
```

---

## 🐛 Troubleshooting

### El menú no inicia:
```bash
# Verificar permisos
chmod +x core/menu.sh core/menu.py

# Ejecutar directamente
python3 core/menu.py
```

### Colores no se ven bien:
Los colores ANSI están soportados en:
- ✅ Linux terminal
- ✅ macOS terminal
- ✅ Windows Terminal / Git Bash
- ❌ CMD antiguo de Windows (usar Git Bash)

### Script no encuentra módulos:
El menú ejecuta scripts desde la raíz del proyecto, por lo que los paths son correctos automáticamente.

---

## 🌐 Funcionalidad de Servidor HTTP

### Modo 1: Servir Último Sitio
```bash
Puerto: 8000
URL: http://localhost:8000
Comando equivalente: cd output/generated_sites/site_1 && python -m http.server 8000
```

### Modo 2: Servir Sitio Específico
```bash
Seleccionar de lista de sitios disponibles
Puerto: Personalizable (default: 8000)
Muestra: Nombre, número de páginas, tamaño
```

### Modo 3: Servir Todos los Sitios
```bash
Puertos: 8000, 8001, 8002, ... (auto-incremento)
Proceso: Background (servidores en segundo plano)
Detener: pkill -f 'http.server'

Ejemplo con 3 sitios:
- site_1: http://localhost:8000
- site_2: http://localhost:8001
- site_3: http://localhost:8002
```

### Modo 4: Listar Sitios
```bash
Muestra:
- Nombre del sitio
- Título del sitio
- Número de páginas HTML
- Número de imágenes
- Tamaño total en MB
- Puerto sugerido
```

---

## 📊 Estructura del Menú

```
MENÚ PRINCIPAL
├── 1. Generación de Sitios
│   ├── 1. Generar rápido
│   ├── 2. Con verificación dominios
│   ├── 3. Usar cache
│   ├── 4. Personalizado
│   ├── 5. Ver último sitio
│   └── 6. Servir sitios 🌐 ⭐ NUEVO
│       ├── 1. Servir último (port 8000)
│       ├── 2. Seleccionar específico
│       ├── 3. Servir todos (múltiples puertos)
│       └── 4. Listar todos
│
├── 2. Tests y Verificación
│   ├── 1. Test módulos (16)
│   ├── 2. Test flujo completo
│   ├── 3. Test Blackbox API
│   ├── 4. Test parafraseo
│   ├── 5. Test integración
│   └── 6. Ver resultados
│
├── 3. Documentación
│   ├── 1. README
│   ├── 2. README-GENERADOR
│   ├── 3. RESUMEN-FLUJO
│   ├── 4. DIAGRAMA-FLUJO-COMPLETO
│   ├── 5. AGENTS
│   ├── 6. VERIFICACION-MODULOS
│   ├── 7. INDEX-DOCUMENTACION
│   └── 8. Estructura del proyecto
│
└── 4. Utilidades
    ├── 1. Limpiar archivos
    ├── 2. Estadísticas
    ├── 3. Verificar API keys
    ├── 4. Ver sitios generados
    ├── 5. Ver datos
    └── 6. Ver templates CSS
```

---

## 🔗 Referencias

- **Código fuente:** `core/menu.py`
- **Launcher:** `core/menu.sh`
- **Documentación completa:** `INDEX-DOCUMENTACION.md`
- **Tests:** `core/scripts/test/`

---

**Última actualización:** 2026-01-15 15:25  
**Versión:** 1.0  
**Estado:** ✅ Funcional
