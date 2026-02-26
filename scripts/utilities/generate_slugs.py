import json, re, uuid

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:100]

def esc(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

data = json.load(open('data/noticias_paraphrased_20260219_045326.json'))
seen_pids = set()

lines = ['-- Update slugs for existing articles']
for art in data:
    pid = art.get('variation_id') or str(uuid.uuid4())
    if pid in seen_pids:
        pid = str(uuid.uuid4())
    seen_pids.add(pid)
    title = art.get('title') or art.get('original_title') or 'sin-titulo'
    slug = slugify(title)
    lines.append(f'UPDATE ARTICULOS_PARAFRASEADOS SET SLUG={esc(slug)} WHERE ID={esc(pid)};')

with open('update_slugs.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Generated {len(lines)-1} UPDATE statements')
print('Sample slug:', slugify(data[0].get('title', '')))
print('Sample ID:', data[0].get('variation_id', ''))
