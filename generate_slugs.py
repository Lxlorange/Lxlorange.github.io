import glob, re
from pathlib import Path
from pypinyin import slug
import unicodedata

posts = sorted(glob.glob('_posts/*.md'))

existing = {}
for path in posts:
    text = Path(path).read_text(encoding='utf-8')
    m = re.search(r'^title:\s*(.*)$', text, re.M)
    if not m:
        print('MISSING TITLE', path)
        continue
    title = m.group(1).strip().strip('"')
    # remove quotes around title if any
    if title.startswith('"') and title.endswith('"'):
        title = title[1:-1]
    if title.startswith("'") and title.endswith("'"):
        title = title[1:-1]
    # convert Chinese to pinyin and preserve ASCII
    s = slug(title, style=None, separator='-')
    # pypinyin.slug with style None may produce digits? let's normalize
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'[^a-zA-Z0-9\-]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-').lower()
    if not s:
        s = re.sub(r'[^a-zA-Z0-9]+', '-', title).strip('-').lower() or 'post'
    orig = s
    i = 1
    while s in existing.values():
        i += 1
        s = f'{orig}-{i}'
    existing[path] = s
    print(path, '=>', s)
