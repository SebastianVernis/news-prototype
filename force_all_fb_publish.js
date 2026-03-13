#!/usr/bin/env node
/**
 * Script para forzar publicación en Facebook en TODOS los sitios
 * 
 * Uso: node force_all_fb_publish.js
 */

const API_URL = 'https://news-api.sebastianvernis.workers.dev/api';

// Lista completa de los 27 sitios
const SITES = [
  // Sitios Estables (10)
  'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
  'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
  'reportecentralmx', 'verticenoticias', 'noticiasobjetivo',
  // Nuevos Sitios (17)
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc',
];

async function forcePublishAll() {
  console.log('=== FORZAR PUBLICACIÓN FACEBOOK - TODOS LOS SITIOS ===\n');
  console.log(`Total de sitios: ${SITES.length}\n`);
  
  let success = 0;
  let noArticles = 0;
  let failed = 0;
  
  for (const site of SITES) {
    try {
      const res = await fetch(`${API_URL}/facebook/force-publish/${site}`, {
        method: 'POST',
      });
      
      const result = await res.json();
      
      if (result.success) {
        console.log(`✅ ${site}: Publicado artículo ${result.article}`);
        success++;
      } else if (result.error && result.error.includes('No articles')) {
        console.log(`⚠️  ${site}: No hay artículos pendientes`);
        noArticles++;
      } else {
        console.log(`❌ ${site}: ${result.error || JSON.stringify(result)}`);
        failed++;
      }
    } catch (e) {
      console.log(`❌ ${site}: Error - ${e.message}`);
      failed++;
    }
    
    // Delay para evitar rate limiting (2 segundos)
    await new Promise(r => setTimeout(r, 2000));
  }
  
  console.log('\n=== RESULTADO ===');
  console.log(`✅ Exitosos: ${success}`);
  console.log(`⚠️  Sin artículos: ${noArticles}`);
  console.log(`❌ Fallidos: ${failed}`);
  console.log(`📊 Total: ${SITES.length}`);
}

forcePublishAll().catch(console.error);
