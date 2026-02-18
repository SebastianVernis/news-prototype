# ☁️ Guía de Despliegue en Cloudflare Pages

Tus sitios ya están generados y listos para subir. Aquí tienes los comandos para desplegarlos rápidamente usando `wrangler` (la CLI de Cloudflare).

## 1. Prerrequisitos

Necesitas tener una cuenta en Cloudflare y `npm` instalado.

```bash
# Instalar Wrangler globalmente
npm install -g wrangler

# Iniciar sesión (se abrirá el navegador)
wrangler login
```

## 2. Desplegar los Sitios

Ejecuta estos comandos uno por uno para subir cada sitio. Cloudflare te dará una URL pública automática (ej: `site-1.pages.dev`).

### Sitio 1: Política Nacional (Layout 1)
```bash
# Nombre del proyecto: politica-mx-site1
wrangler pages deploy output/sites/site_1 --project-name politica-mx-site1 --branch main
```

### Sitio 2: Economía y Análisis (Layout 2 - Sidebar)
```bash
# Nombre del proyecto: politica-mx-site2
wrangler pages deploy output/sites/site_2 --project-name politica-mx-site2 --branch main
```

### Sitio 3: Internacional y Seguridad (Layout 3)
```bash
# Nombre del proyecto: politica-mx-site3
wrangler pages deploy output/sites/site_3 --project-name politica-mx-site3 --branch main
```

### Sitio 4: Elecciones (Layout 4 - Sidebar Derecha)
```bash
# Nombre del proyecto: politica-mx-site4
wrangler pages deploy output/sites/site_4 --project-name politica-mx-site4 --branch main
```

## 3. Verificar Despliegue

Una vez terminados los comandos, verás algo como esto en la terminal:

```
✨ Success! Uploaded 45 files (3.24 MB)
✨ Deployment complete!
✨ Take a peek over at https://politica-mx-site1.pages.dev
```

¡Esa URL es tu sitio en vivo! 🚀

## 4. (Opcional) Configurar Dominio Personalizado

Si tienes un dominio propio (ej: `mis-noticias.com`), ve al panel de Cloudflare:
1. Entra a **Workers & Pages**.
2. Selecciona tu proyecto (`politica-mx-site1`).
3. Ve a **Custom Domains**.
4. Clic en **Set up a custom domain**.
5. Escribe tu dominio y sigue las instrucciones de DNS.

---

**Nota:** Si haces cambios en los sitios localmente, solo vuelve a ejecutar el comando `wrangler pages deploy ...` para actualizar la versión en la nube.
