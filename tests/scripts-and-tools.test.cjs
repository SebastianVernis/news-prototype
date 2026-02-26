const assert = require('node:assert/strict');
const { test } = require('node:test');
const { exists, list, read } = require('./helpers.cjs');

const expectedScripts = [
  'scripts/deploy/deploy-menu.sh',
  'scripts/deploy/deploy-10-sites.sh',
  'scripts/deploy/deploy-complete-sites.sh',
  'scripts/deploy/deploy-final-10-sites.sh',
  'scripts/deploy/deploy-all-sites-mime-fix.sh',
  'scripts/deploy/create-and-deploy-10-sites.sh',
  'scripts/deploy/redeploy-with-css.sh',
  'scripts/setup/install-publisher.sh',
  'scripts/run/run-publisher.sh',
];

const expectedTools = [
  'tools/news/master-news-flow.py',
  'tools/news/news-flow-complete.py',
  'tools/news/news-publisher.py',
  'tools/site/generate-sites.py',
  'tools/site/create-complete-structure.py',
  'tools/images/r2_image_manager.py',
  'tools/api/update_api_images.py',
];

test('expected scripts exist', () => {
  for (const script of expectedScripts) {
    assert.ok(exists(script), `Missing script: ${script}`);
  }
});

test('expected tools exist', () => {
  for (const tool of expectedTools) {
    assert.ok(exists(tool), `Missing tool: ${tool}`);
  }
});

test('scripts index references deploy directory', () => {
  const content = read('scripts/INDEX.md');
  assert.ok(content.includes('deploy/'), 'scripts/INDEX.md should mention deploy/');
});

test('docs index references core docs', () => {
  const content = read('docs/INDEX.md');
  assert.ok(content.includes('README.md'), 'docs/INDEX.md should reference README.md');
  assert.ok(content.includes('README_DEPLOY.md'), 'docs/INDEX.md should reference README_DEPLOY.md');
});

