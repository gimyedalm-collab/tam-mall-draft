"""Build the authorized cloud blush V2 from reviewed, original-source assets."""
from pathlib import Path
import re, shutil

repo=Path(__file__).resolve().parents[2]
v1=repo/'cloud-blush-v1'
review=repo/'cloud-blush-review'
out=repo/'cloud-blush-v2'
assets=out/'assets'
assets.mkdir(parents=True,exist_ok=True)
for name in ['PretendardVariable.woff2','ManropeVariable.ttf','tam-logo.svg','ending.jpg']+[f'{kind}-{i}.jpg' for kind in ('cheek','swatch') for i in range(1,7)]:
    shutil.copyfile(v1/'assets'/name,assets/name)
for old,new in [('P03.jpg','hero-cloud.jpg'),('moa-blush.jpg','moa-blush.jpg'),('cream-to-powder-sequence-r2.mp4','cream-to-powder.mp4'),('sequence-poster-r2.jpg','cream-to-powder-poster.jpg')]:
    shutil.copyfile(review/'assets'/old,assets/new)

markup=(v1/'detail.template.html').read_text(encoding='utf8')
markup=markup.replace('볼 위에 부드럽게,<br>생기는 보송하게.','크림처럼 부드럽게,<br>파우더처럼 보송하게.')
markup=markup.replace('크림처럼 펴 바르는<br>여섯 가지 블러 컬러.','부드럽게 펴 바르고, 보송하게 마무리하는<br>여섯 가지 블러 컬러.')
markup=markup.replace('assets/hero.jpg','assets/hero-cloud.jpg').replace('핑크 배경 위 클라우드 크림 블러셔 세 가지 제품의 원본 촬영 컷','구름과 하늘 배경 위 클라우드 크림 블러셔 세 가지 제품')
markup=re.sub(r'<section class="section texture">.*?</section>\s*','',markup,flags=re.S)
texture='''<section class="section texture" id="texture">
 <header class="heading"><span class="label">CREAM TO POWDER</span><h2>바를 땐 크림,<br>마무리는 보송.</h2></header>
 <div class="wide-film"><video id="texture-film" controls muted loop playsinline preload="metadata" poster="assets/cream-to-powder-poster.jpg" aria-label="크림 제형을 덜고 얇게 펴 바른 뒤 볼 메이크업을 보여주는 영상"><source src="assets/cream-to-powder.mp4" type="video/mp4"></video></div>
 <div class="film-actions"><button class="film-toggle" type="button" aria-controls="texture-film" aria-pressed="false" hidden>영상 재생</button></div>
 <ol class="texture-stages" aria-label="영상의 세 단계"><li data-start="0"><span>01</span>부드러운 크림</li><li data-start="2.6"><span>02</span>얇게 블렌딩</li><li data-start="7.4"><span>03</span>보송한 마무리</li></ol>
 <p class="body">손끝으로 부드럽게 펴 바르면<br>볼 위에 파우더리하게 마무리돼요.</p>
</section>
<section class="model" aria-label="클라우드 크림 블러셔 메이크업 연출">
 <div class="model-photo"><img src="assets/moa-blush.jpg" width="1200" height="1800" loading="lazy" alt="블러셔를 얼굴 옆에 든 모아 모델의 핑크 볼 메이크업 연출"></div>
</section>'''
markup=re.sub(r'<section class="section application">.*?</section>',texture,markup,flags=re.S)
markup=re.sub(r'\s*<div class="formula-photo">.*?</div>','',markup,flags=re.S)
markup=markup.replace('<h2>보송한 컬러에 담은<br>식물성 오일.</h2><p class="body">여섯 가지 컬러에 공통으로 담았어요.</p>','<h2>식물성 오일을 담은<br>비건 포뮬러.</h2>')
(out/'detail.template.html').write_text(markup,encoding='utf8')
css=(v1/'detail.css').read_text(encoding='utf8')
css+='''
/* V2: texture first, one Moa portrait, quieter formula support. */
#cloud-blush .campaign{aspect-ratio:auto}
#cloud-blush .campaign img{height:auto;object-fit:contain}
#cloud-blush .wide-film{aspect-ratio:3/2}
#cloud-blush .wide-film video{object-fit:contain;background:#fff}
#cloud-blush .film-actions{min-height:56px;display:flex;justify-content:flex-end;align-items:center}
#cloud-blush .film-toggle{margin:8px 0;border-radius:24px;min-width:100px}
#cloud-blush .film-toggle[hidden]{display:none}
#cloud-blush .texture-stages{display:grid;grid-template-columns:repeat(3,1fr);list-style:none;padding:0;text-align:center;gap:12px;margin-top:12px}
#cloud-blush .texture-stages li{border-top:2px solid #e1d9dd;padding-top:15px;font-size:clamp(12px,2.55cqw,22px);color:#6f6a6b}
#cloud-blush .texture-stages li.active{border-color:var(--rose);color:var(--rose)}
#cloud-blush .texture-stages span{display:block;font:400 clamp(11px,1.86cqw,16px)/1.5 CloudEnglish,sans-serif;margin-bottom:5px}
#cloud-blush .model-photo{aspect-ratio:4/5;overflow:hidden;background:#b2afd0}
#cloud-blush .model-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 25%}
#cloud-blush .formula .heading{margin-bottom:0}
#cloud-blush .formula .ingredients{padding-top:32px;border-top:1px solid #e4d8de}
@container(max-width:600px){#cloud-blush .texture-stages{gap:8px}#cloud-blush .texture-stages li{padding-top:12px}#cloud-blush .formula .ingredients{padding-top:25px}}
'''
(out/'detail.css').write_text(css,encoding='utf8')
shell='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>탐뷰티 | 더 클라우드 블러 크림 블러셔 · V2</title><meta name="description" content="크림처럼 부드럽게, 파우더처럼 보송하게. 더 클라우드 블러 크림 블러셔의 제형과 여섯 가지 쉐이크 컬러를 만나보세요."><link rel="stylesheet" href="detail.css"><script src="detail.js" defer></script></head><body><main>'
(out/'index.html').write_text(shell+markup+'</main></body></html>',encoding='utf8')
print(out)
