"""Verify public candidate assets, recording Cafe24 JPEG recompression explicitly."""
import argparse, hashlib, io, json, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
from PIL import Image, ImageCms

parser = argparse.ArgumentParser()
parser.add_argument('--stage', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
pattern = re.compile(r'inner-card-\d+-(480|800)\.png|inner-lookbook-(cloud|jelly)-[123]-(960|1600)\.jpg|candidate-inner-261022-v4\.(css|js)')

def verify(path):
    original = path.read_bytes()
    with urlopen('https://awiz.cafe24.com/tam-detail-20261022/' + path.name, timeout=45) as response:
        public = response.read()
        result = dict(file=path.name, status=response.status, source_bytes=len(original), public_bytes=len(public), byte_identical=original == public)
    result['public_sha256'] = hashlib.sha256(public).hexdigest()
    if path.suffix in ('.png', '.jpg'):
        with Image.open(io.BytesIO(original)) as a, Image.open(io.BytesIO(public)) as b:
            profile = a.info.get('icc_profile')
            profile_name = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(profile))).strip() if profile else None
            result.update(dimensions=list(b.size), same_dimensions=a.size == b.size,
                          decoded_pixels_identical=a.convert('RGBA').tobytes() == b.convert('RGBA').tobytes(),
                          icc_identical=profile == b.info.get('icc_profile'), source_profile=profile_name,
                          standard_srgb_profile_removed=profile_name == 'sRGB IEC61966-2.1' and not b.info.get('icc_profile'))
        result['platform_recompressed'] = path.suffix == '.jpg' and not result['decoded_pixels_identical']
        result['passed'] = result['same_dimensions'] and (path.suffix == '.jpg' or (result['decoded_pixels_identical'] and (result['icc_identical'] or result['standard_srgb_profile_removed'])))
    else:
        result['passed'] = result['byte_identical']
    return result

files = sorted(p for p in args.stage.iterdir() if pattern.fullmatch(p.name))
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(verify, files))
report = dict(expected=42, checked=len(results), passed=len(results) == 42 and all(r['passed'] for r in results),
              note='Display derivatives only; masters preserved. JPEG pass checks availability/dimensions, not pixel fidelity. PNG pass requires identical decoded pixels and either identical ICC or explicitly recorded standard sRGB removal (untagged web images use sRGB). No wide-gamut profile removal is accepted.', results=results)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k != 'results'}))
raise SystemExit(0 if report['passed'] else 1)
