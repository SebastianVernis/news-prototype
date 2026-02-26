const assert = require('node:assert/strict');
const { test } = require('node:test');
const { spawnSync } = require('node:child_process');

test('linguistic paraphraser runs without heavy deps', () => {
  const code = [
    "from tools.api.linguistic_paraphraser import LinguisticParaphraser",
    "rewriter = LinguisticParaphraser()",
    "res = rewriter.paraphrase_text('El presidente anunció nuevas medidas económicas.')",
    "print(res.get('text') or '')",
  ].join("\n");
  const result = spawnSync('python3', ['-c', code], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr || 'python failed');
  assert.ok(result.stdout.trim().length > 0, 'Expected output from paraphraser');
});
