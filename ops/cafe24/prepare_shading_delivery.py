"""Prepare published V9 for storefront integration without re-rendering media."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'heart-shading-v9'
PREFIX = '/web/upload/tam-detail-20261021/heart-shading/'


def main():
    manifest = json.loads((PACKAGE / 'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['images']:
        assert hashlib.sha256((PACKAGE / item['file']).read_bytes()).hexdigest() == item['sha256']
    source = (PACKAGE / 'index.html').read_text(encoding='utf-8')
    count = 0

    def loading(match):
        nonlocal count
        tag = re.sub(r'\s(?:loading|decoding|fetchpriority)="[^"]*"', '', match.group(0))
        count += 1
        return tag[:-1] + ' decoding="async"' + (' fetchpriority="high">' if count == 1 else ' loading="lazy">')

    source = re.sub(r'<img\b[^>]*>', loading, source)
    assert count == 6
    body = re.search(r'<body\b[^>]*>(.*?)</body>', source, re.S).group(1)
    (PACKAGE / 'index.html').write_text(source, encoding='utf-8')
    (PACKAGE / 'detail.local.html').write_text(body, encoding='utf-8')
    hosted = re.sub(r'src="images/([^"]+)"', lambda m: 'src="' + PREFIX + 'images/' + m[1] + '"', body)
    (PACKAGE / 'cafe24-detail.html').write_text(hosted, encoding='utf-8')
    facts = str(BeautifulSoup(body, 'html.parser').select_one('section[aria-label="상품정보"]'))
    assert facts != 'None'
    (PACKAGE / 'product-information.html').write_text(facts, encoding='utf-8')
    manifest.update(product_no=109, delivery_prefix=PREFIX,
                    owner_integration_authorized='2026-10-21: latest V9 requested',
                    loading='First image high priority; remaining five lazy; async decoding',
                    product_information_sha256=hashlib.sha256(facts.encode()).hexdigest())
    (PACKAGE / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    names = ['index.html', 'detail.local.html', 'cafe24-detail.html', 'product-information.html', 'manifest.json', '등록안내.txt']
    names += [item['file'] for item in manifest['images']]
    with zipfile.ZipFile(PACKAGE / 'heart-shading-cafe24-v9.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(PACKAGE / name, name)
    print('V9: six original PNGs preserved; five lazy; explicit Cafe24 upload paths; ZIP refreshed.')


if __name__ == '__main__':
    main()
