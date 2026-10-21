"""Owner-directed copy, type, oil and vegan cleanup; preserve original evidence."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2]; OLD=ROOT/'cloud-blush-v11'; OUT=ROOT/'cloud-blush-v12'
OUT.mkdir(exist_ok=True); (OUT/'assets').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=BeautifulSoup((OLD/'detail.template.html').read_text(encoding='utf-8'),'html.parser')
copy=[('핑크에 더해진','부드러운 코랄'),('로즈와 핑크의','차분한 조화'),('핑크에 살짝','섞인 라벤더'),('오렌지빛을 더한','따뜻한 코랄'),('붉은 기가 도는','또렷한 핑크'),('베이지에 스민','은은한 피치')]
for n,lines in enumerate(copy,1):
    p=s.select_one(f'#face-{n} .tone');p.clear();p.append(lines[0]);p.append(s.new_tag('br'));p.append(lines[1])
f=s.select_one('#formula');f.clear()
f.append(BeautifulSoup('''<header class="heading"><h2>네 가지 식물성 오일 함유</h2><p>살구씨오일 · 동백나무씨오일<br>올리브오일 · 서양자두씨오일</p></header><figure class="oil-still"><img src="../cloud-blush-v6/assets/formula-clear-oil-261019.jpg" alt="식물성 오일 함유를 표현한 오일 연출 이미지"></figure>''','html.parser'))
v=s.select_one('#vegan');v.clear()
v.append(BeautifulSoup('''<header class="heading"><h2>탐뷰티의 비건 포뮬러</h2></header><div class="vegan-mark" role="img" aria-label="VEGAN FORMULA — 브랜드 비건 포뮬러 표기"><svg viewBox="0 0 72 64" aria-hidden="true"><path d="M36 57V31M36 41C18 41 12 28 14 15C28 14 39 22 36 41ZM36 33C33 17 44 8 60 8C60 23 51 34 36 33Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><span>VEGAN</span><span class="mark-sub">FORMULA</span></div>''','html.parser'))
# This typographic brand symbol is not a third-party certification logo.
body=str(s)
(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V12 컬러 설명과 소재 정리</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
css=(OLD/'detail.css').read_text(encoding='utf-8')
css=css.replace('font-size:34px','font-size:28px').replace('font-size:32px','font-size:24px').replace('font-size:26px','font-size:24px')
css='\n'.join(l for l in css.splitlines() if not l.startswith('.vegan{') and not l.startswith('.formula{'))
css+='''
/* V12 type roles: hero28, section24, shade18, body17, labels16.2. */
.hero h2{line-height:1.45;margin-top:20px}.heading h2,.intro h2,.texture .heading h2{font-weight:600;line-height:1.4}
.face-row figcaption{display:flex;flex-direction:column;justify-content:center;padding:10px}.face-row .tone{margin-top:8px;line-height:1.4}
.formula{background:#fbfaf9;padding:0 0 28px}.formula .heading{padding:38px 24px 8px}.formula .heading h2{font-size:24px}.formula .heading p{font-size:16.2px;line-height:1.6;margin-top:14px;color:#756679}
.oil-still{width:100%;height:244px;overflow:hidden}.oil-still img{width:100%;height:100%;object-fit:cover;object-position:center}
.vegan{background:#f3eef3;padding:0 24px 34px}.vegan .heading{padding:34px 0 22px}.vegan-mark{color:#756679;display:flex;flex-direction:column;align-items:center;gap:5px}.vegan-mark svg{width:62px;height:55px;margin-bottom:5px}.vegan-mark>span{font:500 24px/1.2 Manrope,sans-serif;letter-spacing:.12em;padding-left:.12em}.vegan-mark .mark-sub{font-size:16.2px;letter-spacing:.2em;padding-left:.2em}
'''
css=css.replace('#756679','#6d5e70')
(OUT/'detail.css').write_text(css,encoding='utf-8')
for name in ['product-information.html','motion-provenance.json']:
    shutil.copy2(OLD/name,OUT/name)
shutil.copy2(OLD/'assets/cream-spread-finish.gif',OUT/'assets/cream-spread-finish.gif')
assets=[]
for im in s.select('img'):
    path=(OUT/im['src']).resolve();assets.append(dict(file=im['src'],sha256=sha(path),role='existing oil illustration restored, no product overlay' if 'formula-clear-oil' in str(path) else 'unchanged original/previous asset'))
(OUT/'asset-provenance.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
plan=dict(version=12,scope='Owner 2026-10-21: helpful shade descriptions; smaller consistent type; oil-only image restored; vegan mark only',shade_copy=[dict(shade=n+1,description=' '.join(c),basis='Editorial visual description of supplied wrist/texture/cheek images; not measured colour or personal-colour advice') for n,c in enumerate(copy)],type_css_px=dict(hero=28,section=24,shade=18,body=17,label=16.2,native_information=12),vegan=dict(basis='Owner brand claim and existing vegan wording',graphic='New simple botanical VEGAN FORMULA typography, not third-party certification',certification='Current certificate/authorized logo for Cloud blush not found in inspected local evidence; no certification claim'),oil=dict(asset='../cloud-blush-v6/assets/formula-clear-oil-261019.jpg',role='Existing illustrative oil visual; not a photograph of raw materials or product texture',facts='Four oil names present in each of six INCI lists'),preserved=['All six actual wrist, texture and first-revision cheek sources, without recolouring','V11 unified cream/application GIF byte-identical','Native product information and INCI byte-identical'],cafe24_upload='deferred_by_owner')
(OUT/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V12 source and evidence plan built.')
