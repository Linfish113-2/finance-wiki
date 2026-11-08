#!/usr/bin/env python3
"""Finance Wiki 文章與網站建置產物的可重複測試；需要 PyYAML。"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import yaml

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--site', help='Check built Jekyll output directory')
args = parser.parse_args()
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

categories = yaml.safe_load((root / '_data/categories.yml').read_text(encoding='utf-8'))
ids = [x['id'] for x in categories]
check(len(ids) == len(set(ids)) == 7, 'categories.yml: category IDs must be unique, expected seven categories')
files = sorted((root / '_articles').glob('*.md'))
check(len(files) >= 1, 'No article Markdown files')
seen_slugs, all_records = set(), []
required = ['slug','title','category','order','description','tags','reading_time','updated','related','sources','risk_note']
for path in files:
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n',text,re.S)
    check(bool(match), f'{path.name}: YAML front matter missing or invalid')
    if not match: continue
    try: data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f'{path.name}: YAML parse error {e}')
        continue
    check(isinstance(data, dict), f'{path.name}: front matter must be a map')
    if not isinstance(data,dict): continue
    for key in required: check(key in data and data[key] not in (None,''),f'{path.name}: missing {key}')
    slug=data.get('slug','')
    check(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',str(slug))),f'{path.name}: invalid slug')
    check(path.stem==slug,f'{path.name}: slug does not match filename')
    check(slug not in seen_slugs,f'{path.name}: duplicate slug')
    seen_slugs.add(slug)
    check(data.get('category') in ids,f'{path.name}: category not in categories.yml')
    check(isinstance(data.get('order'),int),f'{path.name}: order must be integer')
    check(isinstance(data.get('tags'),list) and bool(data.get('tags')),f'{path.name}: tags need nonempty list')
    check(isinstance(data.get('related'),list),f'{path.name}: related must be list')
    check(re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(data.get('updated',''))) is not None,f'{path.name}: updated should be YYYY-MM-DD')
    check(isinstance(data.get('sources'),list) and bool(data.get('sources')),f'{path.name}: missing sources')
    for source in data.get('sources',[]):
        u=str(source.get('url','')) if isinstance(source,dict) else ''
        check(bool(u.startswith('https://') and urlparse(u).netloc) and 'example.' not in u,f'{path.name}: source URL invalid: {u}')
        check(bool(source.get('name')) if isinstance(source,dict) else False,f'{path.name}: source name missing')
    body=text[match.end():]
    check(body.count('## ')>=3,f'{path.name}: too few article headings')
    check('教學假設' in body,f'{path.name}: teaching example must be explicitly marked')
    check('風險' in body,f'{path.name}: missing risk discussion')
    all_records.append((path.name,data))
for name,record in all_records:
    for rel in record.get('related',[]): check(rel in seen_slugs,f'{name}: related slug not found: {rel}')
check(len({d.get('order') for _,d in all_records})==len(all_records),'Article order duplicated')
for c in ids: check(any(d.get('category')==c for _,d in all_records) or len(all_records)<7,f'Missing category article: {c}')
for file in ('AGENTS.md','README.md','_layouts/default.html','_layouts/article.html','search.json','assets/css/style.css','assets/js/main.js'):
    check((root/file).exists(),f'Missing required file: {file}')
if args.site:
    site=Path(args.site)
    check((site/'index.html').exists(),'Built homepage missing')
    check((site/'about/index.html').exists(),'Built about page missing')
    indexpath=site/'search.json'
    check(indexpath.exists(),'Built search.json missing')
    if indexpath.exists():
        try:
            index=json.loads(indexpath.read_text(encoding='utf-8'))
            check(len(index)==len(files),f'search.json article count mismatch: {len(index)} != {len(files)}')
            for a in index:
                check(all(k in a for k in ('title','description','category','tags','url')),'search.json missing field')
                check((site / a.get('url','').lstrip('/').removeprefix('finance-wiki/').rstrip('/') / 'index.html').exists(),f'Article page does not exist: {a.get("url")}')
        except Exception as e: errors.append(f'search.json parsing failed: {e}')
if errors:
    print('FAIL:',len(errors),'checks')
    for e in errors:print(' -',e)
    raise SystemExit(1)
print('PASS: article metadata, unique slugs, categories, sources, related links, templates'+ (' and built-site outputs' if args.site else ''))
print('ARTICLES:',len(files),'CATEGORIES:',len(ids))
