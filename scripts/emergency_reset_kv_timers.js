#!/usr/bin/env node
// Script de EMERGENCIA para resetear TODOS los timers de Facebook en KV
// Ejecutar: node scripts/emergency_reset_kv_timers.js

const SITES = [
  // Sitios Estables (10)
  "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias",
  "mexicoinformado", "nodoinformativo", "bitacoraurbana",
  "reportecentralmx", "verticenoticias", "noticiasobjetivo",
  // Nuevos Sitios (17)
  "boominformativo", "capitalpress", "diarioexpress", "elpulsomexicano",
  "enfoquecapital", "enfoquedirecto", "formulacdmx", "mexicantimes",
  "mexico360noticias", "mradio", "noticiashorizonte", "pulsodiario",
  "puntoclave", "puntonoticias", "radarinformativo", "reportediario",
  "televisionabc"
];

async function resetTimers() {
  console.log('=== EMERGENCY KV TIMER RESET ===\n');
  
  // Nota: Este script requiere wrangler CLI
  console.log('Para resetear los timers manualmente, ejecuta:\n');
  
  for (const site of SITES) {
    console.log(`wrangler kv:key delete --binding ARTICLES_KV --key "last_fb_post_${site}" --name news-api`);
  }
  
  console.log('\nO para establecer todos a "0" (forzar publicación inmediata):');
  for (const site of SITES) {
    console.log(`echo "0" | wrangler kv:key put --binding ARTICLES_KV --key "last_fb_post_${site}" --value-file - --name news-api`);
  }
}

resetTimers();
