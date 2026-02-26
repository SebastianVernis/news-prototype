const assert = require('node:assert/strict');
const { test } = require('node:test');
const { read } = require('./helpers.cjs');

test('master flow references existing scripts', () => {
  const content = read('tools/news/master-news-flow.py');
  const required = [
    'api/newsapi.py',
    'api/worldnews.py',
    'news/paraphrase.py',
    'api/gemini_paraphraser.py',
    'api/generate-images-ai.py',
    'images/r2_image_manager.py',
    'site/update-images-preloaders.py',
    'site/create-complete-structure.py',
    'site/generate-sites.py',
    'site/gemini_style_audit.py',
  ];
  for (const ref of required) {
    assert.ok(content.includes(ref), `Missing script reference: ${ref}`);
  }
});
