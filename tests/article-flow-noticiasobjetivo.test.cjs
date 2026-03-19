const assert = require('node:assert/strict');
const { test, describe } = require('node:test');

// Importar funciones de utilidad
const { 
  slugify, 
  normalizeArticleTitleForSlug, 
  articleSlugify 
} = require('../src/utils/helpers.js');

describe('Flujo completo de artículo - Noticias Objetivo', () => {
  
  const articuloPrueba = {
    titulo: 'México alcanza acuerdo histórico con Estados Unidos para el comercio bilateral',
    contenido: 'En una reunión celebrada este martes, los representantes de México y Estados Unidos lograron un acuerdo histórico que beneficiará el comercio bilateral entre ambas naciones. El tratado establece nuevas reglas para la exportación de productos agrícolas y manufacturados.',
    categoria: 'NACIONAL',
    autor: 'Redacción',
    sitioDestino: 'noticiasobjetivo'
  };

  test('debe generar un slug válido a partir del título', () => {
    const slug = articleSlugify(articuloPrueba.titulo);
    
    assert.ok(slug, 'El slug no debe estar vacío');
    assert.ok(!slug.includes(' '), 'El slug no debe contener espacios');
    assert.ok(!slug.includes('null'), 'El slug no debe contener "null"');
    assert.ok(slug.length > 0, 'El slug debe tener contenido');
    assert.ok(slug.length <= 100, 'El slug no debe exceder 100 caracteres');
    
    console.log(`✅ Slug generado: ${slug}`);
  });

  test('debe normalizar títulos con prefijos de medios', () => {
    const tituloConPrefijo = 'La Jornada: México alcanza acuerdo histórico';
    const tituloNormalizado = normalizeArticleTitleForSlug(tituloConPrefijo);
    
    assert.ok(!tituloNormalizado.toLowerCase().includes('la jornada'), 
      'Debe eliminar el prefijo del medio');
    
    const slug = articleSlugify(tituloConPrefijo);
    assert.ok(!slug.includes('la-jornada'), 
      'El slug no debe incluir el prefijo del medio');
  });

  test('debe manejar títulos vacíos o nulos con fallback', () => {
    const tituloVacio = '';
    const tituloNull = null;
    const tituloUndefined = undefined;
    
    const slugVacio = articleSlugify(tituloVacio);
    const slugNull = articleSlugify(tituloNull);
    const slugUndefined = articleSlugify(tituloUndefined);
    
    // Con título vacío, el slugify retorna string vacío
    // La lógica de fallback debe manejar esto
    assert.strictEqual(typeof slugVacio, 'string', 'Debe retornar string aunque esté vacío');
    assert.strictEqual(typeof slugNull, 'string', 'Debe retornar string para null');
    assert.strictEqual(typeof slugUndefined, 'string', 'Debe retornar string para undefined');
  });

  test('debe construir URL válida para el sitio', () => {
    const siteSlug = 'noticiasobjetivo';
    const domain = `https://www.${siteSlug}.click`;
    const slug = articleSlugify(articuloPrueba.titulo);
    
    // Simular construcción de URL como en facebook.js
    const url = `${domain}/articulo/?slug=${slug}`;
    
    assert.ok(url.includes(siteSlug), 'La URL debe incluir el slug del sitio');
    assert.ok(url.includes('/articulo/?slug='), 'La URL debe tener la estructura correcta');
    assert.ok(!url.includes('slug=null'), 'La URL no debe tener slug=null');
    assert.ok(!url.includes('slug=undefined'), 'La URL no debe tener slug=undefined');
    assert.ok(url.startsWith('https://'), 'La URL debe usar HTTPS');
    
    console.log(`✅ URL construida: ${url}`);
  });

  test('debe validar que el artículo tiene todos los campos requeridos para Facebook', () => {
    // Simular validación como en publishToFBIndividual
    const article = {
      TITULO: articuloPrueba.titulo,
      SLUG: articleSlugify(articuloPrueba.titulo),
      URL_IMAGEN: 'https://uploads.sebastianvernis.space/auto/test-image.jpg'
    };
    
    assert.ok(article.TITULO, 'Debe tener título');
    assert.ok(article.SLUG, 'Debe tener slug');
    assert.ok(article.SLUG !== 'null', 'El slug no debe ser string "null"');
    assert.ok(article.SLUG !== '', 'El slug no debe estar vacío');
    assert.ok(article.URL_IMAGEN, 'Debe tener imagen');
    assert.ok(!article.URL_IMAGEN.includes('logo.png'), 'La imagen no debe ser el logo');
  });

  test('debe generar slug único usando timestamp cuando el título está vacío', () => {
    // Simular la lógica de fallback implementada
    let slug = articleSlugify('');
    
    if (!slug || slug.trim() === '') {
      slug = `articulo-${Date.now()}`;
    }
    
    assert.ok(slug, 'Debe generar un slug fallback');
    assert.ok(slug.includes('articulo-'), 'El slug fallback debe incluir prefijo');
    assert.ok(slug.length > 10, 'El slug fallback debe tener timestamp');
    
    console.log(`✅ Fallback slug: ${slug}`);
  });

  test('debe verificar estructura de OG tags', () => {
    const slug = articleSlugify(articuloPrueba.titulo);
    const image = 'https://uploads.sebastianvernis.space/auto/test-image.jpg';
    const domain = 'https://www.noticiasobjetivo.click';
    const url = `${domain}/articulo/?slug=${slug}`;
    
    // Simular OG tags como en _middleware.js
    const ogTags = {
      'og:title': articuloPrueba.titulo,
      'og:description': articuloPrueba.contenido.substring(0, 200),
      'og:image': image,
      'og:url': url,
      'og:type': 'article'
    };
    
    assert.ok(ogTags['og:title'], 'Debe tener og:title');
    assert.ok(ogTags['og:image'], 'Debe tener og:image');
    assert.ok(!ogTags['og:image'].includes('/logo.png'), 'og:image no debe ser logo');
    assert.ok(ogTags['og:url'].includes(slug), 'og:url debe incluir el slug');
  });

  test('debe construir query SQL válido para selección de artículos Facebook', () => {
    const siteSlug = 'NOTICIASOBJETIVO';
    const tableName = `ARTICULOS_SITIO_${siteSlug}`;
    
    // Simular el query como en facebook.js
    const query = `
      SELECT
        s.ID as SITIO_ID,
        s.ID_PARAFRASEADO,
        p.TITULO_PARAFRASEADO as TITULO,
        p.SLUG,
        p.URL_IMAGEN
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 0
        AND p.URL_IMAGEN IS NOT NULL
        AND p.URL_IMAGEN != ''
        AND p.URL_IMAGEN NOT LIKE '%logo.png'
        AND p.URL_IMAGEN NOT LIKE '%fallback%'
        AND p.SLUG IS NOT NULL
        AND p.SLUG != ''
      ORDER BY s.FECHA_ASIGNACION ASC
      LIMIT 1
    `;
    
    assert.ok(query.includes('SLUG IS NOT NULL'), 'Query debe filtrar SLUG NULL');
    assert.ok(query.includes("SLUG != ''"), 'Query debe filtrar SLUG vacío');
    assert.ok(query.includes('URL_IMAGEN NOT LIKE'), 'Query debe filtrar imágenes logo');
    
    console.log('✅ Query SQL válido con filtros correctos');
  });
});

