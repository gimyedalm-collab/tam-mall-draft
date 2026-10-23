"""Package the current cushion composition for native Cafe24 product23 HTML.

Static assets stay unchanged. Existing video transcodes are hosted on GitHub
Pages and use native controls, without a custom JavaScript dependency.
"""
import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / 'storefront-v2/preview'
REMOTE = 'https://awiz.cafe24.com/tam-detail-20261022/'
PAGES = 'https://gimyedalm-collab.github.io/tam-mall-draft/storefront-v2/preview/'


def build(output):
    upload = output / 'upload-lossless'
    upload.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup((PREVIEW / 'product-23.html').read_text(encoding='utf-8'), 'html.parser')
    detail = soup.select_one('.cushion-final-detail .detail-images')
    records = []
    pieces = ['<div data-tam-cushion-version="261023" style="width:100%;max-width:860px;margin:0 auto;font-size:0;line-height:0;background:#fff">']

    def asset(relative):
        source = PREVIEW / relative
        target = 'p23-261023-' + source.stem + '.png'
        with Image.open(source) as im:
            width, height = im.size
            if source.suffix.lower() == '.jpg':
                im.save(upload / target, format='PNG', optimize=True, icc_profile=im.info.get('icc_profile'))
            else:
                shutil.copyfile(source, upload / target)
        records.append({'file': target, 'source': relative, 'width': width, 'height': height,
                        'bytes': (upload / target).stat().st_size,
                        'sha256': hashlib.sha256((upload / target).read_bytes()).hexdigest(),
                        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        return REMOTE + target, width, height

    for index, child in enumerate(detail.find_all(['img', 'figure'], recursive=False)):
        if child.name == 'img':
            url, width, height = asset(child['src'])
            loading = 'fetchpriority="high" loading="eager"' if index == 0 else 'loading="lazy"'
            pieces.append(f'<img src="{url}" width="{width}" height="{height}" alt="{html.escape(child.get("alt", "더 젤리 스킨 쿠션"), quote=True)}" {loading} decoding="async" style="display:block;width:100%;max-width:100%;height:auto;margin:0;border:0"/>')
        else:
            video = child.video
            poster, width, height = asset(video['poster'])
            relative = video.source['src']
            source = PREVIEW / relative
            records.append({'video': PAGES + relative, 'source': relative, 'bytes': source.stat().st_size,
                            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'hosting': 'existing GitHub Pages'})
            pieces.append(f'<video controls muted playsinline loop preload="none" poster="{poster}" width="{width}" height="{height}" aria-label="쿠션 사용 영상" style="display:block;width:100%;max-width:100%;height:auto;margin:0;background:#fff"><source src="{PAGES + relative}" type="video/mp4"/><a href="{PAGES + relative}">쿠션 사용 영상 보기</a></video>')
    pieces.append('</div>')
    result = '\n'.join(pieces) + '\n'
    (output / 'product-23-ready.html').write_text(result, encoding='utf-8')
    public = ROOT / 'storefront-v2/cafe24/tam/sections/cushion-detail-261023.html'
    public.write_text(result, encoding='utf-8')
    manifest = {'product_no': 23, 'source': 'current product-23 preview: vegan-261002 + ux-261013',
                'status': 'prepared_not_yet_uploaded', 'custom_javascript': False,
                'external_video_hosting': True, 'maximum_css_width': 860,
                'static_image_count': 10, 'video_count': 3, 'assets': records}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'uploads': len(list(upload.iterdir())), 'upload_bytes': sum(p.stat().st_size for p in upload.iterdir()), 'videos': 3}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    build(parser.parse_args().output)
