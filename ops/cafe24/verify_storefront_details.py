"""Verify current delivery bytes, ordering, exclusions and purchase UI preservation."""
import hashlib
import json
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup
from sync_storefront_details import ROOT, PACKAGES, DetailSpan

BASELINE = '363d346'
rows = []
for number, (package, release) in PACKAGES.items():
    path = f'storefront-v2/preview/product-{number}.html'
    before = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=ROOT).decode().replace('\r\n', '\n')
    after = (ROOT / path).read_text(encoding='utf-8')
    a, b = DetailSpan(before), DetailSpan(after)
    assert before[:a.start] + before[a.end:] == after[:b.start] + after[b.end:], path
    detail = BeautifulSoup(after[b.start:b.end], 'html.parser')
    manifest = json.loads((ROOT / package / 'manifest.json').read_text(encoding='utf-8'))
    files = manifest.get('files', manifest.get('media'))
    images = detail.find_all('img')
    assert len(images) == len(files) + (4 if number == 25 else 0)
    for image, item in zip(images, files):
        asset = (ROOT / path).parent / image['src'].split('?')[0]
        assert asset.is_file(), asset
        assert asset.name == Path(item['file']).name
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == item['sha256'], asset
    assert not detail.select('script, video, iframe, link')
    rows.append({'product': number, 'release': release, 'package': package,
                 'media_count': len(files), 'manifest_order_and_hashes_match': True,
                 'outside_detail_identical_after_newline_normalization': True})
excluded = 'storefront-v2/preview/product-109.html'
assert not subprocess.check_output(['git', 'diff', BASELINE, '--', excluded], cwd=ROOT)
report = {'date': '2026-10-21', 'baseline': BASELINE,
          'scope': 'GitHub storefront integration; live Cafe24 upload remains deferred',
          'excluded_product': 109, 'excluded_product_unchanged': True,
          'products': rows,
          'lip_series': 'All four preview options and original common-series images retained. Oils-only component is explicitly scoped to01-03, with00 gloss detail link.',
          'main_film': 'V16 already connected; unchanged',
          'owner_visual_acceptance': 'Not inferred from integration QA'}
destination = ROOT / 'ops/cafe24/main-sync-20261021.json'
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
