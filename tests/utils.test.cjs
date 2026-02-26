const assert = require('node:assert/strict');
const { test } = require('node:test');
const { exists, read } = require('./helpers.cjs');

test('utils helpers exist', () => {
  assert.ok(exists('utils/utils.py'), 'Missing utils/utils.py');
  const content = read('utils/utils.py');
  for (const fn of ['normalize_article', 'save_articles', 'print_summary', 'enrich_with_full_text']) {
    assert.ok(content.includes(`def ${fn}`), `Missing function: ${fn}`);
  }
});
