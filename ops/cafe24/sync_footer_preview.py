"""Keep GitHub preview footer aligned with the native Cafe24 composition."""
import re
import shutil
from prepare_footer import ROOT, FRAGMENT, CSS, FOOTER

PREVIEW = ROOT / 'storefront-v2/preview'


def main():
    # Static public shop details in the preview; live uses Cafe24 company_info import.
    company = (ROOT / 'storefront-v2/cafe24/tam/sections/footer-company-preview.html').read_text(encoding='utf-8')
    fragment = FRAGMENT.read_text(encoding='utf-8').strip()
    fragment = fragment.replace(' module="Layout_footer"', '')
    fragment = fragment.replace('<!--@import(/moa/import/footer/company_info.html)-->', company)
    fragment = fragment.replace('{$phone}', '1668-0868').replace('{$runtime}', '평일 오전 10:00시 ~ 17:00시')
    fragment = fragment.replace('https://awiz.cafe24.com/tam-detail-20261022/inner-38d19c7e8e86.png', 'assets/38d19c7e8e86.png')
    fragment = fragment.replace('href="/"', 'href="index.html"').replace('href="/about.html"', 'href="about.html"')
    fragment = re.sub(r'href="(/[^\"]+)"', r'href="https://tambeauty.kr\1"', fragment)
    count = 0
    for path in sorted(PREVIEW.glob('*.html')):
        original = path.read_text(encoding='utf-8')
        old = FOOTER.findall(original)
        if len(old) != 1 or not ('ux-footer' in old[0] or 'tam-site-footer' in old[0]):
            continue
        result = original.replace(old[0], fragment, 1)
        if 'assets/footer-261026.css' not in result:
            result = result.replace('</head>', '<link rel="stylesheet" href="assets/footer-261026.css"></head>', 1)
        path.write_text(result, encoding='utf-8')
        count += 1
    shutil.copyfile(CSS, PREVIEW/'assets/footer-261026.css')
    print(f'{count} preview footers synchronized; page bodies unchanged.')


if __name__ == '__main__':
    main()
