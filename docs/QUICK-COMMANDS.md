# ⚡ Quick Commands - Referencia Rápida

> Comandos esenciales para usuarios avanzados

---

## 🎮 Menú Interactivo

```bash
./core/menu.sh                    # Menú principal (RECOMENDADO)
```

---

## 🏗️ Generación

```bash
# Modo rápido (default)
python core/scripts/master_orchestrator.py

# Con verificación WHOIS
python core/scripts/master_orchestrator.py --verificar-dominios

# Usar cache (no descargar)
python core/scripts/master_orchestrator.py --usar-cache

# Output personalizado
python core/scripts/master_orchestrator.py --output-dir /path/to/output
```

---

## 🌐 Servidor HTTP

```bash
# Servir último sitio (port 8000)
python core/scripts/serve_sites.py

# Servir sitio específico
python core/scripts/serve_sites.py --site site_2 --port 8002

# Servir todos (múltiples puertos)
python core/scripts/serve_sites.py --all

# Listar sitios
python core/scripts/serve_sites.py --list

# Detener todos los servidores
pkill -f 'http.server'
```

---

## 🧪 Tests

```bash
# Verificar 16 módulos
python core/scripts/test/test_modulos_completo.py

# Test end-to-end (2 artículos)
python core/scripts/test/test_flujo_completo.py

# Test Blackbox API
python core/scripts/test/test_blackbox.py

# Test parafraseo
python core/scripts/test/test_paraphrase_quick.py

# Test integración
python core/scripts/test/test_integration.py
```

---

## 📚 Documentación

```bash
# Con bat (recomendado)
bat DIAGRAMA-FLUJO-COMPLETO.md
bat AGENTS.md
bat RESUMEN-FLUJO.md

# Con less
less README-GENERADOR.md
less VERIFICACION-MODULOS.md

# Desde el menú
./core/menu.sh → 3 → Seleccionar documento
```

---

## 🔧 Utilidades

```bash
# Limpiar archivos generados
rm -rf output/generated_sites output/generated_sites_test test_output_modules

# Ver estadísticas
./core/menu.sh → 4 → 2

# Verificar API keys
./core/menu.sh → 4 → 3

# Listar sitios
ls -lah output/generated_sites/
```

---

## 📊 Workflows Comunes

### Generar y Visualizar (Fast)

```bash
python core/scripts/master_orchestrator.py --usar-cache && \
python core/scripts/serve_sites.py
```

### Test Completo

```bash
python core/scripts/test/test_modulos_completo.py && \
python core/scripts/test/test_flujo_completo.py
```

### Limpiar y Regenerar

```bash
rm -rf output/generated_sites && \
python core/scripts/master_orchestrator.py && \
python core/scripts/serve_sites.py
```

### Múltiples Sitios Simultáneos

```bash
# Generar 3 sitios (uno por uno)
for i in {1..3}; do
    python core/scripts/master_orchestrator.py --usar-cache
done

# Servir todos
python core/scripts/serve_sites.py --all
```

---

## 🎯 Atajos por Caso de Uso

| Caso | Comando |
|------|---------|
| **Primera generación** | `./core/menu.sh` → 1 → 1 |
| **Generar + Ver** | `./core/menu.sh` → 1 → 1, luego 1 → 6 → 1 |
| **Test rápido** | `./core/menu.sh` → 2 → 1 |
| **Ver docs** | `./core/menu.sh` → 3 |
| **Limpiar** | `./core/menu.sh` → 4 → 1 |
| **Servir último** | `./core/menu.sh` → 1 → 6 → 1 |
| **Servir todos** | `./core/menu.sh` → 1 → 6 → 3 |

---

## 🔗 Navegación Rápida

```bash
# Ir a sitio generado
cd output/generated_sites/site_1

# Ver estructura
ls -lah

# Abrir index en navegador (Linux)
xdg-open index.html

# O servir con HTTP
python -m http.server 8000
```

---

## 💡 Tips

### Desarrollo Rápido:
```bash
# Terminal 1: Auto-regenerar
watch -n 60 'python core/scripts/master_orchestrator.py --usar-cache'

# Terminal 2: Servidor
python core/scripts/serve_sites.py
```

### Testing Continuo:
```bash
# Ejecutar tests antes de cada commit
python core/scripts/test/test_modulos_completo.py && \
python core/scripts/test/test_flujo_completo.py && \
echo "✅ Ready to commit"
```

### Múltiples Puertos:
```bash
# Site 1
python core/scripts/serve_sites.py --site site_1 --port 8001 &

# Site 2
python core/scripts/serve_sites.py --site site_2 --port 8002 &

# Site 3
python core/scripts/serve_sites.py --site site_3 --port 8003 &

# Ver procesos
jobs

# Detener todos
pkill -f 'http.server'
```

---

## ⌨️ Keyboard Shortcuts en Menú

| Tecla | Acción |
|-------|--------|
| `1-9` | Seleccionar opción |
| `0` | Volver atrás |
| `q` | Salir |
| `Ctrl+C` | Interrumpir |
| `Enter` | Continuar (en pausas) |

---

## 🚀 One-Liners Útiles

```bash
# Generar y servir en un comando
python core/scripts/master_orchestrator.py && python core/scripts/serve_sites.py

# Test y generar si OK
python core/scripts/test/test_modulos_completo.py && \
python core/scripts/master_orchestrator.py --usar-cache

# Limpiar, generar y servir
rm -rf output/generated_sites && \
python core/scripts/master_orchestrator.py && \
python core/scripts/serve_sites.py

# Generar múltiples y servir todos
for i in {1..3}; do python core/scripts/master_orchestrator.py --usar-cache; done && \
python core/scripts/serve_sites.py --all

# Ver último sitio generado
python core/scripts/serve_sites.py --list | head -5 && \
python core/scripts/serve_sites.py
```

---

## 📋 Checklist Rápido

### Antes de generar:
- [ ] API keys configuradas: `./core/menu.sh` → 4 → 3
- [ ] Tests OK: `./core/menu.sh` → 2 → 1

### Después de generar:
- [ ] Sitio existe: `ls output/generated_sites/site_1/`
- [ ] 27 archivos: `find output/generated_sites/site_1 -type f | wc -l`
- [ ] Servir: `./core/menu.sh` → 1 → 6 → 1
- [ ] Verificar en navegador: `http://localhost:8000`

---

**Última actualización:** 2026-01-15 15:45  
**Para más detalles:** Ver `MENU-PRINCIPAL.md`