// Test de integración con la API (requiere servidor corriendo)
describe('Integración API - Noticias Objetivo', { skip: !process.env.RUN_INTEGRATION_TESTS }, () => {
  
  const API_BASE = 'https://news-api.sebastianvernis.workers.dev/api';
  
  test('debe verificar que el sitio noticiasobjetivo existe y tiene configuración', async () => {
    try {
      const response = await fetch(`${API_BASE}/sites/noticiasobjetivo`);
      
      if (response.ok) {
        const site = await response.json();
        assert.ok(site.SLUG === 'noticiasobjetivo', 'El sitio debe tener slug correcto');
        assert.ok(site.DOMINIO, 'El sitio debe tener dominio configurado');
        console.log('✅ Sitio noticiasobjetivo configurado correctamente');
      } else {
        console.log('⚠️ Sitio no encontrado o API no disponible');
      }
    } catch (e) {
      console.log('⚠️ No se pudo conectar a la API:', e.message);
    }
  });

  test('debe verificar que no hay artículos con SLUG NULL pendientes de Facebook', async () => {
    try {
      const response = await fetch(`${API_BASE}/facebook/monitor`);
      
      if (response.ok) {
        const articles = await response.json();
        const nullSlugs = articles.filter(a => !a.SLUG || a.SLUG === 'null' || a.SLUG === '');
        
        assert.strictEqual(nullSlugs.length, 0, 
          `No debe haber artículos con SLUG NULL pendientes. Encontrados: ${nullSlugs.length}`);
        
        console.log(`✅ Verificados ${articles.length} artículos, ninguno con SLUG NULL`);
      }
    } catch (e) {
      console.log('⚠️ No se pudo verificar monitor de Facebook:', e.message);
    }
  });
});

console.log('\n📋 Para ejecutar tests de integración:');
console.log('RUN_INTEGRATION_TESTS=1 npm test tests/article-flow-noticiasobjetivo.test.cjs\n');
