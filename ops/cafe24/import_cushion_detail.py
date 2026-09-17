"""Install the user's final 0908 cushion detail assets without re-encoding."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('C:/Users/BNK-1/Downloads/jelly-skin-cushion_0908')
SLUG = 'jelly-skin-cushion-0908'
preview_assets = ROOT/'storefront-v2/preview/assets'/SLUG
native_assets = ROOT/'storefront-v2/cafe24/tam/assets'/SLUG
for folder in (preview_assets, native_assets):
    folder.mkdir(parents=True, exist_ok=True)
original_html = (SOURCE/'jelly-skin-cushion_0908.html').read_text(encoding='utf-8')
names = re.findall(r'<IMG SRC="([^"]+)"', original_html, re.I)
available = {p.name.lower(): p for p in SOURCE.iterdir() if p.is_file()}
assert len(names) == 10, 'Unexpected final detail section count'
records = []
for number, name in enumerate(names, 1):
    source = available[name.lower()]
    target = f'{number:02d}{source.suffix.lower()}'
    with Image.open(source) as image:
        width, height = image.size
        frames = getattr(image, 'n_frames', 1)
    for folder in (preview_assets, native_assets):
        shutil.copy2(source, folder/target)
    records.append({'order': number, 'source_name': source.name, 'file': target,
        'width': width, 'height': height, 'frames': frames, 'bytes': source.stat().st_size,
        'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})

def markup(prefix):
    return '\n'.join(f'<img src="{prefix}/{r["file"]}" width="{r["width"]}" height="{r["height"]}" '
        f'loading="lazy" decoding="async" alt="더 젤리 스킨 쿠션 제품 상세 정보 {r["order"]}"/>' for r in records)

page = ROOT/'storefront-v2/preview/product-23.html'
html = page.read_text(encoding='utf-8')
section = ('<section class="detail-source container cushion-final-detail" id="product-detail" '
    'aria-label="더 젤리 스킨 쿠션 제품 상세"><h2>제품 상세</h2>'
    '<div class="detail-images">' + markup('assets/'+SLUG) + '</div>'
    '<a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section>')
html = html.replace('class="preview-options" data-preview-product="23"', 'class="preview-options" id="purchase-options" data-preview-product="23"')
pattern = r'<details class="detail-source container">.*?</details>|<section class="detail-source container cushion-final-detail".*?</section>'
html, count = re.subn(pattern, lambda _: section, html, count=1, flags=re.S)
assert count == 1, 'Could not locate cushion detail section'
if 'assets/cushion-final-detail.css' not in html:
    html = html.replace('</head>', '<link rel="stylesheet" href="assets/cushion-final-detail.css?v=0908"/>\n</head>')
page.write_text(html, encoding='utf-8')
native = ROOT/'storefront-v2/cafe24/tam/sections/cushion-detail-0908.html'
native.write_text('<!-- Product 23 only: paste into its product description after uploading /tam/assets/'+SLUG+'/ -->\n'
    '<div style="max-width:860px;margin:0 auto;font-size:0;line-height:0">\n' +
    markup('/tam/assets/'+SLUG).replace('<img ', '<img style="display:block;width:100%;height:auto;border:0" ') +
    '\n</div>\n', encoding='utf-8')
manifest = {'source_package': 'jelly-skin-cushion_0908.zip', 'source_html': 'jelly-skin-cushion_0908.html',
    'product_no': 23, 'method': 'Original bytes and source order retained; uppercase JPG references normalized for case-sensitive hosting.',
    'total_bytes_per_copy': sum(r['bytes'] for r in records), 'sections': records,
    'production_status': 'Prepared native assets and HTML; live Cafe24 product description not changed.'}
(ROOT/'ops/cafe24/cushion-detail-0908.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Installed {len(records)} final sections; {manifest["total_bytes_per_copy"]:,} bytes per copy; animated WebP preserved.')
