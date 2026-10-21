"""Connect storefront routes to the current Cafe24 delivery composition.

Only product-detail markup changes. Purchase UI, options, reviews and the
excluded shading duo remain untouched. Run again after updating a package.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = {
    110: ('cafe24-delivery-20261019/cloud-blush', 'cloud-blush-v13'),
    111: ('cafe24-delivery-20261020/powder-balm', 'powder-balm-v5'),
    25: ('cafe24-delivery-20261019/lip-oil', 'lipoil-v9'),
    118: ('cafe24-delivery-20261019/lip-liner', 'lip-liner-r34'),
    102: ('cafe24-delivery-20261019/milky-cheek', 'cheek-v12'),
    24: ('cafe24-delivery-20261019/highlighter', 'highlighter-r33'),
}


class DetailSpan(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.start = self.end = None
        self.tag = None
        self.depth = 0
        self.feed(source)

    def pos(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if self.start is None and dict(attrs).get('id') == 'product-detail':
            self.start, self.tag = self.pos(), tag
        if self.start is not None and self.end is None and tag == self.tag:
            self.depth += 1

    def handle_endtag(self, tag):
        if self.start is not None and self.end is None and tag == self.tag:
            self.depth -= 1
            if self.depth == 0:
                self.end = self.source.index('>', self.pos()) + 1


def compose(package):
    directory = ROOT / package
    source = (directory / 'index.html').read_text(encoding='utf-8')
    body = re.search(r'<body\b[^>]*>(.*?)</body>', source, re.S).group(1)

    def asset(match):
        relative = urlsplit(html.unescape(match.group(1))).path
        path = directory / relative
        assert path.is_file(), path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        return f'src="../../{package}/{relative}?v={digest}"'

    return re.sub(r'src="([^"]+)"', asset, body)


def main():
    for product, (package, release) in PACKAGES.items():
        page = ROOT / f'storefront-v2/preview/product-{product}.html'
        source = page.read_text(encoding='utf-8')
        span = DetailSpan(source)
        assert span.start is not None and span.end is not None, page
        old = source[span.start:span.end]
        body = compose(package)
        if product == 25:
            # Product25 has 00 gloss and 01–03 oils. Keep the existing common
            # series information and all four options; oil is a new component.
            saved = re.search(r'<!-- SERIES-LEGACY-START -->(.*?)<!-- SERIES-LEGACY-END -->', old, re.S)
            legacy = saved.group(1) if saved else re.search(r'<div class="detail-images">(.*?)</div>', old, re.S).group(1)
            body = ('<div style="padding:24px 20px;font:15px/1.7 system-ui,sans-serif;word-break:keep-all;background:#fff">'
                    '<h2 style="font-size:22px;margin:0 0 12px">더 젤리 플럼핑 립 시리즈</h2>'
                    '<p>00 히말라야 핑크는 립 글로스, 01 퍼스트 러브 · 02 인피니트 로즈 · 03 나이트 뷰는 립오일입니다.</p>'
                    '<p><a href="product-18.html#product-detail">00 립 글로스 상세 보기</a></p>'
                    '<h3 style="font-size:18px;margin:20px 0 0">01–03 립오일</h3></div>' + body +
                    '<details style="padding:20px;background:#fff"><summary style="cursor:pointer;font:15px/1.7 system-ui,sans-serif">립 시리즈 공통 안내 · 글로스 포함</summary>'
                    '<div class="detail-images"><!-- SERIES-LEGACY-START -->' + legacy +
                    '<!-- SERIES-LEGACY-END --></div></details>')
        replacement = (f'<section id="product-detail" class="tam-registration-detail" '
                       f'data-detail-release="{release}" data-delivery-package="{package}" '
                       'aria-label="제품 상세" style="width:100%;max-width:860px;margin:48px auto;padding:0;box-sizing:border-box">'
                       + body + '</section>')
        page.write_text(source[:span.start] + replacement + source[span.end:], encoding='utf-8')
        print(f'product-{product}: {release} ({package})')


if __name__ == '__main__':
    main()
