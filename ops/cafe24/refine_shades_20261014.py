"""Replace fragmented thumbnails; keep source imagery and native option values intact."""
from pathlib import Path
from bs4 import BeautifulSoup
import re, html

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'storefront-v2/preview'
for pid in (23,112,102):
    path = BASE / f'product-{pid}.html'
    text = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(text,'html.parser')
    old = re.search(r'<div class="ux-shades">.*?</div>\s*(?=<label class="field">)',text,re.S).group(0)
    choices = soup.select('[data-preview-product] select option')[1:]
    tones = {
        23:['쿨 · 17호','쿨 · 21호','뉴트럴 · 21호','웜 · 23호','뉴트럴 · 25호','웜 · 27호'],
        112:['쿨 · 밀키 핑크','쿨 · 버블 핑크','쿨 · 모브 로즈','쿨 · 플럼 레드','웜 · 누디 베이지','웜 · 코랄 레드','웜 · 브라이트 레드','웜 · 코랄 브라운'],
        102:[e.get_text(strip=True) for e in soup.select('.c12-tone')]
    }[pid]
    buttons = ''.join(f'<button class="ux-shade-button" type="button" data-option-index="{i}" aria-pressed="false"><span>{html.escape(o.get_text(strip=True))}</span><small>{tones[i-1]}</small></button>' for i,o in enumerate(choices,1))
    if pid == 102:
        reference = '<div class="ux-reference-cheeks">'+''.join(f'<figure><figcaption>{html.escape(o.get_text(strip=True))}</figcaption><img src="assets/milky-cheek-v11/cheek{i:02d}.jpg" width="2992" height="3740" alt="{html.escape(o.get_text(strip=True))} 볼 발색"/><img src="assets/milky-cheek-v12/swatch{i:02d}.jpg" width="840" height="840" alt="{html.escape(o.get_text(strip=True))} 제형"/></figure>' for i,o in enumerate(choices,1))+'</div>'
    else:
        src,w,h = ('assets/jelly-skin-cushion-0908/04.jpg',860,4200) if pid==23 else ('assets/ux-261013/tint-original-color-chart.jpg',840,5380)
        reference = f'<img src="{src}" width="{w}" height="{h}" alt="브랜드 원본 컬러 비교표"'+(' data-start-ratio="0.44"' if pid==23 else '')+'/>'
    new = f'<div class="ux-shades"><fieldset><legend>컬러 선택</legend><div class="ux-shade-grid">{buttons}</div></fieldset><button class="ux-compare-open" type="button" aria-haspopup="dialog">발색 크게 비교하기 <span aria-hidden="true">↗</span></button><p aria-live="polite" class="ux-shade-selected">컬러를 선택해 주세요.</p><p class="ux-shade-note">피부 톤·사용량·화면 환경에 따라 발색이 다르게 보일 수 있습니다.</p><template class="ux-shade-reference">{reference}</template></div>'
    assert old in text
    text=text.replace(old,new,1)
    path.write_text(text,encoding='utf-8')
for path in BASE.glob('*.html'):
    text=path.read_text(encoding='utf-8')
    revised=re.sub(r'(assets/ux-261013\.(?:css|js))\?v=1',r'\1?v=2',text)
    if revised!=text:path.write_text(revised,encoding='utf-8')
