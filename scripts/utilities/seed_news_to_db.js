#!/usr/bin/env node
/**
 * Sistema de Seed de Noticias a Base de Datos
 * 
 * Toma noticias procesadas y las inserta en la base de datos D1
 * Distribuye automáticamente según categoría a los sitios correspondientes
 */

const fs = require('fs');
const path = require('path');
const { NewsProcessor } = require('./news-downloader');

// Configuración de mapeo de categorías a sitios
const SITE_TARGETS = {
  'politica': ['cbnnoticias', 'centralmexico', 'noticiasobjetivo'],
  'economia': ['cbnnoticias', 'mexicoinformado', 'reportecentralmx'],
  'deportes': ['radiocinconoticias', 'tvmexico', 'verticenoticias'],
  'tecnologia': ['nodoinformativo', 'verticenoticias', 'mexicoinformado'],
  'nacional': ['cbnnoticias', 'centralmexico', 'mexicoinformado', 'noticiasobjetivo'],
  'internacional': ['cbnnoticias', 'nodoinformativo', 'reportecentralmx'],
  'ciencia': ['nodoinformativo', 'verticenoticias', 'mexicoinformado'],
  'entretenimiento': ['radiocinconoticias', 'tvmexico', 'verticenoticias']
};

// Configuración
const CONFIG = {
  PROCESSED_DIR: './data/news_downloaded',
  OUTPUT_DIR: './data/news_downloaded',
  BATCH_SIZE: 10
};

// Utilidades
const Utils = {
  slugify(text) {
    if (!text) return '';
    return text
      .toString()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[áàäâã]/g, 'a')
      .replace(/[éèëê]/g, 'e')
      .replace(/[íìïî]/g, 'i')
      .replace(/[óòöôõ]/g, 'o')
      .replace(/[úùüû]/g, 'u')
      .replace(/[ñ]/g, 'n')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .substring(0, 100);
  },

  formatDate(date) {
    if (!date) return new Date().toISOString();
    return new Date(date).toISOString();
  },

  escapeSQL(str) {
    if (!str) return '';
    return str
      .replace(/'/g, "''")
      .replace(/\\/g, '\\\\')
      .replace(/\n/g, '\\n')
      .replace(/\r/g, '\\r');
  }
};

// Generador de SQL
const SQLGenerator = {
  generateInsertStatements(articles) {
    const statements = [];
    
    for (const article of articles) {
      const sites = SITE_TARGETS[article.category] || ['cbnnoticias'];
      const primarySite = sites[0];
      
      const sql = `
INSERT INTO ARTICULOS_PARAFRASEADOS (
  TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
  CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO,
  DESTACADO, VISTAS, ESTADO
) VALUES (
  '${Utils.escapeSQL(article.title)}',
  '${Utils.slugify(article.title)}',
  '${Utils.escapeSQL(article.content)}',
  '${Utils.escapeSQL(article.excerpt)}',
  '${article.category.toUpperCase()}',
  '${Utils.escapeSQL(article.author)}',
  '${Utils.formatDate(article.publishedAt)}',
  '${Utils.escapeSQL(article.imageUrl)}',
  '${primarySite}',
  0,
  0,
  'PUBLICADO'
);`;
      
      statements.push(sql);
    }
    
    return statements;
  },

  generateFullSQL(articles) {
    const header = `-- Seed de noticias generado el ${new Date().toISOString()}
-- Total: ${articles.length} artículos

BEGIN TRANSACTION;

`;
    
    const inserts = this.generateInsertStatements(articles).join('\n');
    
    const footer = `

COMMIT;
`;
    
    return header + inserts + footer;
  }
};

