/**
 * Script para limpiar nombres de autores y marcas de medios
 * antes de publicar artículos parafraseados
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../src/wrangler.toml');
const JSON_FILE = path.join(__dirname, '../noticias_parafraseadas_20260225_205015.json');

// Lista de medios a eliminar
const MEDIA_BRANDS = [
  'El Financiero',
  'El Financiero.com.mx',
  'BBC News',
  'BBC',
  'La Nacion',
  'LA NACION',
  'lanacion.com.ar',
  'RT en Español',
  'RT',
  'Russia Today',
  'actualidad.rt.com',
  'Expansion.com',
  'Expansión',
  'expansion.mx',
  'El Mundo',
  'elmundo.es',
  'Xataka.com',
  'Xataka',
  'Huffingtonpost.es',
  'Huffington Post',
  'Latercera.com',
  'La Tercera',
  'ABC.es',
  'ABC',
  'abc.es',
  'Tribuna.com.mx',
  'Tribuna',
  'Jornada.com.mx',
  'La Jornada',
  'Jornada',
  'El Periodico',
  'elperiodico.com',
  'Boston Herald',
  'bostonherald.com',
  'Republica.com',
  'República',
  'Associated Press',
  'AP',
  'Associated Press Spanish',
  'Reuters',
  'EFE',
  'DPA',
  'Bloomberg',
  'CNN',
  'Televisa',
  'TV Azteca'
];

// Patrones para eliminar autores
const AUTHOR_PATTERNS = [
  /Por\s+[A-Z][a-z]+\s+[A-Z][a-z]+/gi,
  /De\s+[A-Z][a-z]+\s+[A-Z][a-z]+/gi,
  /[A-Z][a-z]+\s+[A-Z][a-z]+\s*[@|]\s*\w+/gi,
  /Redacción\s+\w*/gi,
  /Agencias/gi,
  /Notimex/gi,
  /EFE/gi,
  /Reuters/gi,
  /Bloomberg/gi,
  /AP/gi,
  /Associated Press/gi,
  /DPA/gi,
  /SinEmbargo/gi,
  /Animal Político/gi,
  /Aristegui Noticias/gi,
  /AnimalPolitico/gi,
];

