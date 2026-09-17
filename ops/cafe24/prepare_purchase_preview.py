"""Attach the opt-in purchase preview and sync reusable assets into the skin package."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
preview = ROOT / 'storefront-v2/preview'
assets = ['purchase-policy.js', 'purchase-experience.js', 'purchase-experience.css']
includes = '\n'.join([
    '<link rel="stylesheet" href="assets/purchase-experience.css?v=4"/>',
    '<script defer src="assets/purchase-policy.js?v=4"></script>',
    '<script defer src="assets/purchase-experience.js?v=4"></script>'
])
for path in [*preview.glob('product-*.html'), preview/'design-only.html', preview/'index.html', preview/'shop.html']:
    text = path.read_text(encoding='utf-8')
    if 'assets/purchase-experience.js' not in text:
        text = text.replace('</head>', includes + '\n</head>', 1)
    if 'data-tam-purchase-preview' not in text:
        text = re.sub(r'<body\b', '<body data-tam-purchase-preview', text, count=1)
    for asset in assets:
        text = re.sub(re.escape('assets/' + asset) + r'\?v=\d+', 'assets/' + asset + '?v=4', text)
    path.write_text(text, encoding='utf-8')
for name in assets:
    shutil.copy2(preview/'assets'/name, ROOT/'storefront-v2/cafe24/tam/assets'/name)
print('Attached preview to 14 products and home/shop pages; native assets copied without enabling live behavior.')