// API Client para insertar vía REST
const APIClient = {
  async insertArticle(article, apiBaseUrl = 'https://tu-worker.pages.dev') {
    try {
      const sites = SITE_TARGETS[article.category] || ['cbnnoticias'];
      
      const response = await fetch(`${apiBaseUrl}/api/articles`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: article.title,
          content: article.content,
          excerpt: article.excerpt,
          category: article.category,
          author: article.author,
          publishedAt: article.publishedAt,
          imageUrl: article.imageUrl,
          sites: sites.join(','),
          featured: false
        })
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`API Error: ${response.status} - ${error}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error insertando "${article.title.substring(0, 50)}...":`, error.message);
      return null;
    }
  },

  async insertBulk(articles, apiBaseUrl = 'https://tu-worker.pages.dev') {
    try {
      const response = await fetch(`${apiBaseUrl}/api/articles/bulk`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          articles: articles.map(a => ({
            title: a.title,
            content: a.content,
            excerpt: a.excerpt,
            category: a.category,
            author: a.author,
            publishedAt: a.publishedAt,
            imageUrl: a.imageUrl,
            sites: (SITE_TARGETS[a.category] || ['cbnnoticias']).join(','),
            featured: false
          }))
        })
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`API Error: ${response.status} - ${error}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error en bulk insert:', error.message);
      return null;
    }
  }
};

// Procesador principal
const SeedProcessor = {
  async seedFromFile(filePath, options = {}) {
    console.log(`📂 Leyendo archivo: ${filePath}\n`);
    
    const data = fs.readFileSync(filePath, 'utf8');
    const articles = JSON.parse(data);
    
    console.log(`📰 Total artículos a procesar: ${articles.length}\n`);
    
    if (options.sql) {
      // Generar SQL
      console.log('📝 Generando archivo SQL...');
      const sql = SQLGenerator.generateFullSQL(articles);
      const sqlFile = path.join(CONFIG.OUTPUT_DIR, `seed_articles_${Date.now()}.sql`);
      fs.writeFileSync(sqlFile, sql);
      console.log(`✅ SQL guardado en: ${sqlFile}`);
      
      console.log('\n📋 Para aplicar a la base de datos:');
      console.log(`   npx wrangler d1 execute news-db --file=${sqlFile}`);
    }
    
    if (options.api) {
      // Insertar vía API
      console.log('\n🌐 Insertando vía API...');
      
      if (options.bulk) {
        // Bulk insert
        const result = await APIClient.insertBulk(articles, options.apiUrl);
        if (result) {
          console.log(`✅ Insertados: ${result.inserted}`);
          if (result.errors) {
            console.log(`❌ Errores: ${result.errors.length}`);
          }
        }
      } else {
        // Individual inserts
        let success = 0;
        let failed = 0;
        
        for (let i = 0; i < articles.length; i++) {
          const article = articles[i];
          console.log(`   [${i + 1}/${articles.length}] ${article.title.substring(0, 50)}...`);
          
          const result = await APIClient.insertArticle(article, options.apiUrl);
          if (result) {
            success++;
          } else {
            failed++;
          }
          
          // Delay para no saturar la API
          await new Promise(r => setTimeout(r, 200));
        }
        
        console.log(`\n✅ Exitosos: ${success}`);
        console.log(`❌ Fallidos: ${failed}`);
      }
    }
    
    // Resumen por categoría
    const byCategory = {};
    articles.forEach(a => {
      byCategory[a.category] = (byCategory[a.category] || 0) + 1;
    });
    
    console.log('\n📊 Distribución por categoría:');
    Object.entries(byCategory).forEach(([cat, count]) => {
      const sites = SITE_TARGETS[cat] || ['cbnnoticias'];
      console.log(`  - ${cat}: ${count} artículos → ${sites.join(', ')}`);
    });
  },

  async seedFromLatest(options = {}) {
    // Buscar el archivo más reciente
    const files = fs.readdirSync(CONFIG.PROCESSED_DIR)
      .filter(f => f.startsWith('news_processed_') && f.endsWith('.json'))
      .map(f => ({
        name: f,
        path: path.join(CONFIG.PROCESSED_DIR, f),
        mtime: fs.statSync(path.join(CONFIG.PROCESSED_DIR, f)).mtime
      }))
      .sort((a, b) => b.mtime - a.mtime);
    
    if (files.length === 0) {
      console.error('❌ No se encontraron archivos de noticias procesadas');
      console.log('   Ejecuta primero: node news-downloader.js');
      return;
    }
    
    const latestFile = files[0].path;
    console.log(`📂 Usando archivo más reciente: ${files[0].name}\n`);
    
    await this.seedFromFile(latestFile, options);
  },

  async runFullPipeline(options = {}) {
    console.log('🚀 Ejecutando pipeline completo: Descarga → Parafraseo → Seed\n');
    
    // Paso 1: Descargar noticias
    console.log('📥 PASO 1: Descargando noticias...');
    const articles = await NewsProcessor.process();
    
    if (articles.length === 0) {
      console.error('❌ No se obtuvieron artículos');
      return;
    }
    
    // Paso 2: Seed a base de datos
    console.log('\n💾 PASO 2: Insertando en base de datos...');
    await this.seedFromLatest(options);
    
    console.log('\n✅ Pipeline completado');
  }
};

// CLI
async function main() {
  const args = process.argv.slice(2);
  const options = {
    sql: args.includes('--sql') || args.includes('-s'),
    api: args.includes('--api') || args.includes('-a'),
    bulk: args.includes('--bulk') || args.includes('-b'),
    pipeline: args.includes('--pipeline') || args.includes('-p'),
    apiUrl: args.find(a => a.startsWith('--url='))?.split('=')[1] || 'https://tu-worker.pages.dev',
    file: args.find(a => a.startsWith('--file='))?.split('=')[1]
  };

  console.log('='.repeat(60));
  console.log('  SEED DE NOTICIAS A BASE DE DATOS');
  console.log('='.repeat(60));
  console.log('');

  if (options.pipeline) {
    // Pipeline completo
    await SeedProcessor.runFullPipeline(options);
  } else if (options.file) {
    // Desde archivo específico
    await SeedProcessor.seedFromFile(options.file, options);
  } else {
    // Desde archivo más reciente
    await SeedProcessor.seedFromLatest(options);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { SeedProcessor, SITE_TARGETS, SQLGenerator, APIClient };
