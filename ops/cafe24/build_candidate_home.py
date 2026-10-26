"""Build skin21 homepage from the approved preview; original skin stays outside Git."""
import argparse
import json
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
ASSET_URL = 'https://awiz.cafe24.com/tam-detail-20261022/'
FILM_URL = 'https://gimyedalm-collab.github.io/tam-mall-draft/storefront-v2/preview/assets/tam-main-film-v16-261013.mp4'


def build(original, output):
    preview = ROOT / 'storefront-v2/preview'
    output.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup((preview / 'design-only.html').read_text(encoding='utf-8'), 'html.parser')
    paths = {
        'index.html': '/', 'shop.html': '/product/list.html?cate_no=74',
        'lookbook.html': '/board/gallery/list.html?board_no=8', 'about.html': '/about.html',
        'jelly.html': '/product/list.html?cate_no=74&tam_collection=jelly',
        'cloud.html': '/product/list.html?cate_no=74&tam_collection=cloud',
        'login.html': '/member/login.html', 'search.html': '/product/search.html',
        'basket.html': '/order/basket.html',
    }
    for script in soup.select('script[src]'):
        if Path(script['src'].split('?')[0]).name in ('purchase-policy.js', 'purchase-experience.js', 'ux-261013.js'):
            script.decompose()
    files = set()
    for el in soup.find_all(True):
        for attr in ('href', 'src', 'poster'):
            val = el.get(attr, '')
            if val.startswith('assets/'):
                name = val.split('?')[0][7:]
                if name.endswith('.mp4'):
                    el[attr] = FILM_URL
                else:
                    target = 'home-' + name
                    shutil.copyfile(preview / 'assets' / name, output / target)
                    files.add(target)
                    el[attr] = ASSET_URL + target
        if el.name == 'a':
            val = el.get('href', '')
            match = re.fullmatch(r'product-(\d+)\.html', val)
            if match:
                el['href'] = f'/skin-skin21/product/detail.html?product_no={match[1]}'
                if 'do-product' in el.get('class', []):
                    el['data-native-product'] = match[1]
                    el.select_one('.ux-product-price').string = '상품에서 가격 확인'
            elif val in paths:
                el['href'] = '/skin-skin21' + paths[val]
            elif val.startswith('https://tambeauty.kr/'):
                el['href'] = val.replace('https://tambeauty.kr', '/skin-skin21').replace('/member/agreement.html', '/member/mall_agreement.html')
    # Preserve the native floating Kakao button; never load the preview substitute.
    js = output / 'home-design-only.js'
    js.write_text(js.read_text(encoding='utf-8').split('/* 전 페이지 공통:')[0], encoding='utf-8')
    css = output / 'home-design-only.css'
    css.write_text(css.read_text(encoding='utf-8').replace("url('PretendardVariable.woff2')", "url('home-PretendardVariable.woff2')"), encoding='utf-8')
    main = soup.body.find('main')
    main.name = 'div'
    main['id'] = 'tam-home-main'
    soup.select_one('.ux-skip')['href'] = '#tam-home-main'
    # The native layout supplies one shared footer.
    footer = soup.select_one('#tam-site-footer, .ux-footer')
    if footer:
        footer.decompose()
    app_source = original.read_text(encoding='utf-8')
    snap = app_source[app_source.index('<!-- snap common  start'):]
    # Owner removed the repetitive homepage review section on 2026-10-23.
    # Preserve Snap common scripts and product-specific review mappings.
    extras = ROOT / 'storefront-v2/cafe24/tam/assets'
    for name in ('candidate-home-261022.css', 'candidate-home-261022.js'):
        target = name.replace('.css', '-v4.css')
        shutil.copyfile(extras / name, output / target)
        files.add(target)
    head = '\n'.join(str(x) for x in soup.head.find_all(['link', 'script']))
    body = '\n'.join(str(x) for x in soup.body.contents)
    result = '<!--@layout(/layout/basic/main.html)-->\n<script>document.body.classList.add("home-film","tam-candidate-home");</script>\n'
    result += head + '\n<link rel="stylesheet" href="' + ASSET_URL + 'candidate-home-261022-v4.css">\n'
    result += '<script defer src="' + ASSET_URL + 'candidate-home-261022.js"></script>\n' + body + '\n' + snap
    (output / 'candidate-index.html').write_text(result, encoding='utf-8')
    (output / 'home-upload-manifest.json').write_text(json.dumps({'files': sorted(files), 'film_url': FILM_URL, 'candidate': 'skin21', 'original_source': 'local-only backup', 'index_file': 'candidate-index.html'}, indent=2), encoding='utf-8')
    print(f'{len(files)} assets; {len(result)} HTML characters; skin21 only')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.original, args.output)
