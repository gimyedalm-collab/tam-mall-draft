"""Verify copy/typography and the requested HOW TO source replacement."""
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[2]
path = 'highlighter-r32/layout.json'
old = json.loads(subprocess.check_output(['git', 'show', f'04b9b15:{path}'], cwd=root))
new = json.loads((root / path).read_text(encoding='utf-8'))
for before, after in zip(old['sections'], new['sections']):
    assert before['name'] == after['name']
    if after['name'] != 'how-to':
        assert before['height'] == after['height']
    media = lambda s: [e for e in s['elements'] if e['type'] in ('image', 'vector')]
    if after['name'] != 'how-to':
        assert media(before) == media(after), before['name']
    else:
        assert [e['file'] for e in media(after)] == ['howto-touch-261012.jpg']
        assert after['height'] == 1190
    if after['name'] in ('shades', 'how-to'):
        assert not any(e['type'] == 'rect' and e['w'] == 5 for e in after['elements'])
    if after['name'] == 'information':
        assert before == after
for name in ('index.html', 'embed.html'):
    text = (root / 'highlighter-r32' / name).read_text(encoding='utf-8')
    assert text.count('<video ') == 2
    assert '입체적인 광채' in text
    assert 'howto-touch-261012.jpg' in text
    assert 'assets/application.jpg' not in text
    assert 'assets/nose-detail.jpg' not in text
    assert '어떤 빛으로 마무리할까요?' not in text
    assert '비건 포뮬러' in text
commerce = 'storefront-v2/preview/product-24.html'
assert (root / commerce).read_bytes().replace(b'\r\n', b'\n') == subprocess.check_output(
    ['git', 'show', f'HEAD:{commerce}'], cwd=root).replace(b'\r\n', b'\n')
height = sum(s['height'] for s in new['sections'])
assert f'aspect-ratio:860/{height}' in (root / 'storefront-v2/preview/assets/highlighter-final-detail.css').read_text()
print('PASS: HOW TO source replaced; other media and commerce preserved; no decorative bars; iframe height matches.')
