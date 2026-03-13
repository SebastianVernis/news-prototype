#!/usr/bin/env node
/**
 * Script para resetear los timers de Facebook y forzar la publicación
 * 
 * Uso: node reset_fb_timers.js
 * 
 * Nota: Este script requiere autenticación en el CMS
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

async function resetTimersViaAPI() {
  console.log('=== Reset de Timers de Facebook ===\n');
  console.log('Nota: Los timers se resetean automáticamente cuando pasan 3 horas.\n');
  console.log('Para forzar la publicación inmediata, usa:\n');
  console.log('  curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/[SITE_SLUG]\n');
  
  // Verificar estado actual
  console.log('Verificando estado actual...\n');
  
  const cronRes = await fetch(`${API_URL}/cron/status`);
  const cron = await cronRes.json();
  
  console.log('Estado del Cron:');
  console.log(`  Última ejecución: ${cron.lastRun}`);
  console.log(`  Facebook: ${cron.tasks?.fb}`);
  console.log(`  Próxima ejecución: ${cron.nextRunInMinutes} minutos\n`);
  
  // Verificar artículos pendientes
  console.log('Verificando artículos pendientes...\n');
  
  const monitorRes = await fetch(`${API_URL}/facebook/monitor`);
  const monitor = await monitorRes.json();
  
  // Contar artículos por sitio
  const counts = {};
  monitor.forEach(art => {
    counts[art.SITIO] = (counts[art.SITIO] || 0) + 1;
  });
  
  console.log('Artículos pendientes por sitio (top 10):');
  Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .forEach(([site, count]) => {
      console.log(`  ${site}: ${count} artículos`);
    });
  
  console.log('\n=== Instrucciones ===\n');
  console.log('1. Los timers de Facebook expiran automáticamente después de 3 horas.');
  console.log('2. Para forzar publicación manual en un sitio:');
  console.log(`   curl -X POST ${API_URL}/facebook/force-publish/radiocinconoticias`);
  console.log('\n3. Para ver el estado de los tokens de Facebook:');
  console.log(`   curl ${API_URL}/facebook/debug-tokens`);
  console.log('\n4. El cron se ejecuta cada 30 minutos automáticamente.\n');
}

resetTimersViaAPI().catch(console.error);
