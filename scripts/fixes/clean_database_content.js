/**
 * Script de Limpieza y Deduplicación D1
 * - Elimina artículos < 300 palabras.
 * - Deduplica por título (conserva el más reciente).
 * - Repara imágenes (placeholder de Sergio Mayer o NULL -> Logo del sitio).
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');

async function run() {
  const isRemote = process.argv.includes('--remote');
  const target = isRemote ? '--remote' : '--local';
  console.log(`🧹 Limpieza profunda D1 (${target})...`);

  try {
    // 1. Obtener todos los artículos
    const cmd = `npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO_PARAFRASEADO, CONTENIDO, SITIO_DESTINO, URL_IMAGEN FROM ARTICULOS_PARAFRASEADOS ORDER BY FECHA_PUBLICACION DESC" --config=${WRANGLER_CONFIG} --json`;
    const output = execSync(cmd, { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 });
    const data = JSON.parse(output);
    const articles = data[0]?.results || data.results || data;
    
    console.log(`✅ Total artículos en DB: ${articles.length}`);

    let seenTitles = new Set();
    let toDelete = [];
    let toUpdateImages = [];

    for (const art of articles) {
      const content = art.CONTENIDO || '';
      const title = art.TITULO_PARAFRASEADO || '';
      const words = content.trim().split(/\s+/).length;

      // REGLA 1: Borrar si es muy corto
      if (words < 300) {
        toDelete.push(art.ID);
        continue;
      }

      // REGLA 2: Deduplicación por título
      if (seenTitles.has(title)) {
        toDelete.push(art.ID);
        continue;
      }
      seenTitles.add(title);

      // REGLA 3: Reparar imagen (si es null o placeholder de Sergio Mayer detectado por URL)
      // Nota: Si no hay URL, usamos /logo.png del sitio
      const badImageKeywords = ['sergio-mayer', 'placeholder', 'jornada.com.mx/imagemeta'];
      const isBadImage = !art.URL_IMAGEN || badImageKeywords.some(k => art.URL_IMAGEN.includes(k));
      
      if (isBadImage) {
        toUpdateImages.push({ id: art.ID, url: '/logo.png' });
      }
    }

    // Ejecutar borrados
    if (toDelete.length > 0) {
      console.log(`🗑️ Borrando ${toDelete.length} artículos (cortos o duplicados)...`);
      for (let i = 0; i < toDelete.length; i += 50) {
        const chunk = toDelete.slice(i, i + 50);
        const ids = chunk.map(id => `'${id}'`).join(',');
        const sql = `DELETE FROM METRICAS_CONTENIDO WHERE ID_ARTICULO_PARAFRASEADO IN (${ids}); DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID IN (${ids});`;
        const tempFile = `del_${Date.now()}.sql`;
        fs.writeFileSync(tempFile, sql);
        execSync(`npx wrangler d1 execute news_db ${target} --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`);
        fs.unlinkSync(tempFile);
      }
    }

    // Ejecutar actualizaciones de imagen
    if (toUpdateImages.length > 0) {
      console.log(`🖼️ Actualizando ${toUpdateImages.length} imágenes por logo oficial...`);
      for (let i = 0; i < toUpdateImages.length; i += 50) {
        const chunk = toUpdateImages.slice(i, i + 50);
        const sql = chunk.map(upd => `UPDATE ARTICULOS_PARAFRASEADOS SET URL_IMAGEN = '${upd.url}' WHERE ID = '${upd.id}';`).join('\n');
        const tempFile = `upd_img_${Date.now()}.sql`;
        fs.writeFileSync(tempFile, sql);
        execSync(`npx wrangler d1 execute news_db ${target} --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`);
        fs.unlinkSync(tempFile);
      }
    }

    console.log(`🎉 ¡Deduplicación y reparación de imágenes completada!`);

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

run();
