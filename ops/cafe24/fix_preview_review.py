"""Repair the preview entry point and final cushion detail return link."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / 'storefront-v2/preview'
(PREVIEW / 'index.html').write_text('''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>tam BEAUTY</title>
<script>location.replace('design-only.html' + location.search + location.hash);</script>
<meta http-equiv="refresh" content="0;url=design-only.html">
</head><body><a href="design-only.html">탐뷰티 홈으로 이동</a></body></html>
''', encoding='utf-8')
path = PREVIEW / 'product-23.html'
html = path.read_text(encoding='utf-8')
html = html.replace('class="preview-options" data-preview-product="23"', 'class="preview-options" id="purchase-options" data-preview-product="23"')
if 'class="detail-return"' not in html:
    html = html.replace('</div></section><section class="shop-section', '</div><a class="detail-return" href="#purchase-options">색상 선택으로 돌아가기 ↑</a></section><section class="shop-section', 1)
html = html.replace('cushion-final-detail.css?v=0908', 'cushion-final-detail.css?v=review1')
path.write_text(html, encoding='utf-8')
path = PREVIEW / 'design-only.html'
html = path.read_text(encoding='utf-8')
html = html.replace('<a href="#lookbook">룩북</a></nav>', '<a href="#lookbook">룩북</a><a href="basket.html">장바구니</a></nav>')
path.write_text(html, encoding='utf-8')
for path in PREVIEW.glob('*.html'):
    if path.name in ('design-before-balance.html', 'video-review.html'):
        continue
    html = path.read_text(encoding='utf-8')
    html = html.replace('tam.js?v=cushion2', 'tam.js?v=review1').replace('purchase-experience.js?v=4', 'purchase-experience.js?v=review1')
    path.write_text(html, encoding='utf-8')