function cleanText(text) {
  if (!text) return '';
  
  let cleaned = text;
  
  // 1. Eliminar marcas de medios
  MEDIA_BRANDS.forEach(brand => {
    const regex = new RegExp(brand.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    cleaned = cleaned.replace(regex, '');
  });
  
  // 2. Eliminar patrones de autores
  AUTHOR_PATTERNS.forEach(pattern => {
    cleaned = cleaned.replace(pattern, '');
  });
  
  // 3. Eliminar referencias a sitios web
  cleaned = cleaned.replace(/https?:\/\/[^\s]+/gi, '');
  
  // 4. Eliminar referencias como "según", "de acuerdo con" + medio
  cleaned = cleaned.replace(/según\s+(el|la|los|las)?\s*\w+\s*(de\s+)?(México|España|Argentina|Colombia|Chile)?/gi, '');
  cleaned = cleaned.replace(/de acuerdo con\s+(el|la|los|las)?\s*\w+/gi, '');
  cleaned = cleaned.replace(/informa\s+(el|la|los|las)?\s*\w+/gi, '');
  cleaned = cleaned.replace(/reporta\s+(el|la|los|las)?\s*\w+/gi, '');
  
  // 5. Limpieza de espacios múltiples
  cleaned = cleaned.replace(/\s+/g, ' ');
  cleaned = cleaned.replace(/\s+([,.!?;:])/g, '$1');
  cleaned = cleaned.replace(/([,.!?;:])([a-zA-ZáéíóúÁÉÍÓÚñÑ])/g, '$1 $2');
  
  // 6. Eliminar líneas vacías
  cleaned = cleaned.replace(/^\s*[\r\n]/gm, '');
  
  return cleaned.trim();
}

function cleanArticlesInJSON() {
  console.log('🧹 Limpiando artículos en el JSON...\n');
  
  if (!fs.existsSync(JSON_FILE)) {
    console.error(`❌ Archivo no encontrado: ${JSON_FILE}`);
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(JSON_FILE, 'utf-8'));
  console.log(`📊 Total artículos en JSON: ${data.length}`);
  
  let modifiedCount = 0;
  
  data.forEach((article, index) => {
    const originalTitle = article.title;
    const originalDesc = article.description;
    const originalContent = article.full_text;
    
    // Limpiar título
    article.title = cleanText(article.title);
    
    // Limpiar descripción
    article.description = cleanText(article.description);
    
    // Limpiar contenido completo
    article.full_text = cleanText(article.full_text);
    
    // Verificar si hubo cambios
    if (originalTitle !== article.title || 
        originalDesc !== article.description || 
        originalContent !== article.full_text) {
      modifiedCount++;
      console.log(`✅ Artículo ${index + 1}: "${originalTitle.substring(0, 50)}..." - Limpiado`);
    }
  });
  
  // Guardar JSON limpio
  const cleanFile = JSON_FILE.replace('.json', '_CLEANED.json');
  fs.writeFileSync(cleanFile, JSON.stringify(data, null, 2), 'utf-8');
  
  console.log(`\n📝 Artículos modificados: ${modifiedCount}`);
  console.log(`💾 JSON limpio guardado en: ${cleanFile}`);
  
  return cleanFile;
}

async function publishCleanedArticles(jsonFile) {
  console.log('\n🚀 Publicando artículos limpios...\n');
  
  const data = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
  
  const REQUIRED_FIELDS = ['title', 'description', 'full_text', 'image_url', 'published_at', 'url', 'author'];
  
  function isValidArticle(article) {
    for (const field of REQUIRED_FIELDS) {
      if (!article[field] || article[field].trim() === '') return false;
    }
    if (article.full_text.length < 200) return false;
    if (article.title.length < 20) return false;
    if (!article.image_url.startsWith('http')) return false;
    return true;
  }
  
  function extractSitesFromCategory(category) {
    const siteMap = {
      'POLITICA': 'noticiasobjetivo,mexicoinformado,nodoinformativo',
      'NACIONAL': 'mexicoinformado,cbnnoticias,centralmexico',
      'INTERNACIONAL': 'noticiasobjetivo,verticenoticias',
      'ECONOMIA': 'mexicoinformado,reportecentralmx',
      'DEPORTES': 'cbnnoticias,tvmexico',
      'TECNOLOGIA': 'bitacoraurbana,nodoinformativo',
      'ENTRETENIMIENTO': 'radiocinconoticias,tvmexico',
      'SALUD': 'mexicoinformado,cbnnoticias',
      'CIENCIA': 'bitacoraurbana,nodoinformativo',
      'CULTURA': 'radiocinconoticias,centralmexico'
    };
    return siteMap[category] || 'noticiasobjetivo,mexicoinformado';
  }
  
  function generateSlug(title) {
    return title
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 100);
  }
  
  const completeArticles = data.filter(isValidArticle);
  console.log(`✅ Artículos válidos para publicar: ${completeArticles.length}\n`);
  
  let published = 0;
  let failed = 0;
  
  for (const article of completeArticles) {
    const category = article.category || 'NACIONAL';
    const sites = extractSitesFromCategory(category);
    const slug = generateSlug(article.title);
    const now = new Date().toISOString();
    
    console.log(`📰 Publicando: "${article.title.substring(0, 60)}..."`);
    
    const insertSql = `
      INSERT INTO ARTICULOS_PARAFRASEADOS (
        ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, SLUG, 
        DESCRIPCION_PARAFRASEADA, CONTENIDO, CATEGORIA, AUTOR, 
        FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO, DESTACADO, 
        VISTAS, ESTADO, FB_REQUERIDO, ES_BREVE
      ) VALUES (
        '${article.url.replace(/'/g, "''")}', 
        '${article.url.replace(/'/g, "''")}',
        '${article.title.replace(/'/g, "''")}',
        '${slug}',
        '${article.description.replace(/'/g, "''")}',
        '${article.full_text.replace(/'/g, "''")}',
        '${category}',
        'Redacción',
        '${now}',
        '${article.image_url}',
        '${sites}',
        0, 0, 'PUBLICADO', 0, 0
      )
      ON CONFLICT(ID) DO NOTHING;
    `;
    
    try {
      const tempFile = `pub_clean_${Date.now()}.sql`;
      fs.writeFileSync(tempFile, insertSql);
      execSync(
        `npx wrangler d1 execute news_db --remote --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
        { encoding: 'utf-8', stdio: 'pipe' }
      );
      fs.unlinkSync(tempFile);
      console.log(`   ✅ Publicado\n`);
      published++;
    } catch (err) {
      if (err.message.includes('UNIQUE constraint failed')) {
        console.log(`   ⏭️  Ya existe\n`);
      } else {
        console.log(`   ❌ Error: ${err.message}\n`);
      }
      failed++;
    }
    
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('✨ PUBLICACIÓN COMPLETADA');
  console.log('='.repeat(60));
  console.log(`📰 Artículos publicados: ${published}`);
  console.log(`⏭️  Artículos ya existentes: ${failed}`);
  console.log('='.repeat(60));
}

async function run() {
  console.log('🧹 LIMPIEZA Y PUBLICACIÓN DE ARTÍCULOS\n');
  console.log('Eliminando nombres de autores y marcas de medios...\n');
  
  const cleanFile = cleanArticlesInJSON();
  
  console.log('\n' + '='.repeat(60));
  console.log('¿Proceder con la publicación de artículos limpios?');
  console.log('='.repeat(60));
  
  await publishCleanedArticles(cleanFile);
}

run().catch(err => {
  console.error('❌ Error fatal:', err.message);
  process.exit(1);
});
