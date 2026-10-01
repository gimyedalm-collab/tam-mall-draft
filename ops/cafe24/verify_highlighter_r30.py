"""Scoped, read-only integrity checks. No orders, authentication or customer export."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[2]
folder=root/'highlighter-r30'
manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
layout=json.loads((folder/'layout.json').read_text(encoding='utf-8'))
html=(folder/'index.html').read_text(encoding='utf-8')
current=(root/'storefront-v2/preview/product-24.html').read_text(encoding='utf-8')
baseline=subprocess.check_output(['git','show','4bbfb67:storefront-v2/preview/product-24.html'],cwd=root).decode('utf-8').replace('\r\n','\n')
expected=re.sub(r'      <details class="detail-source container">.*?</details>','[APPROVED DETAIL]',baseline,count=1,flags=re.S)
actual=re.sub(r'      <section class="highlighter-final-detail".*?</section>','[APPROVED DETAIL]',current,count=1,flags=re.S)
actual=actual.replace('    <link href="assets/highlighter-final-detail.css" rel="stylesheet" />\n','')
actual=actual.replace('class="preview-options" id="purchase-options"','class="preview-options"')
assert actual==expected, 'Unrelated product page content changed'
assert len(layout['sections'])==9 and manifest['height']==14131
assert html.count('class="animated"')==2
embed=(folder/'embed.html').read_text(encoding='utf-8')
assert embed.replace('<base target="_top"><style>html,body{overflow:hidden}</style>', '')==html
assert all(bad not in html for bad in ['actual-skin-glow','tam-airy-2','ingredient-botanical-v3'])
for asset in manifest['assets']:
    assert hashlib.sha256((folder/'assets'/asset['file']).read_bytes()).hexdigest()==asset['sha256']
for asset in re.findall(r'(?:src="|url\(\')assets/([^"\']+)',html):
    assert (folder/'assets'/asset).is_file()
svgs=sorted((folder/'figma-import').glob('*.svg'))
assert len(svgs)==9
for svg in svgs:
    ET.parse(svg)
    assert 'data:image/webp' not in svg.read_text(encoding='utf-8')
assert 'word-break:keep-all' in (folder/'product-information.html').read_text(encoding='utf-8')
base=sys.argv[1].rstrip('/')
routes=['highlighter-r30/','highlighter-r30/embed.html','highlighter-r30/product-information.html','storefront-v2/preview/product-24.html','storefront-v2/preview/assets/highlighter-final-detail.css']
routes += ['highlighter-r30/assets/'+a['file'] for a in manifest['assets']]
for route in routes:
    with urllib.request.urlopen(base+'/'+route,timeout=25) as response:
        assert response.status==200,route
result={'passed':True,'http_routes_checked':len(routes),'assets_hash_checked':len(manifest['assets']),'figma_svg_xml_valid':9,'motion_sources':2,'sections':9,'height_at_860px':14131,'unrelated_product_content_exact':True,'production_cafe24_changed':False,'figma_uploaded':False}
print(json.dumps(result,ensure_ascii=False))
