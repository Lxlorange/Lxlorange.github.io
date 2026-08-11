import glob, re
from pathlib import Path

config = Path('_config.yml').read_text(encoding='utf-8')
print('config_permalink_correct=', 'permalink: /posts/:slug/' in config)

posts = sorted(glob.glob('_posts/*.md'))
missing_slug=[]
slug_issues=[]
for path in posts:
    text = Path(path).read_text(encoding='utf-8')
    fm = re.match(r'^(---\n.*?\n---\n)', text, re.S)
    if not fm:
        continue
    header = fm.group(1)
    if not re.search(r'^slug:\s*', header, re.M):
        missing_slug.append(path)
    m = re.search(r'^slug:\s*(.*)$', header, re.M)
    if m:
        slug = m.group(1).strip()
        if re.search(r'[\u4e00-\u9fff]', slug):
            slug_issues.append((path, slug))

print('missing_slug_count=', len(missing_slug))
print('slug_issue_count=', len(slug_issues))
for item in slug_issues[:20]:
    print('slug_issue:', item)

cats=set()
for path in posts:
    text = Path(path).read_text(encoding='utf-8')
    fm = re.match(r'^(---\n.*?\n---\n)', text, re.S)
    if not fm:
        continue
    header = fm.group(1)
    m = re.search(r'^categories:\s*\[(.*?)\]', header, re.M)
    if m:
        for item in re.split(r',\s*', m.group(1)):
            item = item.strip().strip('"').strip("'")
            if item:
                cats.add(item)
    else:
        lines = header.splitlines()
        i=0
        while i < len(lines):
            if re.match(r'^categories\s*:\s*$', lines[i]):
                i += 1
                while i < len(lines) and re.match(r'^\s+-\s*(.*)$', lines[i]):
                    cats.add(re.match(r'^\s+-\s*(.*)$', lines[i]).group(1).strip())
                    i += 1
                break
            i += 1
print('categories=', sorted(cats))

mapping = {}
if Path('_data/category_slugs.yml').exists():
    for line in Path('_data/category_slugs.yml').read_text(encoding='utf-8').splitlines():
        if ':' in line:
            k,v=line.split(':',1)
            mapping[k.strip()] = v.strip()
print('mapping_count=', len(mapping))
for cat in sorted(cats):
    if cat not in mapping:
        print('MISSING mapping for category:', cat)

pages = sorted(glob.glob('categories/*.md'))
print('category_pages_count=', len(pages))
for page in pages:
    text = Path(page).read_text(encoding='utf-8')
    perm = re.search(r'^permalink:\s*(.*)$', text, re.M)
    title = re.search(r'^title:\s*(.*)$', text, re.M)
    cate = re.search(r'^category:\s*(.*)$', text, re.M)
    print(page, 'permalink=', perm.group(1).strip() if perm else None, 'title=', title.group(1).strip() if title else None, 'category=', cate.group(1).strip() if cate else None)

# scan templates for raw category URL patterns that don't use mapping or slugify
for path in glob.glob('**/*.{html,md}', recursive=True):
    text = Path(path).read_text(encoding='utf-8')
    if 'categories/{{ category' in text or 'categories/{{ sub_category' in text or 'categories/{{ category_name' in text or 'categories/{{ sub_category' in text:
        print('raw category template', path)
