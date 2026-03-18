# 🚀 Quick Start - Despliegue de Nuevos Sitios

## Resumen Ejecutivo

Se han preparado **17 nuevos sitios** para expandir la red NexoPress de 10 a **27 sitios totales**.

---

## 📁 Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| `scripts/add_new_sites.sql` | SQL para agregar sitios a la DB |
| `scripts/deploy_new_sites.sh` | Script bash para desplegar a Pages |
| `scripts/setup_new_sites_fb_tokens.py` | Script Python para configurar FB tokens |
| `scripts/DEPLOYMENT_GUIDE.md` | Guía completa de despliegue |

---

## ⚡ Despliegue Rápido (3 Pasos)

### 1️⃣ Actualizar Worker (API)
```bash
cd /mnt/c/Users/soluc/cloudflare-news-project/src
wrangler deploy --config wrangler.toml
```

### 2️⃣ Agregar Sitios a la DB
```bash
cd /mnt/c/Users/soluc/cloudflare-news-project
wrangler d1 execute news_db --file scripts/add_new_sites.sql --remote
```

### 3️⃣ Desplegar Sitios a Pages
```bash
chmod +x scripts/deploy_new_sites.sh
./scripts/deploy_new_sites.sh
```

---

## 🔐 Configurar Facebook (Opcional)

```bash
python3 scripts/setup_new_sites_fb_tokens.py
```

---

## ✅ Verificación

```bash
# Verificar DB (debería mostrar 27)
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM SITIOS" --remote

# Verificar Worker
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status

# Verificar RSS de nuevo sitio
curl -s "https://news-api.sebastianvernis.workers.dev/api/rss/boominformativo" | head -10
```

---

## 📋 Lista de Nuevos Sitios

1. boominformativo
2. capitalpress
3. diarioexpress
4. elpulsomexicano
5. enfoquecapital
6. enfoquedirecto
7. formulacdmx
8. mexicantimes
9. mexico360noticias
10. mradio
11. noticiashorizonte
12. pulsodiario
13. puntoclave
14. puntonoticias
15. radarinformativo
16. reportediario
17. televisionabc

---

## 🆘 Solución de Problemas

| Problema | Solución |
|----------|----------|
| Error "Project already exists" | Usar `--branch=main` en deploy |
| Error "UNIQUE constraint failed" | El sitio ya existe en DB, ignorar |
| Error "Secret not found" | Configurar token con `wrangler secret put` |

---

## 📚 Documentación Completa

Ver `scripts/DEPLOYMENT_GUIDE.md` para instrucciones detalladas.

---

**Actualizado:** Marzo 2026  
**Total sitios:** 27 (10 estables + 17 nuevos)
