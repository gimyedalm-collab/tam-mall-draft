"""Package the approved R30 snapshot without publishing unused/rejected assets.

Usage: python ops/cafe24/package_highlighter_r30.py /path/to/approved-r30
Only the highlighter description in the GitHub storefront preview is replaced.
No Cafe24 administration, product options, prices or review content are changed.
"""
from pathlib import Path
import base64
import hashlib
import json
import re
import shutil
import sys
import subprocess

repo = Path(__file__).resolve().parents[2]
source = Path(sys.argv[1]).resolve()
dest = repo / 'highlighter-r30'
dest.mkdir(exist_ok=True)
(dest / 'assets').mkdir(exist_ok=True)
(dest / 'figma-import').mkdir(exist_ok=True)
page = (source / 'index.html').read_text(encoding='utf-8')
layout = json.loads((source / 'layout.json').read_text(encoding='utf-8'))
assets = set(re.findall(r'(?:src="|url\(\')assets/([^"\']+)', page))
assets.update(['Manrope-OFL.txt', 'PretendardVariable.woff2'])
for name in sorted(assets):
    assert Path(name).name == name
    shutil.copy2(source / 'assets' / name, dest / 'assets' / name)
shutil.copy2(repo / 'storefront-v2/preview/assets/Pretendard-LICENSE.txt', dest / 'assets/Pretendard-LICENSE.txt')
for name in ['index.html', 'product-information.html', 'layout.json']:
    shutil.copy2(source / name, dest / name)
# A fixed-ratio embed must not acquire its own scrollbar from subpixel rounding.
# Reader links open as full pages rather than inside a very tall static frame.
embed=page.replace('</head>', '<base target="_top"><style>html,body{overflow:hidden}</style></head>')
(dest/'embed.html').write_text(embed, encoding='utf-8')

# Figma SVG import is a static representation; preserve the web motions above.
for order, section in enumerate(layout['sections'], 1):
    svg = (source / 'editable-svg' / (section['name'] + '.svg')).read_text(encoding='utf-8')
    for name in ['tam-pearl-detail', 'tam-intro-1']:
        motion = 'data:image/webp;base64,' + base64.b64encode((source/'assets'/(name+'.webp')).read_bytes()).decode()
        still = 'data:image/jpeg;base64,' + base64.b64encode((source/'assets'/(name+'-still.jpg')).read_bytes()).decode()
        svg = svg.replace(motion, still)
    (dest/'figma-import'/f'{order:02d}-{section["name"]}.svg').write_text(svg, encoding='utf-8')

product = repo / 'storefront-v2/preview/product-24.html'
# This isolated publish worktree starts at origin/main. Preserve every byte
# outside our integration block, including the repository's mixed line endings.
existing = subprocess.check_output(['git', 'show', 'HEAD:storefront-v2/preview/product-24.html'], cwd=repo).decode('utf-8')
replacement = '''      <section class="highlighter-final-detail" id="product-detail" aria-label="더 젤리 빔 하이라이터 상세 정보">
        <div class="highlighter-detail-frame">
          <iframe src="../../highlighter-r30/embed.html" title="더 젤리 빔 하이라이터 상세페이지" loading="lazy" scrolling="no"></iframe>
        </div>
        <a class="highlighter-detail-return" href="#purchase-options">컬러 선택으로 돌아가기 ↑</a>
      </section>'''
if 'class="highlighter-final-detail"' not in existing:
    existing, count = re.subn(r'      <details class="detail-source container">.*?</details>', replacement, existing, count=1, flags=re.S)
    assert count == 1
    existing = existing.replace('<div class="preview-options" data-preview-product="24">', '<div class="preview-options" id="purchase-options" data-preview-product="24">')
    existing = existing.replace('    <link href="assets/tam.css" rel="stylesheet" />', '    <link href="assets/tam.css" rel="stylesheet" />\n    <link href="assets/highlighter-final-detail.css" rel="stylesheet" />')
    product.write_bytes(existing.encode('utf-8'))

manifest = {
    'version': 'R30 / 2026-10-01 / approved typography check',
    'width': 860,
    'height': sum(s['height'] for s in layout['sections']),
    'product_no': 24,
    'sections': [{'name': s['name'], 'height': s['height']} for s in layout['sections']],
    'web_source_unchanged': True,
    'assets': [{'file': p.name, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((dest/'assets').iterdir())],
    'figma_status': 'not_uploaded_starter_mcp_limit',
    'figma_file': 'https://www.figma.com/design/EB9W31rgIwrchSEAfbWTNA',
    'figma_import': '9 SVG sections with text/vector layers; motions represented by same-placement stills. Native Figma import not yet verified.',
    'production_cafe24_changed': False,
    'preview_integration': 'Existing product-24 route; isolated responsive full-height iframe, expanded by default. Purchase/options/reviews retained.'
}
(dest/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'assets':len(manifest['assets']), 'bytes':sum(a['bytes'] for a in manifest['assets']), 'sections':len(layout['sections']), 'height':manifest['height']}))
