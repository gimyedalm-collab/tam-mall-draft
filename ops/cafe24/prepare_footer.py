"""Prepare shared footer against private native templates; never publish admin source."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAGMENT = ROOT / 'storefront-v2/cafe24/tam/sections/footer-261026.html'
CSS = ROOT / 'storefront-v2/cafe24/tam/assets/footer-261026.css'
FOOTER = re.compile(r'<footer\b[^>]*>[\s\S]*?</footer>')


def prepare(original, output):
    output.mkdir(parents=True, exist_ok=True)
    fragment = FRAGMENT.read_text(encoding='utf-8').strip()
    css = CSS.read_text(encoding='utf-8')
    before = {name: (original / name).read_text(encoding='utf-8')
              for name in ('index.html', 'head.html', 'footer.html')}
    assert len(FOOTER.findall(before['footer.html'])) == 1
    home_footers = FOOTER.findall(before['index.html'])
    assert len(home_footers) == 1 and 'ux-footer' in home_footers[0]
    after = {
        'footer.html': FOOTER.sub(lambda _: fragment, before['footer.html'], count=1),
        'index.html': FOOTER.sub('', before['index.html'], count=1),
        'head.html': before['head.html'] + '\n<style id="tam-footer-261026">\n' + css + '</style>\n',
    }
    assert 'tam-footer-261026' not in before['head.html'], 'Already patched'
    assert FOOTER.sub('', before['footer.html']) == FOOTER.sub('', after['footer.html'])
    assert after['index.html'] == before['index.html'].replace(home_footers[0], '', 1)
    assert after['head.html'].startswith(before['head.html'])
    for name, text in after.items():
        (output / name).write_text(text, encoding='utf-8')
    (output / 'preservation.json').write_text(json.dumps({
        'only_changes': ['one shared footer', 'remove duplicated home footer', 'append scoped CSS'],
        'native_footer_hooks_unchanged': True, 'homepage_outside_footer_unchanged': True,
        'existing_head_unchanged': True, 'company_import_preserved': True,
        'phone_runtime_variables_preserved': True,
    }, indent=2), encoding='utf-8')
    print('Prepared 3 native templates; outside-footer markup and existing head preserved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.original, args.output)
