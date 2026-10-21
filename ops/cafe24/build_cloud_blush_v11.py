"""Unite texture and usage, and remove the oil/product composite."""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[2]; OLD=ROOT/'cloud-blush-v10'; OUT=ROOT/'cloud-blush-v11'
OUT.mkdir(exist_ok=True)
s=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
texture=s.select_one('#texture');texture.clear()
texture.append(BeautifulSoup('''<header class="heading export-panel"><p class="eyebrow">CREAM TO POWDER</p><h2>크림처럼 펴 바르고,<br>파우더처럼 보송하게.</h2></header>
<div class="motion-wrap export-motion" data-gif="assets/cream-spread-finish.gif"><img src="assets/cream-spread-finish.gif" alt="크림 제형을 덜고 손에 얇게 펴 바른 뒤, 손가락이 지나간 도포 표면을 보여주는 실제 촬영 편집"></div>
<div id="application" class="application export-panel"><p class="motion-caption note">실제 제형·도포 장면을 연결한 영상입니다.</p><p>손끝이나 도구로 얇게 펴 바른 뒤,<br>경계를 가볍게 두드려 주세요.</p></div>''','html.parser'))
s.select_one('#howto').decompose()
formula=s.select_one('#formula');formula.clear()
formula.append(BeautifulSoup('''<div class="formula-summary"><h2>네 가지 식물성 오일 함유</h2><p>살구씨오일 · 동백나무씨오일<br>올리브오일 · 서양자두씨오일</p></div>''','html.parser'))
formula.name='div';texture.append(formula.extract())
body=str(s)
(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V11 제형과 사용법 연결</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
css=(OLD/'detail.css').read_text(encoding='utf-8')
lines=[]
for line in css.splitlines():
    if line.startswith('.formula{') or line.startswith('.howto{'):continue
    lines.append(line)
lines.extend([
    '.texture{background:#faf6f7}.texture .heading{padding:50px 24px 28px}.texture .heading h2{font-size:32px}.texture .motion-wrap{background:#faf6f7}.application{padding:16px 24px 28px;background:#faf6f7}.application p{font-size:17px;line-height:1.6;letter-spacing:-.02em}.application .motion-caption{font-size:16.2px;line-height:1.5;margin-bottom:18px;color:#756679}',
    '.formula{background:#faf6f7;padding:0 30px 34px}.formula-summary{border-top:1px solid #ded4df;padding-top:18px}.formula h2{font-size:18px;line-height:1.4;font-weight:500;letter-spacing:-.035em;color:#57475b}.formula p{font-size:16.2px;line-height:1.6;color:#756679;margin-top:8px}'
])
(OUT/'detail.css').write_text('\n'.join(lines)+'\n',encoding='utf-8')
shutil.copy2(OLD/'product-information.html',OUT/'product-information.html')
prior=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
for sel in ['#hero','#introduction','#palette','#faces','#vegan','#check','[data-tam-product-info]']:
    assert str(s.select_one(sel))==str(prior.select_one(sel)),sel
assert not s.select('#howto,.oil-still,.oil-product')
assert len(s.select('#texture .export-motion'))==1
assert len(s.select('.export-motion'))==1
provenance=[]
for im in s.select('img'):
    f=(OUT/im['src']).resolve()
    provenance.append({'file':im['src'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'role':'new editorial GIF, see motion-provenance.json' if 'cream-spread-finish' in f.name else 'unchanged prior asset'})
(OUT/'asset-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf-8')
print('V11 unified texture/application section built; oil composite removed.')
