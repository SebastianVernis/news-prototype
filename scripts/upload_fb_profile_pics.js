#!/usr/bin/env node
/**
 * Script para subir logos como foto de perfil en Facebook
 * Solo para los 17 SITIOS NUEVOS
 * 
 * Uso: node upload_fb_profile_pics.js
 * 
 * Requisitos:
 * - Tener los tokens de Facebook configurados en Cloudflare Secrets
 * - Wrangler autenticado
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Lista de los 17 SITIOS NUEVOS (no los 10 estables)
const NEW_SITES = [
  'boominformativo',
  'capitalpress',
  'diarioexpress',
  'elpulsomexicano',
  'enfoquecapital',
  'enfoquedirecto',
  'formulacdmx',
  'mexicantimes',
  'mexico360noticias',
  'mradio',
  'noticiashorizonte',
  'pulsodiario',
  'puntoclave',
  'puntonoticias',
  'radarinformativo',
  'reportediario',
  'televisionabc'
];

// Mapeo de slugs a Facebook Page IDs (debes verificar estos IDs)
const SITE_FB_IDS = {
  'boominformativo': '61568203340617',
  'capitalpress': 'PENDIENTE',
  'diarioexpress': 'PENDIENTE',
  'elpulsomexicano': 'PENDIENTE',
  'enfoquecapital': 'PENDIENTE',
  'enfoquedirecto': 'PENDIENTE',
  'formulacdmx': 'PENDIENTE',
  'mexicantimes': 'PENDIENTE',
  'mexico360noticias': 'PENDIENTE',
  'mradio': 'PENDIENTE',
  'noticiashorizonte': 'PENDIENTE',
  'pulsodiario': 'PENDIENTE',
  'puntoclave': 'PENDIENTE',
  'puntonoticias': 'PENDIENTE',
  'radarinformativo': 'PENDIENTE',
  'reportediario': 'PENDIENTE',
  'televisionabc': 'PENDIENTE'
};

// URL base donde están alojados los logos
const LOGO_BASE_URL = 'https://www';

console.log('📋 Script para subir fotos de perfil a Facebook');
console.log('   Solo para los 17 SITIOS NUEVOS\n');

// Función para obtener token de Facebook desde wrangler
function getFBToken(siteSlug) {
  try {
    // El secret en Cloudflare se llama FB_TOKEN_[SLUG_UPPERCASE]
    const secretName = `FB_TOKEN_${siteSlug.toUpperCase()}`;
    // Nota: No podemos obtener el valor del secret directamente por seguridad
    // El usuario deberá tener los tokens configurados
    return null;
  } catch (error) {
    return null;
  }
}

// Función para subir foto de perfil a Facebook
async function uploadProfilePicture(pageId, imageUrl, accessToken) {
  try {
    // Método 1: Usar URL directa (Facebook la descarga)
    const url = `https://graph.facebook.com/v19.0/${pageId}/picture`;
    const formData = new URLSearchParams();
    formData.append('url', imageUrl);
    formData.append('access_token', accessToken);
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    
    if (response.ok) {
      return { success: true, data: result };
    } else {
      return { success: false, error: result };
    }
  } catch (error) {
    return { success: false, error: { message: error.message } };
  }
}

// Función alternativa: subir foto de perfil usando endpoint /photos
async function uploadProfilePictureAlt(pageId, imageUrl, accessToken) {
  try {
    // Primero subir la foto
    const uploadUrl = `https://graph.facebook.com/v19.0/${pageId}/photos`;
    const formData = new URLSearchParams();
    formData.append('url', imageUrl);
    formData.append('published', 'false'); // No publicar en timeline
    formData.append('access_token', accessToken);
    
    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    
    if (response.ok && result.id) {
      // Luego establecer como foto de perfil
      const profileUrl = `https://graph.facebook.com/v19.0/${pageId}`;
      const profileData = new URLSearchParams();
      profileData.append('profile_pic', result.id);
      profileData.append('access_token', accessToken);
      
      const profileResponse = await fetch(profileUrl, {
        method: 'POST',
        body: profileData
      });
      
      const profileResult = await profileResponse.json();
      
      if (profileResponse.ok) {
        return { success: true, data: profileResult };
      } else {
        return { success: false, error: profileResult };
      }
    } else {
      return { success: false, error: result };
    }
  } catch (error) {
    return { success: false, error: { message: error.message } };
  }
}

// Verificar si wrangler está autenticado
function checkWranglerAuth() {
  try {
    execSync('wrangler whoami', { stdio: 'pipe' });
    return true;
  } catch (error) {
    return false;
  }
}

// Obtener lista de secrets desde wrangler
function getSecrets() {
  try {
    const output = execSync('wrangler secret list --name news-api', { 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    return output;
  } catch (error) {
    return '';
  }
}

// Main
async function main() {
  console.log('🔍 Verificando autenticación...');
  if (!checkWranglerAuth()) {
    console.error('❌ Wrangler no está autenticado. Ejecuta: wrangler login');
    process.exit(1);
  }
  console.log('✅ Wrangler autenticado\n');
  
  console.log('📊 Obteniendo secrets de Cloudflare...');
  const secrets = getSecrets();
  
  console.log('\n📋 Sitios nuevos a procesar:\n');
  
  let success = 0;
  let failed = 0;
  let skipped = 0;
  
  for (const site of NEW_SITES) {
    const logoUrl = `${LOGO_BASE_URL}.${site === 'boominformativo' ? 'top' : 
                     site === 'capitalpress' ? 'lat' :
                     site === 'diarioexpress' ? 'click' :
                     site === 'elpulsomexicano' ? 'lat' :
                     site === 'enfoquecapital' ? 'top' :
                     site === 'enfoquedirecto' ? 'lat' :
                     site === 'formulacdmx' ? 'top' :
                     site === 'mexicantimes' ? 'top' :
                     site === 'mexico360noticias' ? 'click' :
                     site === 'mradio' ? 'lat' :
                     site === 'noticiashorizonte' ? 'click' :
                     site === 'pulsodiario' ? 'lat' :
                     site === 'puntoclave' ? 'lat' :
                     site === 'puntonoticias' ? 'website' :
                     site === 'radarinformativo' ? 'online' :
                     site === 'reportediario' ? 'online' :
                     site === 'televisionabc' ? 'lat' : 'pages.dev'}/logo.png`;
    
    const pageId = SITE_FB_IDS[site];
    const secretName = `FB_TOKEN_${site.toUpperCase()}`;
    
    // Verificar si el secret existe
    const hasToken = secrets.includes(secretName);
    
    if (!hasToken || pageId === 'PENDIENTE') {
      console.log(`⏭️  ${site}: Skip (falta token o Page ID)`);
      skipped++;
      continue;
    }
    
    console.log(`📤 ${site}: Subiendo logo...`);
    console.log(`   Logo URL: ${logoUrl}`);
    console.log(`   Page ID: ${pageId}`);
    
    // Nota: No podemos obtener el token directamente por seguridad
    // Este script requiere que el usuario proporcione los tokens manualmente
    // o use la API de Cloudflare para obtenerlos
    
    console.log(`   ⚠️  Requiere implementación manual con token`);
    skipped++;
  }
  
  console.log('\n─────────────────────────────────────────');
  console.log(`✅ Exitosos: ${success}`);
  console.log(`❌ Fallidos: ${failed}`);
  console.log(`⏭️  Saltados: ${skipped}`);
  console.log('─────────────────────────────────────────');
  
  console.log('\n⚠️  NOTA: Este script requiere los tokens de Facebook.');
  console.log('   Los tokens están guardados como secrets en Cloudflare.');
  console.log('\n📌 Opción recomendada:');
  console.log('   1. Ir a Facebook Graph API Explorer: https://developers.facebook.com/tools/explorer/');
  console.log('   2. Generar token para cada página con permiso: manage_pages, publish_pages');
  console.log('   3. Usar curl para subir la foto de perfil:');
  console.log('');
  console.log('   curl -X POST "https://graph.facebook.com/v19.0/{PAGE_ID}/picture" \\');
  console.log('     -d "url={LOGO_URL}" \\');
  console.log('     -d "access_token={ACCESS_TOKEN}"');
  console.log('');
}

main().catch(console.error);
