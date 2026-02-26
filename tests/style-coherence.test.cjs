const assert = require('node:assert/strict');
const { test } = require('node:test');
const { exists, list, read } = require('./helpers.cjs');

const templatesDir = 'public/templates/css';

function templateNumbers(files) {
  return files
    .filter((f) => /^template\d+\.css$/.test(f))
    .map((f) => Number(f.replace('template', '').replace('.css', '')))
    .sort((a, b) => a - b);
}

test('template CSS files exist and are coherent', () => {
  assert.ok(exists(templatesDir), 'Missing public/templates/css');
  const files = list(templatesDir);
  const nums = templateNumbers(files);
  assert.ok(nums.length >= 10, 'Expected at least 10 templates');
  for (let i = 1; i <= 10; i += 1) {
    assert.ok(nums.includes(i), `Missing template${i}.css`);
  }
});

test('site generator points to templates/css for styling', () => {
  const content = read('tools/site/generate-sites.py');
  assert.ok(content.includes('CSS_LINK_PATH = os.getenv("NEWS_TEMPLATES_LINK", "templates/css")'));
});
