"""Use the alternate original cushion photograph without recoloring or resampling."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('C:/Users/BNK-1/Desktop/_탐뷰티/PROSTER_젤리라인_SNS소스_260916/05_Product_Cuts/04_Skin_Cushion/cutout_png/탐_용기_쿠션 (2).png')
NAME = 'cushion-pink-original-2.png'
image = Image.open(SOURCE)
width, height = image.size
left, top, right, bottom = image.getchannel('A').getbbox()
bw, bh = right-left, bottom-top
for folder in ('storefront-v2/preview', 'storefront-v2/cafe24/tam'):
    base = ROOT/folder
    shutil.copy2(SOURCE, base/'assets'/NAME)
    for path in [*base.rglob('*.html'), *base.rglob('*.js')]:
        if path.name == 'design-before-balance.html':
            continue
        old = path.read_text(encoding='utf-8')
        new = old.replace('packshot-23.png', NAME).replace('retouched-23-v1.png', NAME)
        def dimensions(match):
            tag = match.group(0)
            if NAME not in tag:
                return tag
            tag = re.sub(r'\bwidth="\d+"', f'width="{width}"', tag)
            return re.sub(r'\bheight="\d+"', f'height="{height}"', tag)
        new = re.sub(r'<img\b[^>]*>', dimensions, new)
        if path.name != 'design-before-balance.html':
            new = re.sub(r'assets/retouched-objects\.css(?:\?v=[^"\s]+)?',
                         'assets/retouched-objects.css?v=cushion2', new)
            if path.suffix == '.html':
                for script in ('tam.js', 'preview-catalog.js'):
                    new = re.sub(re.escape('assets/' + script) + r'(?:\?v=[^"\s]+)?',
                                 'assets/' + script + '?v=cushion2', new)
        if new != old:
            path.write_text(new, encoding='utf-8')
css = ROOT/'storefront-v2/preview/assets/retouched-objects.css'
rules = css.read_text(encoding='utf-8').splitlines()
rules[0] = (f'.object-23{{aspect-ratio:{bw}/{bh};--object-x:0%;--object-y:0%}}'
    f'.object-23 img{{width:{width/bw*100:.6f}%;left:{-left/bw*100:.6f}%;top:{-top/bh*100:.6f}%}}')
css.write_text('\n'.join(rules)+'\n', encoding='utf-8')
provenance = ROOT/'design-retouch-provenance.json'
data = json.loads(provenance.read_text(encoding='utf-8'))
data['23'] = {
    'asset': NAME, 'size': [width, height], 'visible_bbox': [left, top, right, bottom],
    'source': str(SOURCE), 'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'alpha': 'Original supplied PNG alpha, unchanged',
    'editing': 'Byte-identical source copy. No AI retouch, hue adjustment, or browser color filter.',
    'status': 'Alternate original (2) selected for review after user identified similar 1/2 source cuts',
    'previous_asset': 'retouched-23-v1.png'
}
provenance.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Copied original {NAME}: {width}x{height}; alpha bbox {left,top,right,bottom}')
