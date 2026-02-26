const assert = require('node:assert/strict');
const { test } = require('node:test');
const { exists, read } = require('./helpers.cjs');

function readJson(relPath) {
  return JSON.parse(read(relPath));
}

test('package.json has required scripts', () => {
  const pkg = readJson('package.json');
  const scripts = pkg.scripts || {};
  for (const key of ['dev', 'build', 'preview', 'deploy', 'test']) {
    assert.ok(scripts[key], `Missing npm script: ${key}`);
  }
});

test('wrangler configs exist', () => {
  assert.ok(exists('wrangler.toml'), 'Missing wrangler.toml');
  assert.ok(exists('src/wrangler.toml'), 'Missing src/wrangler.toml');
});
