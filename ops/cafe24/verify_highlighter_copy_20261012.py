"""Verify the copy-only revision without changing product imagery or commerce."""
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[2]
path = 'highlighter-r32/layout.json'
old = json.loads(subprocess.check_output(['git', 'show', f'HEAD:{path}'], cwd=root))
new = json.loads((root / path).read_text(encoding='utf-8'))
for before, after in zip(old['sections'], new['sections']):
    assert before['name'] == after['name']
    assert before['height'] == after['height']
    media = lambda s: [e for e in s['elements'] if e['type'] in ('image', 'vector')]
    assert media(before) == media(after), before['name']
    if after['name'] in ('shades', 'how-to'):
        assert not any(e['type'] == 'rect' and e['w'] == 5 for e in after['elements'])
    if after['name'] == 'information':
        assert before == after
for name in ('index.html', 'embed.html'):
    text = (root / 'highlighter-r32' / name).read_text(encoding='utf-8')
    assert text.count('<video ') == 2
    assert '쓱, 바르고 톡톡' in text
    assert '어떤 빛으로 마무리할까요?' not in text
    assert '비건 포뮬러' in text
commerce = 'storefront-v2/preview/product-24.html'
assert (root / commerce).read_bytes().replace(b'\r\n', b'\n') == subprocess.check_output(
    ['git', 'show', f'HEAD:{commerce}'], cwd=root).replace(b'\r\n', b'\n')
print('PASS: source photos, films, section heights, product information and commerce unchanged; copy updated; four decorative bars removed.')
