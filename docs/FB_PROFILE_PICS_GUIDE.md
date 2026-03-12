# 📘 Subir Logos como Foto de Perfil en Facebook
## Solo para los 17 SITIOS NUEVOS

---

## 📋 Instrucciones Previas

### 1. Generar Token de Acceso de Facebook

1. Ve a [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Selecciona tu app (o crea una nueva)
3. Click en "Get Token" → "Get User Access Token"
4. Selecciona los permisos:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`
5. Click en "Generate Access Token"
6. Copia el token generado

### 2. Verificar Logos

Los logos deben estar accesibles en:
```
https://www.[DOMINIO]/logo.png
```

Ejemplo: `https://www.boominformativo.top/logo.png`

---

## 🚀 Comandos para Subir Fotos de Perfil

Copia y ejecuta cada comando, reemplazando `TU_TOKEN_AQUI` con el token que generaste.

### 1. Boom Informativo
```bash
curl -X POST "https://graph.facebook.com/v19.0/501728116348917/picture" \
  -d "url=https://www.boominformativo.top/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 2. Capital Press
```bash
curl -X POST "https://graph.facebook.com/v19.0/458242550714232/picture" \
  -d "url=https://www.capitalpress.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 3. Diario Express
```bash
curl -X POST "https://graph.facebook.com/v19.0/270142695517794/picture" \
  -d "url=https://www.diarioexpress.click/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 4. El Pulso Mexicano
```bash
curl -X POST "https://graph.facebook.com/v19.0/253187761218980/picture" \
  -d "url=https://www.elpulsomexicano.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 5. Enfoque Capital
```bash
curl -X POST "https://graph.facebook.com/v19.0/457328060805587/picture" \
  -d "url=https://www.enfoquecapital.top/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 6. Enfoque Directo
```bash
curl -X POST "https://graph.facebook.com/v19.0/454841367704076/picture" \
  -d "url=https://www.enfoquedirecto.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 7. Fórmula CDMX
```bash
curl -X POST "https://graph.facebook.com/v19.0/500033023189155/picture" \
  -d "url=https://www.formulacdmx.top/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 8. Mexican Times
```bash
curl -X POST "https://graph.facebook.com/v19.0/578088192045850/picture" \
  -d "url=https://www.mexicantimes.top/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 9. México 360 Noticias
```bash
curl -X POST "https://graph.facebook.com/v19.0/286495644543503/picture" \
  -d "url=https://www.mexico360noticias.click/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 10. M Radio
```bash
curl -X POST "https://graph.facebook.com/v19.0/472254365974557/picture" \
  -d "url=https://www.mradio.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 11. Noticias Horizonte
```bash
curl -X POST "https://graph.facebook.com/v19.0/403046706229851/picture" \
  -d "url=https://www.noticiashorizonte.click/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 12. Pulso Diario
```bash
curl -X POST "https://graph.facebook.com/v19.0/429372300256610/picture" \
  -d "url=https://www.pulsodiario.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 13. Punto Clave
```bash
curl -X POST "https://graph.facebook.com/v19.0/497685936753403/picture" \
  -d "url=https://www.puntoclave.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 14. Punto Noticias
```bash
curl -X POST "https://graph.facebook.com/v19.0/216140764924862/picture" \
  -d "url=https://www.puntonoticias.website/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 15. Radar Informativo
```bash
curl -X POST "https://graph.facebook.com/v19.0/405301062674763/picture" \
  -d "url=https://www.radarinformativo.online/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 16. Reporte Diario
```bash
curl -X POST "https://graph.facebook.com/v19.0/274537812414282/picture" \
  -d "url=https://www.reportediario.online/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

### 17. Televisión ABC
```bash
curl -X POST "https://graph.facebook.com/v19.0/481562451709320/picture" \
  -d "url=https://www.televisionabc.lat/logo.png" \
  -d "access_token=TU_TOKEN_AQUI"
```

---

## ✅ Script Automático (Opcional)

Si prefieres ejecutar un script automático:

```bash
# Hacer ejecutable
chmod +x scripts/upload_fb_profile_pics_manual.sh

# Editar el script y agregar tu token
nano scripts/upload_fb_profile_pics_manual.sh

# Ejecutar
./scripts/upload_fb_profile_pics_manual.sh
```

---

## 🔍 Verificación

Después de subir cada logo, verifica en Facebook:

1. Ve a la página de Facebook del sitio
2. Verifica que la foto de perfil se actualizó
3. Si no se ve, espera unos minutos (Facebook puede tardar en procesar)

---

## ❌ Solución de Problemas

### Error: "Unsupported URL"
- El logo no es accesible públicamente
- Verifica que la URL del logo funcione en un navegador

### Error: "Page not found"
- El Page ID es incorrecto
- Verifica el Page ID en Facebook Page Settings

### Error: "Invalid OAuth access token"
- El token expiró o es inválido
- Genera un nuevo token en Graph API Explorer

### Error: "Permissions error"
- El token no tiene los permisos necesarios
- Genera un token con `pages_manage_posts` y `pages_read_engagement`

---

## 📞 Soporte

Si tienes problemas, revisa:
- [Facebook Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [Page Photo Upload](https://developers.facebook.com/docs/graph-api/reference/page/picture)
