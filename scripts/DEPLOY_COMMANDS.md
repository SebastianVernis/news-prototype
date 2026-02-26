# 📋 Comandos de Despliegue - Copiar y Pegar

## Despliegue Rápido (Un sitio por uno)

```bash
# 1. Radio Cinco Noticias
wrangler pages deploy ./sites/radiocinconoticias --project-name=radiocinconoticias

# 2. Central México
wrangler pages deploy ./sites/centralmexico --project-name=centralmexico

# 3. TV México
wrangler pages deploy ./sites/tvmexico --project-name=tvmexico

# 4. CBN Noticias
wrangler pages deploy ./sites/cbnnoticias --project-name=cbnnoticias

# 5. México Informado
wrangler pages deploy ./sites/mexicoinformado --project-name=mexicoinformado

# 6. Nodo Informativo
wrangler pages deploy ./sites/nodoinformativo --project-name=nodoinformativo

# 7. Bitácora Urbana
wrangler pages deploy ./sites/bitacoraurbana --project-name=bitacoraurbana

# 8. Reporte Central MX
wrangler pages deploy ./sites/reportecentralmx --project-name=reportecentralmx

# 9. Vértice Noticias
wrangler pages deploy ./sites/verticenoticias --project-name=verticenoticias

# 10. Noticias Objetivo
wrangler pages deploy ./sites/noticiasobjetivo --project-name=noticiasobjetivo
```

---

## URLs de Producción

Después de desplegar, cada sitio estará en:

| Sitio | URL |
|-------|-----|
| Radio Cinco Noticias | https://radiocinconoticias.pages.dev |
| Central México | https://centralmexico.pages.dev |
| TV México | https://tvmexico.pages.dev |
| CBN Noticias | https://cbnnoticias.pages.dev |
| México Informado | https://mexicoinformado.pages.dev |
| Nodo Informativo | https://nodoinformativo.pages.dev |
| Bitácora Urbana | https://bitacoraurbana.pages.dev |
| Reporte Central MX | https://reportecentralmx.pages.dev |
| Vértice Noticias | https://verticenoticias.pages.dev |
| Noticias Objetivo | https://noticiasobjetivo.pages.dev |

---

## Script Automático

```bash
# Ejecutar script interactivo
./deploy.sh

# Seleccionar:
# - Número (1-10) para desplegar un sitio
# - 'all' para desplegar todos
```

---

## Verificación

Después de cada despliegue:

1. ✅ Abrir URL en navegador
2. ✅ Verificar que el logo carga
3. ✅ Verificar que las imágenes cargan
4. ✅ Probar navegación
5. ✅ Probar CMS: `/admin/login.html`

---

## CMS Admin

Cada sitio tiene CMS en:
- URL: `https://[sitio].pages.dev/admin/login.html`
- Token: Ver `sites/CMS_TOKENS.txt`

---

**Total de sitios:** 10  
**Estado:** ✅ Listos para desplegar  
**Fecha:** 2026-02-19
