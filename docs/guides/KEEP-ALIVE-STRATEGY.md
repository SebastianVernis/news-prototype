# Estrategia Anti-Suspensión para Render Free Tier

## 🎯 Problema

Render Free Tier suspende servicios después de **15 minutos de inactividad** (sin requests HTTP). El servicio entra en "sleep mode" y tarda ~30-60 segundos en despertar cuando llega una nueva request.

## ✅ Soluciones Implementadas

### 1. Cron Job en Render (Recomendado)

**Configuración**: `render.yaml`

```yaml
# Cron job que hace ping cada 10 minutos
- type: cron
  name: news-generator-keep-alive
  schedule: "*/10 * * * *"  # Cada 10 minutos
  startCommand: "python scripts/keep_alive_cron.py"
```

**Ventajas:**
- ✅ Nativo de Render
- ✅ No requiere servicios externos
- ✅ Gratuito
- ✅ Confiable

**Cómo funciona:**
1. Cada 10 minutos ejecuta `keep_alive_cron.py`
2. Script hace ping a `/api/health` y `/api/keep-alive`
3. Backend recibe request y se mantiene activo
4. Nunca llega a los 15 minutos de inactividad

### 2. GitHub Actions (Backup)

**Configuración**: `.github/workflows/keep-alive.yml`

```yaml
on:
  schedule:
    - cron: '*/10 * * * *'  # Cada 10 minutos
```

**Ventajas:**
- ✅ Backup si cron de Render falla
- ✅ Gratuito (GitHub Actions)
- ✅ Funciona desde cualquier repo público

**Limitaciones:**
- ⚠️ GitHub Actions puede tener delays de 3-10 minutos
- ⚠️ Se desactiva automáticamente si no hay commits en 60 días

### 3. Servicios Externos de Monitoring (Opcional)

#### A. UptimeRobot (Recomendado)
**URL**: https://uptimerobot.com

**Setup:**
1. Crear cuenta gratis
2. Añadir monitor HTTP(S)
   - URL: `https://news-generator-backend.onrender.com/api/health`
   - Interval: 5 minutos (free tier)
3. Configurar alertas por email

**Ventajas:**
- ✅ Interfaz web para ver uptime
- ✅ Alertas cuando el servicio cae
- ✅ Gratis hasta 50 monitores
- ✅ Más confiable que GitHub Actions

#### B. Pingdom (Alternativa)
**URL**: https://www.pingdom.com

**Setup:** Similar a UptimeRobot
**Limitación:** Solo 1 monitor en free tier

#### C. StatusCake (Alternativa)
**URL**: https://www.statuscake.com

**Setup:** Similar a UptimeRobot
**Free tier:** Unlimited monitors, checks cada 5 min

### 4. Cron Job Manual (Servidor Propio)

Si tienes un servidor/VPS propio:

```bash
# Editar crontab
crontab -e

# Añadir:
*/10 * * * * curl -s https://news-generator-backend.onrender.com/api/keep-alive > /dev/null 2>&1
```

## 📊 Comparativa de Soluciones

| Solución | Confiabilidad | Costo | Setup | Alertas |
|----------|---------------|-------|-------|---------|
| **Render Cron** | ⭐⭐⭐⭐⭐ | Gratis | Fácil | ❌ |
| **GitHub Actions** | ⭐⭐⭐ | Gratis | Fácil | ❌ |
| **UptimeRobot** | ⭐⭐⭐⭐⭐ | Gratis | Muy fácil | ✅ |
| **Cron Manual** | ⭐⭐⭐⭐ | Gratis* | Media | ❌ |

*Requiere servidor propio

## 🚀 Configuración Recomendada

### Setup Básico (Solo Render)
```
1. Deploy a Render con render.yaml
2. Cron job se crea automáticamente
✅ Listo
```

### Setup Óptimo (Render + UptimeRobot)
```
1. Deploy a Render con render.yaml
2. Crear cuenta en UptimeRobot
3. Añadir monitor cada 5 minutos
4. Configurar alertas por email
✅ Máxima confiabilidad + Monitoreo
```

### Setup Paranoid (Triple Redundancia)
```
1. Render Cron Job (principal)
2. GitHub Actions (backup)
3. UptimeRobot (backup + alertas)
✅ Si uno falla, los otros continúan
```

## 🔧 Endpoints Implementados

