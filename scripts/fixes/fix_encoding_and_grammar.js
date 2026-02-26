const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const WRANGLER_CONFIG = path.join(__dirname, '../../src/wrangler.toml');
const ENCODING_MAP = {'Ã¡':'á','Ã©':'é','Ã­':'í','Ã³':'ó','Ãº':'ú','Ã':'Á','Ã‰':'É','Ã':'Í','Ã“':'Ó','Ãš':'Ú','Ã±':'ñ','Ã‘':'Ñ','Â¡':'¡','Â¿':'¿','â€œ':'"','â€?':'"','â€':'"','â€˜':"'",'â€™':"'",'â€“':'–','â€”':'—','â€¦':'...','Â':''};
function fixEncoding(text) {
  if (!text) return "";
  let fixed = text;
  for (const [bad, good] of Object.entries(ENCODING_MAP)) { fixed = fixed.split(bad).join(good); }
  fixed = fixed.replace(/MÃ©xico/g, 'México');
  fixed = fixed.replace(/\s+([,.!?;:])/g, '$1');
  fixed = fixed.replace(/([,.!?;:])([a-zA-ZáéíóúÁÉÍÓÚ])/g, '$1 $2');
  fixed = fixed.replace(/\.\.+/g, '...');
  fixed = fixed.replace(/\s\s+/g, ' ');
  return fixed.trim();
}
async function run() {
  const target = process.argv.includes('--remote') ? '--remote' : '--local';
  console.log(`🔧 Reparando ${target}...`);
  try {
    const output = execSync(`npx wrangler d1 execute news_db ${target} --command="SELECT ID, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO FROM ARTICULOS_PARAFRASEADOS" --config=${WRANGLER_CONFIG} --json`, { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 });
    const data = JSON.parse(output);
    const articles = data[0]?.results || data.results || data;
    console.log(`📊 Artículos: ${articles.length}`);
    let updates = [];
    for (const art of articles) {
      const nT = fixEncoding(art.TITULO_PARAFRASEADO);
      const nD = fixEncoding(art.DESCRIPCION_PARAFRASEADA);
      const nC = fixEncoding(art.CONTENIDO);
      if (nT !== art.TITULO_PARAFRASEADO || nD !== art.DESCRIPCION_PARAFRASEADA || nC !== art.CONTENIDO) {
        updates.push(`UPDATE ARTICULOS_PARAFRASEADOS SET TITULO_PARAFRASEADO='${nT.replace(/'/g,"''")}', DESCRIPCION_PARAFRASEADA='${nD.replace(/'/g,"''")}', CONTENIDO='${nC.replace(/'/g,"''")}' WHERE ID='${art.ID}';`);
      }
    }
    if (updates.length === 0) return console.log('✨ Limpio.');
    console.log(`📝 Reparando ${updates.length}...`);
    for (let i = 0; i < updates.length; i += 10) {
      const chunk = updates.slice(i, i + 10);
      const f = `f_${Date.now()}.sql`;
      fs.writeFileSync(f, chunk.join('\n'));
      execSync(`npx wrangler d1 execute news_db ${target} --file=${f} --config=${WRANGLER_CONFIG} --yes`);
      fs.unlinkSync(f);
      console.log(` ✅ Bloque ${Math.floor(i/10)+1}`);
    }
    console.log('🎉 ¡Listo!');
  } catch (err) { console.error('❌ Error:', err.message); }
}
run();
