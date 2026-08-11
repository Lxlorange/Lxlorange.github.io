import glob, re
cats=set()
for path in glob.glob('_posts/*.md'):
    text=open(path,encoding='utf-8').read()
    m=re.search(r'^categories:\s*\[(.*?)\]', text, re.M)
    if m:
        for item in m.group(1).split(','):
            item=item.strip().strip('"').strip("'")
            if item: cats.add(item)
    else:
        lines=text.splitlines()
        for i,line in enumerate(lines):
            if line.strip()=='categories:':
                for j in range(i+1, min(i+20, len(lines))):
                    line2=lines[j].strip()
                    if line2.startswith('- '):
                        cats.add(line2[2:].strip())
                    else:
                        break
                break
with open('category-list.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(sorted(cats)))
