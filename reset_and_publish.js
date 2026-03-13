#!/usr/bin/env node
/**
 * Script para resetear timers de Facebook y forzar publicación en TODOS los sitios
 * 
 * Esto resetea los timers de KV para que el cron publique inmediatamente
 * 
 * Uso: node reset_and_publish.js
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

async function resetAndPublish() {
  console.log('=== RESET DE TIMERS + PUBLICACIÓN FORZADA ===\n');
  console.log('Paso 1: Verificando artículos pendientes por sitio...\n');
  
  // Primero verificar qué sitios tienen artículos pendientes
  const sitesWithArticles = [];
  
  for (const site of SITES) {
    try {
      const res = await fetch(`${API_URL}/facebook/monitor`);
      const monitor = await res.json();
      const pendingForSite = monitor.filter(a => a.SITIO === site);
      
      if (pendingForSite.length > 0) {
        console.log(`✓ ${site}: ${pendingForSite.length} artículos pendientes`);
        sitesWithArticles.push(site);
      } else {
        console.log(`- ${site}: Sin artículos pendientes`);
      }
    } catch (e) {
      console.log(`✗ ${site}: Error - ${e.message}`);
    }
  }
  
  console.log(`\n${sitesWithArticles.length} sitios con artículos pendientes.\n`);
  console.log('Paso 2: Forzando publicación en todos los sitios con artículos...\n');
  
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
    
    // Delay para evitar rate limiting (3 segundos entre cada sitio)
    await new Promise(r => setTimeout(r, 3000));
  }
  
  console.log('\n=== RESULTADO FINAL ===');
  console.log(`✅ Publicados: ${success}`);
  console.log(`⚠️  Sin artículos: ${noArticles}`);
  console.log(`❌ Fallidos: ${failed}`);
  console.log(`📊 Total: ${SITES.length}`);
  
  console.log('\n=== PRÓXIMOS PASOS ===');
  console.log('1. El cron automático publicará cada 3 horas');
  console.log('2. Para verificar estado: curl https://news-api.sebastianvernis.workers.dev/api/cron/status');
  console.log('3. Para ver posts recientes: curl https://news-api.sebastianvernis.workers.dev/api/facebook/recent-posts/[SITE]');
}

resetAndPublish().catch(console.error);
