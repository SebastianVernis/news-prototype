# ⚡ Quick Commands - Referencia Rápida

> Comandos esenciales para usuarios avanzados

---

## 🎮 Menú Interactivo

```bash
./menu.sh                    # Menú principal (RECOMENDADO)
```

---

## 🏗️ Generación

```bash
# Modo rápido (default)
python scripts/master_orchestrator.py

# Con verificación WHOIS
python scripts/master_orchestrator.py --verificar-dominios

# Usar cache (no descargar)
python scripts/master_orchestrator.py --usar-cache

# Output personalizado
python scripts/master_orchestrator.py --output-dir /path/to/output
```

---

## 🌐 Servidor HTTP

```bash
# Servir último sitio (port 8000)
python scripts/serve_sites.py

# Servir sitio específico
python scripts/serve_sites.py --site site_2 --port 8002

# Servir todos (múltiples puertos)
python scripts/serve_sites.py --all

# Listar sitios
python scripts/serve_sites.py --list

# Detener todos los servidores
pkill -f 'http.server'
```

---

## 🧪 Tests

```bash
# Verificar 16 módulos
python scripts/test/test_modulos_completo.py

# Test end-to-end (2 artículos)
python scripts/test/test_flujo_completo.py

# Test Blackbox API
python scripts/test/test_blackbox.py

# Test parafraseo
python scripts/test/test_paraphrase_quick.py

# Test integración
python scripts/test/test_integration.py
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
./menu.sh → 3 → Seleccionar documento
```

---

## 🔧 Utilidades

```bash
# Limpiar archivos generados
rm -rf generated_sites generated_sites_test test_output_modules

# Ver estadísticas
./menu.sh → 4 → 2

# Verificar API keys
./menu.sh → 4 → 3

# Listar sitios
ls -lah generated_sites/
```

---

## 📊 Workflows Comunes

### Generar y Visualizar (Fast)

```bash
python scripts/master_orchestrator.py --usar-cache && \
python scripts/serve_sites.py
```

### Test Completo

```bash
python scripts/test/test_modulos_completo.py && \
python scripts/test/test_flujo_completo.py
```

### Limpiar y Regenerar

```bash
rm -rf generated_sites && \
python scripts/master_orchestrator.py && \
python scripts/serve_sites.py
```

### Múltiples Sitios Simultáneos

```bash
# Generar 3 sitios (uno por uno)
for i in {1..3}; do
    python scripts/master_orchestrator.py --usar-cache
done

# Servir todos
python scripts/serve_sites.py --all
```

---

## 🎯 Atajos por Caso de Uso

| Caso | Comando |
|------|---------|
| **Primera generación** | `./menu.sh` → 1 → 1 |
| **Generar + Ver** | `./menu.sh` → 1 → 1, luego 1 → 6 → 1 |
| **Test rápido** | `./menu.sh` → 2 → 1 |
| **Ver docs** | `./menu.sh` → 3 |
| **Limpiar** | `./menu.sh` → 4 → 1 |
| **Servir último** | `./menu.sh` → 1 → 6 → 1 |
| **Servir todos** | `./menu.sh` → 1 → 6 → 3 |

---

## 🔗 Navegación Rápida

```bash
# Ir a sitio generado
cd generated_sites/site_1

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
watch -n 60 'python scripts/master_orchestrator.py --usar-cache'

# Terminal 2: Servidor
python scripts/serve_sites.py
```

### Testing Continuo:
```bash
# Ejecutar tests antes de cada commit
python scripts/test/test_modulos_completo.py && \
python scripts/test/test_flujo_completo.py && \
echo "✅ Ready to commit"
```

### Múltiples Puertos:
```bash
# Site 1
python scripts/serve_sites.py --site site_1 --port 8001 &

# Site 2
python scripts/serve_sites.py --site site_2 --port 8002 &

# Site 3
python scripts/serve_sites.py --site site_3 --port 8003 &

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
python scripts/master_orchestrator.py && python scripts/serve_sites.py

# Test y generar si OK
python scripts/test/test_modulos_completo.py && \
python scripts/master_orchestrator.py --usar-cache

# Limpiar, generar y servir
rm -rf generated_sites && \
python scripts/master_orchestrator.py && \
python scripts/serve_sites.py

# Generar múltiples y servir todos
for i in {1..3}; do python scripts/master_orchestrator.py --usar-cache; done && \
python scripts/serve_sites.py --all

# Ver último sitio generado
python scripts/serve_sites.py --list | head -5 && \
python scripts/serve_sites.py
```

---

## 📋 Checklist Rápido

### Antes de generar:
- [ ] API keys configuradas: `./menu.sh` → 4 → 3
- [ ] Tests OK: `./menu.sh` → 2 → 1

### Después de generar:
- [ ] Sitio existe: `ls generated_sites/site_1/`
- [ ] 27 archivos: `find generated_sites/site_1 -type f | wc -l`
- [ ] Servir: `./menu.sh` → 1 → 6 → 1
- [ ] Verificar en navegador: `http://localhost:8000`

---

**Última actualización:** 2026-01-15 15:45  
**Para más detalles:** Ver `MENU-PRINCIPAL.md`