### `/api/health`
**Propósito**: Health check general
**Respuesta**:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-01-11T19:00:00Z",
  "uptime": "active"
}
```

### `/api/keep-alive`
**Propósito**: Keep-alive específico (ligero, sin lógica)
**Respuesta**:
```json
{
  "status": "alive",
  "message": "Service is active",
  "timestamp": "2024-01-11T19:00:00Z"
}
```

## 📝 Logs del Cron Job

### Ver logs en Render Dashboard
```
1. Dashboard → Services → news-generator-keep-alive
2. Logs (live tail)
3. Ver output cada 10 minutos
```

### Output esperado:
```
======================================================================
🔄 Keep-Alive Cron Job - 2024-01-11 19:00:00
🎯 Target: https://news-generator-backend.onrender.com
======================================================================
✅ [2024-01-11 19:00:01] Ping exitoso a .../api/health
   Respuesta: {'status': 'healthy', 'version': '2.0.0', ...}
✅ [2024-01-11 19:00:02] Ping exitoso a .../api/keep-alive
   Respuesta: {'status': 'alive', 'message': 'Service is active', ...}
======================================================================
📊 Resultados: 2/2 pings exitosos
======================================================================
```

## 🧪 Testing

### Probar cron job localmente
```bash
cd /home/sebastianvernis/news-prototype/Tecnología
export BACKEND_URL=https://news-generator-backend.onrender.com
python3 scripts/keep_alive_cron.py
```

### Probar GitHub Action manualmente
```
1. Ve a tu repo en GitHub
2. Actions → Keep Backend Alive
3. Run workflow → Run workflow
4. Ver logs de ejecución
```

### Simular suspensión
```bash
# 1. No hacer requests al backend por 15 minutos
# 2. Hacer request y medir tiempo de respuesta
time curl https://news-generator-backend.onrender.com/api/health

# Si está dormido: ~30-60s
# Si está activo: <500ms
```

## ⚠️ Troubleshooting

### Cron job no ejecuta

**Problema**: No aparece en logs
```bash
# Verificar en Render dashboard:
# 1. Services → news-generator-keep-alive existe?
# 2. Si no, re-deploy desde render.yaml
```

**Problema**: Falla con "Module not found"
```bash
# Verificar buildCommand en render.yaml:
buildCommand: "pip install requests"
```

### Backend sigue durmiendo

**Problema**: Cron hace ping pero backend duerme igual
```bash
# Posible causa: Free tier cambió políticas
# Solución: Upgrade a Starter ($7/mes) sin auto-sleep
```

### GitHub Action no ejecuta

**Problema**: Workflow deshabilitado
```bash
# GitHub deshabilita workflows si repo inactivo 60 días
# Solución: 
# 1. Actions → Enable workflow
# 2. Hacer commit dummy cada mes
```

## 💡 Tips Adicionales

### Reducir Cold Start Time
```python
# En backend/app.py
# Minimizar imports pesados en startup
# Lazy load librerías no críticas
```

### Optimizar Cron Interval
```yaml
# Muy frecuente (cada 5 min) - más consumo de recursos
schedule: "*/5 * * * *"

# Balance óptimo (cada 10 min) - recomendado
schedule: "*/10 * * * *"

# Económico (cada 14 min) - justo antes del límite
schedule: "*/14 * * * *"
```

### Combinar con CDN
```
Frontend en Vercel + Backend en Render:
- Frontend siempre activo (estático)
- Backend despierta solo cuando frontend necesita API
- Usuarios no notan cold start (esperan respuesta de API)
```

## 📈 Mejores Prácticas

1. **Usar múltiples capas**: Cron + UptimeRobot
2. **Monitorear alertas**: Configurar email cuando cae
3. **Logs centralizados**: Revisar logs de cron semanalmente
4. **Plan de upgrade**: Estar listo para Starter plan si free tier falla
5. **Documentar**: Mantener este doc actualizado con cambios

## 🎓 Cuándo Upgradear

### Mantener Free Tier si:
- ✅ Tráfico bajo (<100 requests/día)
- ✅ No es crítico (prototipo/demo)
- ✅ Cold start tolerable (~30s)
- ✅ Presupuesto $0

### Upgradear a Starter ($7/mes) si:
- ❌ Cold start afecta UX
- ❌ Tráfico medio-alto (>500 requests/día)
- ❌ Aplicación en producción
- ❌ Necesitas 0 downtime

## 🔗 Referencias

- **Render Cron Jobs**: https://render.com/docs/cronjobs
- **Render Free Tier**: https://render.com/docs/free
- **UptimeRobot**: https://uptimerobot.com
- **GitHub Actions Cron**: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule

---

## ✅ Checklist de Implementación

- [x] Endpoint `/api/health` creado
- [x] Endpoint `/api/keep-alive` creado
- [x] Script `keep_alive_cron.py` implementado
- [x] `render.yaml` configurado con cron job
- [x] GitHub Action creado (backup)
- [ ] Deploy a Render
- [ ] Verificar cron job ejecuta cada 10 min
- [ ] (Opcional) Configurar UptimeRobot
- [ ] (Opcional) Configurar alertas email
- [ ] Monitorear por 24-48h para confirmar

---

**¡Backend siempre activo sin costos adicionales! 🎉**
