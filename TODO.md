# TODO - Fix CMS (portada upload + validación de título)

## Contexto
- [x] Revisión inicial de logs del CMS:
  - `POST /api/upload` responde `400`.
  - `POST /api/cms/articles` responde `400` con mensaje: `Título requerido`.
- [x] Revisión de archivos relevantes:
  - `public/admin/js/editor.js` (subida de imagen y guardado universal).
  - `public/admin/js/api.js` (config y consumo de API).
  - `public/admin/views/editor.html` (campos de formulario).

## Plan de implementación aprobado
- [x] Validar y mejorar manejo de errores de upload en `editor.js`:
  - [x] `uploadUniversalImage`: validar `res.ok`, parsear error del backend y mostrar mensaje claro.
  - [x] `uploadContentImage`: validar `res.ok`, parsear error del backend y mostrar mensaje claro.
  - [x] Mantener compatibilidad con URL pública de assets (`uploads.sebastianvernis.space`) para preview.
- [x] Normalizar payload en `saveUniversal`:
  - [x] Aplicar `trim()` a campos string (title, slug, author, excerpt, imageUrl, content).
  - [x] Validar `title` y `content` ya normalizados (evitar falsos “llenos” con solo espacios).
- [x] Endurecer feedback al usuario:
  - [x] Mensajes de validación más específicos previo al POST.
  - [x] Mantener comportamiento actual de selección de sitios.

## Verificación posterior
- [ ] Probar flujo en editor CMS:
  - [ ] Subir imagen de portada.
  - [ ] Guardar borrador con título válido.
  - [ ] Publicar artículo con título y contenido válidos.
- [ ] Confirmar que desaparece error `Título requerido` cuando el campo tiene contenido real.
