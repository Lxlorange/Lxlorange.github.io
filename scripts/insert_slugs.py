import glob
import re
from pathlib import Path
from pypinyin import slug, Style
import unicodedata

posts = sorted(glob.glob('_posts/*.md'))

for path in posts:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    m = re.match(r'^(---\n.*?\n---\n)(.*)$', text, re.S)
    if not m:
        print('SKIP no fm', path)
        continue
    fm, rest = m.group(1), m.group(2)
    if re.search(r'^slug:\s*', fm, re.M):
        print('HAS slug', path)
        continue
    title_match = re.search(r'^title:\s*(.*)$', fm, re.M)
    if not title_match:
        print('MISSING title', path)
        continue
    title = title_match.group(1).strip()
    if (title.startswith("'") and title.endswith("'")) or (title.startswith('"') and title.endswith('"')):
        title = title[1:-1]
    s = slug(title, style=Style.NORMAL, separator='-')
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'[^A-Za-z0-9\-]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-').lower()
    if not s:
        s = re.sub(r'[^A-Za-z0-9]+', '-', title).strip('-').lower() or 'post'
    fm_new = re.sub(r'^(title:.*)$', r'\1\nslug: ' + s, fm, count=1, flags=re.M)
    p.write_text(fm_new + rest, encoding='utf-8')
    print('UPDATED', path, '=>', s)
