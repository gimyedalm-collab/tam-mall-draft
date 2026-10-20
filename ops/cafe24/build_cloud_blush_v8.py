from pathlib import Path
from PIL import Image
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cloud-blush-v8';A=OUT/'assets';A.mkdir(parents=True,exist_ok=True)
SRC=next(next((Path.home()/'Desktop').glob('_*디모멘텀')).glob('*/08. 더 클라우드 블러 크림 블러셔'))
ledger=[]
for shade,view in [(1,2),(6,2),(2,1),(4,1)]:
    src=next((SRC/'누끼').glob(f'0{shade}호 *{view}.png'));out=A/f'product-{shade}-{view}.png'
    im=Image.open(src).convert('RGBA');box=im.getchannel('A').getbbox();im=im.crop(box);im.thumbnail((1500,1500),Image.Resampling.LANCZOS);im.save(out)
    ledger.append(dict(file=out.relative_to(OUT).as_posix(),source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),operation='Alpha bbox trim and proportional resize only; placement/rotation in HTML; no recolour',size=im.size))
(OUT/'asset-provenance.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
names=['백도 쉐이크','구아바 쉐이크','아사이베리 쉐이크','파파야 쉐이크','용과 쉐이크','살구 쉐이크']
eng=['White Peach','Guava','Acai Berry','Papaya','Dragon Fruit','Apricot']
tones=['피치 핑크','로지 핑크','라벤더 핑크','코랄 오렌지','선명한 핑크','살구 베이지']
V7='../cloud-blush-v7/assets/';V6='../cloud-blush-v6/assets/'
wrists=''.join(f'<figure><img src="{V6}arm-{i}.jpg" alt="{i:02} {n} 손목 발색"><figcaption>{i:02} {n.replace(" 쉐이크","")}</figcaption></figure>' for i,n in enumerate(names,1))
cards=''.join(f'<figure><figcaption>{i:02} <i>{e}</i></figcaption><img src="{V7}texture-{i}-original.png" alt="{i:02} {n} 제형 원본"><p>{n.replace(" 쉐이크","")}</p><small>{t}</small></figure>' for i,(n,e,t) in enumerate(zip(names,eng,tones),1))
faces=''.join(f'<figure class="face-row export-panel" id="face-{i}" data-ref="04–06"><div class="cheek"><img src="{V7}cheek-{i}-r1.jpg" alt="{i:02} {n} 제공 1차 얼굴 발색"></div><figcaption><p class="english">{i:02} <i>{e}</i></p><h3>{n}</h3><p class="tone">{t}</p></figcaption></figure>' for i,(n,e,t) in enumerate(zip(names,eng,tones),1))
info=(ROOT/'cloud-blush-v7/product-information.html').read_text(encoding='utf-8');(OUT/'product-information.html').write_text(info,encoding='utf-8')
body=f'''<article id="cloud-blush">
<section class="hero export-panel" id="hero" data-ref="01"><div class="hero-copy"><h1>Cream <i>to</i> Powder</h1><h2>크림처럼 사르르,<br><strong>파우더처럼 보송하게.</strong></h2><p>#크림투파우더 &nbsp; #보송한마무리</p></div><img class="hero-open-one" src="assets/product-1-2.png" alt="탐뷰티 백도 쉐이크 열린 제품 원본"><img class="hero-open-two" src="assets/product-6-2.png" alt="탐뷰티 살구 쉐이크 열린 제품 원본"><img class="hero-closed" src="assets/product-2-1.png" alt="탐뷰티 구아바 쉐이크 닫힌 제품 원본"></section>
<section class="intro export-panel" id="introduction" data-ref="01"><header><h2>더 클라우드 블러 크림 블러셔</h2><p class="serif">The Cloud Blur<br><i>Cream Blusher</i></p><div class="keywords"><span>크림투파우더</span><span>6가지 컬러</span><span>비건 포뮬러</span></div></header><img src="../cloud-blush-v3/assets/ending.jpg" alt="탐뷰티 여섯 컬러 제품 원본 사진"></section>
<section class="palette export-panel" id="palette" data-ref="03"><header class="heading"><h2>Blush <i>Colour</i> Shades</h2><p>볼 위에 부드럽게 펴 바르는<br><strong>여섯 가지 블러셔 컬러</strong></p></header><div class="wrist-grid">{wrists}</div><div class="texture-grid">{cards}</div><p class="note">피부색·사용량·조명 및 화면 환경에 따라<br>발색이 다르게 보일 수 있습니다.</p></section>
<section id="faces" class="faces" data-ref="04–06"><header class="heading export-panel"><h2 class="halo"><i>Colour</i> on Cheeks</h2></header>{faces}<div class="export-panel face-end"></div></section>
<section id="texture" class="texture" data-ref="07"><header class="heading export-panel"><h2>Cream <i>to</i> Powder</h2><p><strong>펴 바를 땐 부드럽게,<br>마무리는 보송하게.</strong></p></header><div class="motion-wrap export-motion" data-gif="../cloud-blush-v7/assets/texture-touch.gif"><img src="{V7}texture-touch.gif" alt="제공 원본의 크림 제형을 손끝에 묻히는 장면"></div><div class="texture-strip export-panel"><span><i>Cream</i></span><b></b><span><i>Powder</i></span></div><div class="texture-bottom export-panel"><p>크림처럼 부드럽게 펴 발리고<br><strong>파우더처럼 보송하게 마무리돼요.</strong></p></div></section>
<section id="formula" class="formula export-panel" data-ref="09"><header class="heading"><h2>Four <i>Botanical</i> Oils</h2><p><strong class="highlight">네 가지 식물성 오일 함유</strong></p><p class="oil-names">살구씨 · 동백나무씨<br>올리브 · 서양자두씨오일</p></header><figure class="oil-still"><img src="{V6}formula-clear-oil-261019.jpg" alt="맑은 오일을 표현한 기존 원료 연출 이미지"><img class="oil-product" src="assets/product-4-1.png" alt="탐뷰티 파파야 쉐이크 닫힌 제품 원본"></figure><p class="note">원료를 표현한 연출 이미지입니다.</p></section>
<section id="howto" class="howto" data-ref="10"><header class="heading export-panel"><h2 class="oval">How to Use</h2><p><strong>손끝이나 도구로 얇게 펴 바른 뒤</strong><br>경계를 가볍게 두드려 주세요.</p></header><div class="motion-wrap inset export-motion" data-gif="../cloud-blush-v7/assets/howto-spread.gif"><img src="{V7}howto-spread.gif" alt="제공 원본의 블러셔를 손으로 얇게 펴 바르는 장면"></div><div class="howto-end export-panel"></div></section>
<section id="vegan" class="vegan export-panel" data-ref="11"><header class="heading"><h2><i>Vegan</i> Formula</h2><p><strong>탐뷰티의 비건 포뮬러</strong></p></header><figure class="vegan-still"><img src="{V7}vegan-background.png" alt="기존 생성 식물 장식 배경"><img class="vegan-product" src="{V7}compact-original.png" alt="탐뷰티 백도 쉐이크 원본 제품 누끼"></figure></section>
<section id="check" class="check export-panel" data-ref="12"><h2 class="serif">Check point</h2><div class="stem"></div><div class="check-box"><p>개봉 후 사용 기한</p><strong>12개월</strong><p>개봉 전 사용 기한은 36개월입니다.</p></div><img class="logo" src="../cloud-blush-v3/assets/tam-logo.svg" alt="TAM BEAUTY"></section>{info}</article>'''
body=body.replace('<h1>Cream <i>to</i> Powder</h1>','<h1>The <i>Cloud</i> Blur</h1>')
body=body.replace('<div class="export-panel face-end"></div>','<div class="export-panel face-end"><p class="note">피부색·사용량·조명 및 화면 환경에 따라<br>발색이 다르게 보일 수 있습니다.</p></div>')
(OUT/'detail.template.html').write_text(body,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM Cloud · V8 레퍼런스 디자인 치환본</title><link rel="stylesheet" href="detail.css"></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
print('V8 reference geometry assembled',flush=True)
