"""Align public previews with the native product25 oil-only assortment.

Historical reviews and source archives are intentionally outside this update.
Native SKU retirement is recorded separately in the administrator audit.
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
NAME = '더 젤리 플럼핑 립오일'
OLD = '더 젤리 플럼핑 립 시리즈'


def main():
    preview = ROOT / 'storefront-v2/preview'
    for name in ['about.html', 'jelly.html', 'search.html', 'shop.html', 'product-25.html']:
        path = preview / name
        text = path.read_text(encoding='utf-8').replace(OLD, NAME)
        if name == 'product-25.html':
            doc = BeautifulSoup(text, 'html.parser')
            for option in doc.select('select option'):
                if '[립글로스] 00.' in option.get('value', ''):
                    option.decompose()
            text = str(doc)
        path.write_text(text, encoding='utf-8')
    mapping = ROOT / 'storefront-v2/상품연결표.json'
    records = json.loads(mapping.read_text(encoding='utf-8'))
    catalog = preview / 'assets/preview-catalog.js'
    prefix = 'window.TAM_CATALOG='
    catalog_records = json.loads(catalog.read_text(encoding='utf-8').removeprefix(prefix).rstrip().removesuffix(';'))
    for rows in [records, catalog_records]:
        item = next(row for row in rows if row['id'] == 25)
        item['name'] = NAME
        for option in item['options']:
            option['values'] = [v for v in option['values'] if '[립글로스] 00.' not in v]
        assert sum(len(o['values']) for o in item['options']) == 3
    mapping.write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    catalog.write_text(prefix+json.dumps(catalog_records, ensure_ascii=False)+';\n', encoding='utf-8')
    import re
    for path in preview.glob('*.html'):
        text = path.read_text(encoding='utf-8')
        updated = re.sub(r'(assets/preview-catalog\.js)\?v=[^"\s>]+', r'\1?v=lipoil261023', text)
        if updated != text:
            path.write_text(updated, encoding='utf-8')
    print('Product25 identity synchronized across seven public files; three oil options.')


if __name__ == '__main__':
    main()
