"""Connect storefront routes to the current Cafe24 delivery composition.

Only product-detail markup changes. Purchase UI, options and reviews remain
untouched. Run again after updating a package. Latest Shading V9 is authorized.
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
    109: ('heart-shading-v9', 'heart-shading-v9'),
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
        # Owner removed the series introduction/link/common accordion on 2026-10-23.
        replacement = (f'<section id="product-detail" class="tam-registration-detail" '
                       f'data-detail-release="{release}" data-delivery-package="{package}" '
                       'aria-label="제품 상세" style="width:100%;max-width:860px;margin:48px auto;padding:0;box-sizing:border-box">'
                       + body + '</section>')
        page.write_text(source[:span.start] + replacement + source[span.end:], encoding='utf-8')
        print(f'product-{product}: {release} ({package})')


if __name__ == '__main__':
    main()
