/**
 * Script para publicar artículos parafraseados completos
 * Extrae del JSON los artículos que tienen todos los campos requeridos
 * y los publica en los sitios correspondientes
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WRANGLER_CONFIG = path.join(__dirname, '../src/wrangler.toml');
const JSON_FILE = path.join(__dirname, '../noticias_parafraseadas_20260225_205015.json');

// Campos requeridos para considerar un artículo como "completo"
const REQUIRED_FIELDS = [
  'title',
  'description', 
  'full_text',
  'image_url',
  'published_at',
  'url',
  'author'
];

function isValidArticle(article) {
  // Verificar campos requeridos
  for (const field of REQUIRED_FIELDS) {
    if (!article[field] || article[field].trim() === '') {
      return false;
    }
  }
  
  // Verificar que la imagen sea URL válida (no placeholder)
  if (article.image_url.includes('placeholder') || 
      article.image_url.includes('/logo.png') ||
      !article.image_url.startsWith('http')) {
    return false;
  }
  
  // Verificar que el contenido tenga longitud mínima (200 caracteres)
  if (article.full_text.length < 200) {
    return false;
  }
  
  // Verificar que el título tenga longitud mínima (20 caracteres)
  if (article.title.length < 20) {
    return false;
  }
  
  return true;
}

function extractSitesFromCategory(category) {
  // Mapeo de categorías a sitios por defecto
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

async function publishArticle(article) {
  const category = article.category || 'NACIONAL';
  const sites = extractSitesFromCategory(category);
  const slug = generateSlug(article.title);
  const now = new Date().toISOString();
  
  console.log(`\n📰 Publicando: "${article.title.substring(0, 60)}..."`);
  console.log(`   Categoría: ${category}`);
  console.log(`   Sitios: ${sites}`);
  
  // Insertar en ARTICULOS_PARAFRASEADOS
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
      '${(article.author || 'Redacción').replace(/'/g, "''")}',
      '${now}',
      '${article.image_url}',
      '${sites}',
      0, 0, 'PUBLICADO', 0, 0
    );
  `;
  
  try {
    const tempFile = `pub_${Date.now()}.sql`;
    fs.writeFileSync(tempFile, insertSql);
    execSync(
      `npx wrangler d1 execute news_db --remote --file=${tempFile} --config=${WRANGLER_CONFIG} --yes`,
      { encoding: 'utf-8', stdio: 'pipe' }
    );
    fs.unlinkSync(tempFile);
    console.log(`   ✅ Publicado exitosamente`);
    return true;
  } catch (err) {
    console.error(`   ❌ Error: ${err.message}`);
    return false;
  }
}

async function run() {
  console.log('🚀 PUBLICACIÓN DE ARTÍCULOS PARAFRASEADOS\n');
  console.log('📁 Leyendo JSON...');
  
  if (!fs.existsSync(JSON_FILE)) {
    console.error(`❌ Archivo no encontrado: ${JSON_FILE}`);
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(JSON_FILE, 'utf-8'));
  console.log(`📊 Total artículos en JSON: ${data.length}`);
  
  // Filtrar artículos completos
  const completeArticles = data.filter(isValidArticle);
  console.log(`✅ Artículos completos: ${completeArticles.length}`);
  console.log(`⏭️  Artículos incompletos: ${data.length - completeArticles.length}`);
  
  if (completeArticles.length === 0) {
    console.log('\n⚠️ No hay artículos completos para publicar');
    process.exit(0);
  }
  
  // Mostrar resumen de artículos a publicar
  console.log('\n📋 ARTÍCULOS A PUBLICAR:');
  completeArticles.forEach((art, i) => {
    console.log(`\n${i + 1}. ${art.title.substring(0, 80)}${art.title.length > 80 ? '...' : ''}`);
    console.log(`   Fuente: ${art.source_name || 'Desconocido'}`);
    console.log(`   Fecha: ${art.published_at}`);
    console.log(`   Imagen: ${art.image_url.startsWith('http') ? '✅' : '❌'}`);
    console.log(`   Contenido: ${art.full_text.length} caracteres`);
  });
  
  // Confirmar publicación
  console.log('\n⚠️ ¿Proceder con la publicación de estos artículos?');
  console.log('   (Los artículos se insertarán en ARTICULOS_PARAFRASEADOS)');
  
  // Publicar artículos
  console.log('\n🔄 Iniciando publicación...\n');
  
  let published = 0;
  let failed = 0;
  
  for (const article of completeArticles) {
    const success = await publishArticle(article);
    if (success) {
      published++;
    } else {
      failed++;
    }
    
    // Pequeña pausa entre publicaciones
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('✨ PUBLICACIÓN COMPLETADA');
  console.log('='.repeat(60));
  console.log(`📰 Artículos publicados: ${published}`);
  console.log(`❌ Fallidos: ${failed}`);
  console.log('='.repeat(60));
}

run().catch(err => {
  console.error('❌ Error fatal:', err.message);
  process.exit(1);
});
