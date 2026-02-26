const assert = require('node:assert/strict');
const { test } = require('node:test');
const { exists, isDirectory } = require('./helpers.cjs');

const requiredDirs = [
  'public',
  'src',
  'docs',
  'scripts',
  'tools',
  'functions',
  'workers',
  'assets',
  'assets/images',
  'data',
  'data/logs',
  'data/news_queue',
  'data/published_news',
  'sites',
  'generated_images',
];

const requiredIndexFiles = [
  'docs/INDEX.md',
  'scripts/INDEX.md',
  'scripts/build/INDEX.md',
  'scripts/deploy/INDEX.md',
  'scripts/verify/INDEX.md',
  'scripts/run/INDEX.md',
  'scripts/setup/INDEX.md',
  'scripts/templates/INDEX.md',
  'tools/INDEX.md',
  'tools/news/INDEX.md',
  'tools/site/INDEX.md',
  'tools/images/INDEX.md',
  'tools/api/INDEX.md',
  'public/INDEX.md',
  'functions/INDEX.md',
  'workers/INDEX.md',
  'src/INDEX.md',
  'utils/INDEX.md',
  'build/INDEX.md',
];

test('required directories exist', () => {
  for (const dir of requiredDirs) {
    assert.ok(exists(dir), `Missing directory: ${dir}`);
    assert.ok(isDirectory(dir), `Not a directory: ${dir}`);
  }
});

test('index files exist', () => {
  for (const file of requiredIndexFiles) {
    assert.ok(exists(file), `Missing index file: ${file}`);
  }
});
