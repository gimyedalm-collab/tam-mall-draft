"""Install the lip liner final detail page (lipliner-rNN/upload) into product 118 without re-encoding.

Same approach as import_cushion_detail.py: original bytes and source order are kept, the collapsed
legacy detail block is replaced by an expanded final-detail section, a native Cafe24 description
snippet is prepared, and a manifest with hashes is written. Re-runnable.

Usage: python -X utf8 ops/cafe24/import_lipliner_detail.py [r32]
"""
from pathlib import Path
from PIL import Image
import hashlib
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
RELEASE = (sys.argv[1] if len(sys.argv) > 1 else 'r32').lower()
SOURCE = ROOT / f'lipliner-{RELEASE}'
PRODUCT_NO = 118
PRODUCT_NAME = '더 클라우드 플럼핑 립 라이너'
SLUG = f'cloud-plumping-lip-liner-{RELEASE}'

source_html = (SOURCE / 'index.html').read_text(encoding='utf-8')
names = re.findall(r'src="(upload/[^"]+)"', source_html)
assert names, 'No detail images found in the release page'

preview_assets = ROOT / 'storefront-v2/preview/assets' / SLUG
native_assets = ROOT / 'storefront-v2/cafe24/tam/assets' / SLUG
for folder in (preview_assets, native_assets):
    folder.mkdir(parents=True, exist_ok=True)

records = []
for order, name in enumerate(names, 1):
    source = SOURCE / name
    with Image.open(source) as image:
        width, height = image.size
        frames = getattr(image, 'n_frames', 1)
    for folder in (preview_assets, native_assets):
        shutil.copy2(source, folder / source.name)
    records.append({'order': order, 'file': source.name, 'width': width, 'height': height, 'frames': frames,
                    'bytes': source.stat().st_size, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})


def markup(prefix, style=''):
    return '\n'.join(
        f'<img {style}src="{prefix}/{r["file"]}" width="{r["width"]}" height="{r["height"]}" '
        f'loading="lazy" decoding="async" alt="{PRODUCT_NAME} 제품 상세 정보 {r["order"]}" />' for r in records)


page = ROOT / f'storefront-v2/preview/product-{PRODUCT_NO}.html'
html = page.read_text(encoding='utf-8')
# The layout class was introduced for the cushion; it is the generic "final detail" layout (860px column, no seams).
section = ('<section class="detail-source container cushion-final-detail" id="product-detail" '
           f'aria-label="{PRODUCT_NAME} 제품 상세" data-detail-release="{RELEASE}"><h2>제품 상세</h2>\n'
           '<div class="detail-images">\n' + markup('assets/' + SLUG) + '\n</div>\n'
           '<a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section>')
pattern = (r'<details\s+class="detail-source container"\s*>.*?</details>'
           r'|<section\s+class="detail-source container cushion-final-detail".*?</section>')
html, count = re.subn(pattern, lambda _: section, html, count=1, flags=re.S)
assert count == 1, 'Could not locate the product detail block'
if 'id="purchase-options"' not in html:
    html, count = re.subn(r'(<div\s+class="preview-options")', r'\1 id="purchase-options"', html, count=1)
    assert count == 1, 'Could not locate the purchase options block'
if 'assets/cushion-final-detail.css' not in html:
    html = html.replace('</head>', '<link rel="stylesheet" href="assets/cushion-final-detail.css?v=review1" />\n</head>', 1)
page.write_bytes(html.encode('utf-8'))

native = ROOT / f'storefront-v2/cafe24/tam/sections/lipliner-detail-{RELEASE}.html'
native.write_bytes((
    f'<!-- Product {PRODUCT_NO} only: paste into its product description after uploading /tam/assets/{SLUG}/ -->\n'
    '<div style="max-width:860px;margin:0 auto;font-size:0;line-height:0">\n'
    + markup('/tam/assets/' + SLUG, 'style="display:block;width:100%;height:auto;border:0" ') + '\n</div>\n').encode('utf-8'))

manifest = {'source': f'lipliner-{RELEASE}/upload (final-only preview in this repository)', 'product_no': PRODUCT_NO,
            'method': 'Original bytes, names and source order retained; animated WebP preserved; no resampling.',
            'total_bytes_per_copy': sum(r['bytes'] for r in records),
            'total_height_at_860px': sum(round(r['height'] * 860 / r['width']) for r in records), 'sections': records,
            'production_status': 'Preview updated and native assets/HTML prepared; live Cafe24 product description not changed.'}
(ROOT / f'ops/cafe24/lipliner-detail-{RELEASE}.json').write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(f'Installed {len(records)} sections from lipliner-{RELEASE}; {manifest["total_bytes_per_copy"]:,} bytes per copy; '
      f'{manifest["total_height_at_860px"]:,}px tall; animated: {sum(1 for r in records if r["frames"] > 1)}')
