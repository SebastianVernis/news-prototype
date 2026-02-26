#!/usr/bin/env node
/**
 * Sistema de Descarga de Noticias
 * 
 * Requerimientos:
 * - Categorías: política, economía, deportes, tecnología, nacional, internacional, ciencia, entretenimiento
 * - Mínimo 500 palabras en full text
 * - Parafraseo completo con IA (OpenRouter - Arcee Trinity Large)
 * - Imágenes correctamente mapeadas y usables
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { OpenRouterParaphraser } = require('./paraphraser-openrouter');

// Configuración
const CONFIG = {
  NEWS_APIS: [
    {
      name: 'NewsAPI',
      url: 'https://newsapi.org/v2/top-headlines',
      params: {
        country: 'mx',
        apiKey: process.env.NEWSAPI_KEY || 'demo-key',
        pageSize: 100
      }
    },
    {
      name: 'GNews',
      url: 'https://gnews.io/api/v4/top-headlines',
      params: {
        country: 'mx',
        lang: 'es',
        apikey: process.env.GNEWS_API_KEY || 'demo-key',
        max: 100
      }
    }
  ],
  
  CATEGORIES: {
    'politica': ['politics', 'política', 'government', 'gobierno', 'election', 'elección'],
    'economia': ['business', 'economy', 'economía', 'finance', 'finanzas', 'mercado', 'market'],
    'deportes': ['sports', 'deportes', 'fútbol', 'futbol', 'basketball', 'tennis'],
    'tecnologia': ['technology', 'tecnología', 'tech', 'ciencia', 'science', 'innovation'],
    'nacional': ['nacional', 'national', 'mexico', 'méxico', 'local'],
    'internacional': ['internacional', 'international', 'world', 'global'],
    'ciencia': ['science', 'ciencia', 'research', 'investigación', 'salud', 'health', 'medical'],
    'entretenimiento': ['entertainment', 'entretenimiento', 'cultura', 'culture', 'arte', 'art', 'cine', 'movie', 'música', 'music']
  },
  
  MIN_WORDS: 500,
  MAX_ARTICLES_PER_RUN: 50,
  REQUEST_TIMEOUT: 30000,
  
  OUTPUT_DIR: './data/news_downloaded',
  IMAGES_DIR: './assets/images'
};

// Instancia del parafraseador
const paraphraser = new OpenRouterParaphraser(process.env.OPENROUTER_API_KEY);

// Utilidades
const Utils = {
  countWords(text) {
    if (!text) return 0;
    return text.trim().split(/\s+/).length;
  },
  
  cleanHtml(html) {
    if (!html) return '';
    return html
      .replace(/<[^>]*>/g, ' ')
      .replace(/&nbsp;/g, ' ')
      .replace(/&amp;/g, '&')
      .replace(/</g, '<')
      .replace(/>/g, '>')
      .replace(/"/g, '"')
      .replace(/\s+/g, ' ')
      .trim();
  },
  
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
      .replace(/[ç]/g, 'c')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .substring(0, 100);
  },
  
  mapCategory(sourceCategory) {
    if (!sourceCategory) return 'nacional';
    const catLower = sourceCategory.toLowerCase();
    for (const [targetCat, synonyms] of Object.entries(CONFIG.CATEGORIES)) {
      if (synonyms.some(s => catLower.includes(s))) {
        return targetCat;
      }
    }
    return 'nacional';
  },
  
  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  },
  
  formatDate(date) {
    if (!date) return new Date().toISOString();
    return new Date(date).toISOString();
  },
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
};

// Descargador de imágenes
const ImageDownloader = {
  async downloadImage(url, filename) {
    if (!url || url.includes('placeholder')) {
      return null;
    }
    
    const ext = path.extname(new URL(url).pathname) || '.jpg';
    const safeFilename = `${filename}${ext}`;
    const outputPath = path.join(CONFIG.IMAGES_DIR, safeFilename);
    
    if (fs.existsSync(outputPath)) {
      return `assets/images/${safeFilename}`;
    }
    
    return new Promise((resolve) => {
      const client = url.startsWith('https:') ? https : http;
      
      const request = client.get(url, { timeout: CONFIG.REQUEST_TIMEOUT }, (response) => {
        if (response.statusCode !== 200) {
          resolve(null);
          return;
        }
        
        const file = fs.createWriteStream(outputPath);
        response.pipe(file);
        
        file.on('finish', () => {
          file.close();
          resolve(`assets/images/${safeFilename}`);
        });
        
        file.on('error', () => resolve(null));
      });
      
      request.on('error', () => resolve(null));
      request.on('timeout', () => {
        request.destroy();
        resolve(null);
      });
    });
  }
};

// Fetcher de noticias
const NewsFetcher = {
  async fetchFromAPI(apiConfig) {
    try {
      const url = new URL(apiConfig.url);
      Object.entries(apiConfig.params).forEach(([key, value]) => {
        url.searchParams.append(key, value);
      });
      
      console.log(`📡 Fetching from ${apiConfig.name}...`);
      
      const response = await fetch(url.toString(), {
        timeout: CONFIG.REQUEST_TIMEOUT
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      return this.normalizeArticles(data.articles || data.data || [], apiConfig.name);
    } catch (error) {
      console.error(`❌ Error fetching from ${apiConfig.name}:`, error.message);
      return [];
    }
  },
  
  normalizeArticles(articles, source) {
    return articles.map(article => ({
      id: Utils.generateId(),
      source: source,
      originalTitle: article.title || article.headline || '',
      originalContent: article.content || article.description || article.body || '',
      description: article.description || article.summary || '',
      url: article.url || article.link || '',
      imageUrl: article.urlToImage || article.image || article.imageUrl || '',
      publishedAt: article.publishedAt || article.published || article.date || new Date().toISOString(),
      sourceName: article.source?.name || article.source || source,
      category: article.category || Utils.mapCategory(article.category || article.section || 'general'),
      author: article.author || article.byline || 'Redacción'
    }));
  },
  
  async fetchFullText(article) {
    if (Utils.countWords(article.originalContent) >= CONFIG.MIN_WORDS) {
      return article.originalContent;
    }
    
    const combined = `${article.originalContent}\n\n${article.description}`;
    
    if (Utils.countWords(combined) >= CONFIG.MIN_WORDS) {
      return combined;
    }
    
    return null;
  }
};

// Procesador principal
const NewsProcessor = {
  async process() {
    console.log('🚀 Iniciando descarga de noticias...\n');
    
    if (!fs.existsSync(CONFIG.OUTPUT_DIR)) {
      fs.mkdirSync(CONFIG.OUTPUT_DIR, { recursive: true });
    }
    if (!fs.existsSync(CONFIG.IMAGES_DIR)) {
      fs.mkdirSync(CONFIG.IMAGES_DIR, { recursive: true });
    }
    
    const allArticles = [];
    const processedArticles = [];
    
    for (const api of CONFIG.NEWS_APIS) {
      const articles = await NewsFetcher.fetchFromAPI(api);
      allArticles.push(...articles);
      await Utils.delay(1000);
    }
    
    console.log(`📰 Total artículos obtenidos: ${allArticles.length}\n`);
    
    let count = 0;
    for (const article of allArticles) {
      if (count >= CONFIG.MAX_ARTICLES_PER_RUN) break;
      
      console.log(`📝 Procesando: ${article.originalTitle.substring(0, 60)}...`);
      
      const fullText = await NewsFetcher.fetchFullText(article);
      if (!fullText) {
        console.log('   ⏭️  Descartado: contenido insuficiente (< 500 palabras)');
        continue;
      }
      
      const wordCount = Utils.countWords(fullText);
      console.log(`   ✅ Palabras: ${wordCount}`);
      
      console.log('   🤖 Parafraseando con IA (Arcee Trinity Large)...');
      const paraphrased = await paraphraser.paraphraseArticle(
        article.originalTitle,
        fullText,
        article.category
      );
      
      console.log('   🖼️  Descargando imagen...');
      const localImagePath = await ImageDownloader.downloadImage(
        article.imageUrl,
        Utils.slugify(article.id)
      );
      
      const processedArticle = {
        id: article.id,
        slug: Utils.slugify(paraphrased.title),
        title: paraphrased.title,
        content: paraphrased.content,
        excerpt: paraphrased.excerpt || article.description.substring(0, 200) + '...',
        category: article.category,
        author: article.author,
        publishedAt: Utils.formatDate(article.publishedAt),
        imageUrl: localImagePath || article.imageUrl,
        originalUrl: article.url,
        source: article.sourceName,
        wordCount: paraphrased.wordCount || wordCount,
        processedAt: new Date().toISOString(),
        paraphrasedBy: paraphrased.simulated ? 'simulated' : 'arcee-trinity-large'
      };
      
      processedArticles.push(processedArticle);
      count++;
      
      console.log(`   ✓ Artículo procesado: ${processedArticle.category}\n`);
      await Utils.delay(500);
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputFile = path.join(CONFIG.OUTPUT_DIR, `news_processed_${timestamp}.json`);
    
    fs.writeFileSync(outputFile, JSON.stringify(processedArticles, null, 2));
    
    console.log('\n' + '='.repeat(50));
    console.log('📊 RESUMEN');
    console.log('='.repeat(50));
    console.log(`Total procesado: ${processedArticles.length} artículos`);
    console.log(`Guardado en: ${outputFile}`);
    
    const byCategory = {};
    processedArticles.forEach(a => {
      byCategory[a.category] = (byCategory[a.category] || 0) + 1;
    });
    
    console.log('\nPor categoría:');
    Object.entries(byCategory).forEach(([cat, count]) => {
      console.log(`  - ${cat}: ${count}`);
    });
    
    return processedArticles;
  }
};

if (require.main === module) {
  NewsProcessor.process().catch(console.error);
}

module.exports = { NewsProcessor, CONFIG, Utils };
