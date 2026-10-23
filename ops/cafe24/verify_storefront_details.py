"""Verify current delivery bytes, ordering, exclusions and purchase UI preservation."""
import hashlib
import json
import re
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup
from sync_storefront_details import ROOT, PACKAGES, DetailSpan

BASELINE = '363d346'

def normalize_cache(source):
    # Mobile fixes only change these shared-resource cache revisions outside
    # the detail. Keep all other markup comparisons strict.
    return re.sub(r'(assets/(?:ux-261013\.css|reviews\.(?:css|js)|purchase-(?:policy|experience)\.js))\?v=[^"\s>]+', r'\1', source)

rows = []
for number, (package, release) in PACKAGES.items():
    path = f'storefront-v2/preview/product-{number}.html'
    before = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=ROOT).decode().replace('\r\n', '\n')
    after = (ROOT / path).read_text(encoding='utf-8')
    a, b = DetailSpan(before), DetailSpan(after)
    assert normalize_cache(before[:a.start] + before[a.end:]) == normalize_cache(after[:b.start] + after[b.end:]), path
    detail = BeautifulSoup(after[b.start:b.end], 'html.parser')
    manifest = json.loads((ROOT / package / 'manifest.json').read_text(encoding='utf-8'))
    files = manifest.get('files', manifest.get('media', manifest.get('images')))
    images = detail.find_all('img')
    assert len(images) == len(files)
    for image, item in zip(images, files):
        asset = (ROOT / path).parent / image['src'].split('?')[0]
        assert asset.is_file(), asset
        assert asset.name == Path(item['file']).name
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == item['sha256'], asset
    assert not detail.select('script, video, iframe, link')
    rows.append({'product': number, 'release': release, 'package': package,
                 'media_count': len(files), 'manifest_order_and_hashes_match': True,
                 'outside_detail_identical_after_newline_and_shared_cache_normalization': True})
report = {'date': '2026-10-21', 'baseline': BASELINE,
          'scope': 'Seven current product deliveries; owner authorized latest Shading V9 integration. Cafe24 rollout awaits actual readiness verification.',
          'products': rows,
          'lip_series': 'Owner removed series introduction/link/common accordion on2026-10-23. All four options remain unchanged; seven approved oil panels retained.',
          'main_film': 'V16 already connected; unchanged',
          'owner_visual_acceptance': 'Not inferred from integration QA'}
destination = ROOT / 'ops/cafe24/storefront-details-verification.json'
existing = json.loads(destination.read_text(encoding='utf-8')) if destination.exists() else {}
existing.pop('excluded_product_unchanged', None)
existing.update(report)
destination.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
